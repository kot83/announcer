#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import config
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('a-'), **kwargs)
        for cog in config.cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                print('Could not load extension {0} due to {1.__class__.__name__}: {1}'.format(cog, e))

    async def on_ready(self):
        print('Logged on as {0} (ID: {0.id})'.format(self.user))
        await bot.change_presence(activity=discord.Activity(name='with announcements| a-help', type=1))

bot = Bot()

# write general commands here

async def send_announcement(webhookurl, username, avatar, announcement):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhookurl, adapter=AsyncWebhookAdapter(session))
        await webhook.send(content=announcement, username=username, avatar_url=avatar)

@commands.guild_only()
@bot.command(name='announce', aliases=['a', 'an'])
async def announce(ctx, *, announcement: str):
    '''Announce something in the current channel.'''
    webhooks = await ctx.channel.webhooks()
    webhook=discord.utils.get(webhooks, name='Announcer')
    if not webhooks or not webhook:
        webhook=await ctx.channel.create_webhook(name='Announcer')
    await send_announcement(webhook.url, f'{ctx.author.name}#{ctx.author.discriminator}', avatar=ctx.author.avatar_url, announcement=announcement)
    await ctx.message.delete()

@commands.guild_only()
@bot.command(name='announceurl', aliases=['au', 'url'])
async def announce_url(ctx, url, *, announcement: str):
    '''Announce something with a webhook url.'''
    webhooks = await ctx.channel.webhooks()
    await send_announcement(url, f'{ctx.author.name}#{ctx.author.discriminator}', avatar=ctx.author.avatar_url, announcement=announcement)
    await ctx.message.delete()

@commands.guild_only()
@bot.command(name='leave')
async def clean_up(ctx):
    '''
    Clean up webhooks and leaves the guild.
    The goal here is to leave webhooks not called "Announcer" untouched and leave.
    '''
    webhooks = [await channel.webhooks() for channel in ctx.guild.text_channels]
    filterwebhook = [webhook.name=='Announcer' for webhook in webhooks[0]]
    if filterwebhook:
        for index, value in enumerate(webhooks):
            if filterwebhook[index] == True:
                await value[0].delete()
    await ctx.guild.leave()

bot.run(config.token)
