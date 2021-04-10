# totally not taken from https://github.com/MenuDocs/Discord.PY-Tutorials/blob/Episode-20/utils/util.py
import discord
from discord.ext.buttons import Paginator


class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass
