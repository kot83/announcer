import aiohttp



HASTEBIN_ENDPOINT = 'https://hastebin.com/documents'

HASTEBIN_FMT = 'https://hastebin.com/{}.py'





async def haste(text: str) -> str:
    """ Pastes something to Hastebin, and returns the link to it. """

    async with aiohttp.ClientSession() as session:
        async with session.post(HASTEBIN_ENDPOINT, data=text) as resp:
            resp_json = await resp.json()
            return HASTEBIN_FMT.format(resp_json['key'])

if __name__ == '__main__':
    print(haste('test'))
