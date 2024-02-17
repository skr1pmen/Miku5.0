import sqlite3
from nextcord import Interaction
from nextcord.ext import commands


class logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    global connection
    global cursor

    connection = sqlite3.connect('./database.db')
    cursor = connection.cursor()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        msg = f"{member.mention} присоединился к серверу."
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(921364597888413766)
        await channel.send(msg)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        msg = f"{member.mention} покинул сервер."
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(921364597888413766)
        await channel.send(msg)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None:
            msg = f"{member.mention} присоединился к каналу {after.channel.mention}"
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(921364597888413766)
            await channel.send(msg)
        elif after.channel is None:
            msg = f"{member.mention} вышел из канала {before.channel.mention}"
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(921364597888413766)
            await channel.send(msg)
        elif before.channel != after.channel:
            msg = f"{member.mention} перешёл из канала {before.channel.mention} в канал {after.channel.mention}"
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(921364597888413766)
            await channel.send(msg)


def setup(bot):
    bot.add_cog(logs(bot))
