import asyncio
import json
import random
import sqlite3
import string
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from main import cursor, connection

load_dotenv()


class event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                cursor.execute(f"SELECT id FROM users WHERE id = {member.id}")
                results = cursor.fetchone()
                if not member.bot:
                    if results is None:
                        cursor.execute(
                            f"INSERT INTO users VALUES ('{member}','{member.id}',false,0,0,'{guild.id}',0,0)")
                    else:
                        pass
            cursor.execute(f"SELECT cash FROM CashCasino WHERE server_id = {guild.id}")
            serverCash = cursor.fetchone()
            if serverCash is None:
                cursor.execute(f"INSERT INTO CashCasino VALUES (0,'{guild.id}')")
            else:
                pass
        connection.commit()
        print("База данный загружена!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        cursor.execute(f"SELECT id FROM users WHERE id = {member.id}")
        results = cursor.fetchone()
        if not member.bot:
            if results is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}','{member.id}',0,'{member.guild.id},0,0')")
                connection.commit()

        role = member.guild.get_role(role_id=547109093907628046)
        await member.add_roles(role)
        my_channel = self.bot.get_channel(550082377637036035)
        emb = nextcord.Embed(color=0x00d166)
        emb.add_field(name='У нас пополнение!', value=f'Приветствуем {member.mention}.')
        await my_channel.send(ember=emb)

        embed = nextcord.Embed(color=0x9932cc)
        embed.description = f"Настоятельно рекомендую посетить сайт сервера для ознакомления.\nhttps://ssquadinfo.tk/"
        embed.set_author(name="Привет я Мику! Я управляющая этим сервером SSquad.")
        await member.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        OffMat = ["Или мне кажется, или ты матюкнулся {}?\nНадеюсь показалось, а то забаню!",
                  "Я конечно не профессионалка, но мне показалось что ты материшься {}",
                  "Не используй таких слов, хорошо {}?"]

        if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in
            message.content.split(' ')}.intersection(set(json.load(open('./other/cenz.json')))) != set():

            role = message.author.guild.get_role(874610184692072478)

            cursor.execute(f"UPDATE users SET warns = warns + 1 WHERE id = {message.author.id}")

            await message.channel.send(random.choice(OffMat).format(message.author.mention))

            cursor.execute(f"SELECT warns FROM users WHERE id = {message.author.id}")
            Warns = cursor.fetchone()[0]
            cursor.execute(f"SELECT bad_omen FROM users WHERE id = {message.author.id}")
            Bad_Omen = cursor.fetchone()[0]

            if Warns >= 5 and Bad_Omen == 0:
                cursor.execute(f"UPDATE users SET bad_omen = bad_omen + 1 WHERE id = {message.author.id}")
                cursor.execute(f"UPDATE users SET warns = 0 WHERE id = {message.author.id}")

                emb = nextcord.Embed(title="Оповещение от Мику!", description="Мут", color=0xff0000)
                emb.add_field(name="Вам был выдан мут на 5 минут", value="Причина: Мат", inline=False)
                await message.author.send(embed=emb)

                msg = f"Мику заткнула {message.author.mention} на 5 минут."
                channel = self.bot.get_channel(921364597888413766)
                await channel.send(msg)

                await message.author.add_roles(role)
                await message.author.move_to(None)
                await asyncio.sleep(5 * 60)
                await message.author.remove_roles(role)
            elif Warns >= 5 and Bad_Omen == 1:
                cursor.execute(f"UPDATE users SET bad_omen = bad_omen + 1 WHERE id = {message.author.id}")
                cursor.execute(f"UPDATE users SET warns = 0 WHERE id = {message.author.id}")

                emb = nextcord.Embed(title="Оповещение от Мику!", description="Мут", color=0xff0000)
                emb.add_field(name="Вам был выдан мут на 15 минут", value="Причина: Мат", inline=False)
                await message.author.send(embed=emb)

                msg = f"Мику заткнула {message.author.mention} на 15 минут."
                channel = self.bot.get_channel(921364597888413766)
                await channel.send(msg)

                await message.author.add_roles(role)
                await message.author.move_to(None)
                await asyncio.sleep(15 * 60)
                await message.author.remove_roles(role)
            elif Warns >= 5 and Bad_Omen == 2:
                cursor.execute(f"UPDATE users SET bad_omen = bad_omen + 1 WHERE id = {message.author.id}")
                cursor.execute(f"UPDATE users SET warns = 0 WHERE id = {message.author.id}")

                emb = nextcord.Embed(title="Оповещение от Мику!", description="Мут", color=0xff0000)
                emb.add_field(name="Вам был выдан мут на 30 минут", value="Причина: Мат", inline=False)
                await message.author.send(embed=emb)

                msg = f"Мику заткнула {message.author.mention} на 30 минут."
                channel = self.bot.get_channel(921364597888413766)
                await channel.send(msg)

                await message.author.add_roles(role)
                await message.author.move_to(None)
                await asyncio.sleep(30 * 60)
                await message.author.remove_roles(role)
            elif Warns >= 5 and Bad_Omen == 3:
                cursor.execute(f"UPDATE users SET bad_omen = bad_omen + 1 WHERE id = {message.author.id}")
                cursor.execute(f"UPDATE users SET warns = 0 WHERE id = {message.author.id}")

                emb = nextcord.Embed(title="Оповещение от Мику!", description="Мут", color=0xff0000)
                emb.add_field(name="Вам был выдан мут на 1 час", value="Причина: Мат", inline=False)
                await message.author.send(embed=emb)

                msg = f"Мику заткнула {message.author.mention} на 1 час."
                channel = self.bot.get_channel(921364597888413766)
                await channel.send(msg)

                await message.author.add_roles(role)
                await message.author.move_to(None)
                await asyncio.sleep(60 * 60)
                await message.author.remove_roles(role)
            elif Warns >= 5 and Bad_Omen == 4:
                cursor.execute(f"UPDATE users SET bad_omen = bad_omen + 1 WHERE id = {message.author.id}")
                cursor.execute(f"UPDATE users SET warns = 0 WHERE id = {message.author.id}")

                emb = nextcord.Embed(title="Оповещение от Мику!", description="Мут", color=0xff0000)
                emb.add_field(name="Вам был выдан мут на 1 сутки", value="Причина: Мат", inline=False)
                await message.author.send(embed=emb)

                msg = f"Мику заткнула {message.author.mention} на 1 сутки."
                channel = self.bot.get_channel(921364597888413766)
                await channel.send(msg)

                await message.author.add_roles(role)
                await message.author.move_to(None)
                await asyncio.sleep(24 * 60 * 60)
                await message.author.remove_roles(role)
            elif Warns >= 10 and Bad_Omen == 5:
                cursor.execute(f"UPDATE users SET bad_omen = 0 WHERE id = {message.author.id}")
                cursor.execute(f"UPDATE users SET warns = 0 WHERE id = {message.author.id}")

                cursor.execute("SELECT cash FROM users WHERE id = {}".format(message.author.id))
                money = str(cursor.fetchone()[0])
                cursor.execute(f"UPDATE cashcasino SET cash = cash + {money}")

                emb = nextcord.Embed(title="Оповещение от Мику!", description="Бан", color=0xff0000)
                emb.add_field(name="Вам был выдан бан", value="Причина: Мат", inline=False)
                emb.set_image(url="https://thumbs.gfycat.com/AcceptableAgitatedBarbet-size_restricted.gif")
                await message.author.send(embed=emb)

                await message.author.ban(reason="Мат")

                msg = f"Мику выдала бан {message.author.mention}, по причине \"Мат\"."
                channel = self.bot.get_channel(921364597888413766)
                await channel.send(msg)

                emb = nextcord.Embed(title="", color=0x00ff00)
                emb.add_field(name="Вам бан!", value="{} был успешно забанен Мику".format(message.author.name))
                emb.set_image(url="https://thumbs.gfycat.com/AcceptableAgitatedBarbet-size_restricted.gif")
                await message.channel.send(embed=emb)

        if '@everyone' in message.content.lower():
            await message.add_reaction('👍')
            await message.add_reaction('👎')

        if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in
            message.content.split(' ')}.intersection(set(json.load(open('./other/vk.json')))) != set():
            await message.add_reaction('<:VK:886578224275025961>')

        if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in
            message.content.split(' ')}.intersection(set(json.load(open('./other/yt.json')))) != set():
            await message.add_reaction('<:YouTube:886325532302655578>')

        if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in
            message.content.split(' ')}.intersection(set(json.load(open('./other/twitch.json')))) != set():
            await message.add_reaction('<:Twitch:886578298543550544>')

        try:
            amount = len(message.content) // 10
            if not message.author.bot:
                godRole = message.guild.get_role(547399773322346508)
                gamerRole = message.guild.get_role(888113637561090080)
                ourRole = message.guild.get_role(547398893579665421)
                if godRole in message.author.roles:  # Для богов
                    amount = round(amount * 1.5)
                    cursor.execute(f"UPDATE users SET cash = cash + {amount} WHERE id = {message.author.id}")
                elif gamerRole in message.author.roles:  # Для геймеров
                    amount = round(amount * 1.3)
                    cursor.execute(f"UPDATE users SET cash = cash + {amount} WHERE id = {message.author.id}")
                elif ourRole in message.author.roles:  # Для наших людей
                    amount = round(amount * 1.2)
                    cursor.execute(f"UPDATE users SET cash = cash + {amount} WHERE id = {message.author.id}")
                else:
                    cursor.execute(f"UPDATE users SET cash = cash + {amount} WHERE id = {message.author.id}")
                connection.commit()
        except Exception as ex:
            print(ex)


def setup(bot):
    bot.add_cog(event(bot))
