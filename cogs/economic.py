import asyncio
import datetime
import json
import os
import re
import threading
import nextcord
import requests
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from main import cursor, connection


class Buttons(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="✔ Наш человек", style=nextcord.ButtonStyle.green)
    async def one(self, button: nextcord.ui.Button, inter: Interaction):
        self.value = "1"
        self.stop()

    @nextcord.ui.button(label="🔘 Админ", style=nextcord.ButtonStyle.green)
    async def two(self, button: nextcord.ui.Button, inter: Interaction):
        self.value = "3"
        self.stop()

    @nextcord.ui.button(label="🔰 Бог", style=nextcord.ButtonStyle.green)
    async def three(self, button: nextcord.ui.Button, inter: Interaction):
        self.value = "2"
        self.stop()

    @nextcord.ui.button(label='Подписка "Премиум"', style=nextcord.ButtonStyle.green)
    async def four(self, button: nextcord.ui.Button, inter: Interaction):
        self.value = "4"
        self.stop()

    @nextcord.ui.button(label="Обнуление 1-ого уровня предупреждений", style=nextcord.ButtonStyle.green)
    async def five(self, button: nextcord.ui.Button, inter: Interaction):
        self.value = "5"
        self.stop()


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Выведет баланс пользователя", force_global=False)
    async def balance(
            self,
            inter: Interaction,
            user: nextcord.Member = SlashOption(
                name="ник",
                description="Укажите ник того, кого хотите узнать баланс"
            )
    ):
        cursor.execute(f"SELECT cash FROM users WHERE id = {user.id}")
        results = cursor.fetchone()[0]
        await inter.response.send_message(embed=nextcord.Embed(
            description=f"""Баланс пользователя **{user.mention}** составляет: **{results}** :leaves:"""
        ))

    @nextcord.slash_command(description="Выдача листочков пользователю", force_global=False)
    async def give(
            self,
            inter: Interaction,
            user: nextcord.Member = SlashOption(
                name="ник",
                description="Укажите ник того, кому хотите выдать 🍃"
            ),
            amount: int = SlashOption(
                name="сколько",
                description="Укажите сколько будет начислено"
            )
    ):
        if inter.user.guild_permissions.administrator:
            if amount <= 0:
                embed = nextcord.Embed(title="", color=0xaa0000)
                embed.add_field(name="⚠ Ошибка!", value="Количество :leaves: должно быть больше 0")
                await inter.response.send_message(embed=embed)
            else:
                cursor.execute(f"UPDATE users SET cash = cash + {amount} WHERE id = {user.id}")
                connection.commit()
                complete = nextcord.Embed(
                    color=nextcord.Color.from_rgb(17, 255, 0)
                )
                complete.add_field(name="Успешно!", value="Команда успешно выполнена!")
                await inter.response.send_message(embed=complete)

                channel = self.bot.get_channel(921364597888413766)
                await channel.send(f"{inter.user.mention} выдал {user.mention} {amount} :leaves:")
        else:
            embed = nextcord.Embed(title="", color=0xaa0000)
            embed.add_field(name="⚠ Ошибка!", value="Недостаточно прав!")
            await inter.response.send_message(embed=embed)


    @nextcord.slash_command(description="Таблица самых богатых людей сервера", force_global=False)
    async def leaderboard(self, inter: Interaction):
        embed = nextcord.Embed(title='Топ 10 сервера', color=0x00d166)
        counter = 0
        cursor.execute(f"SELECT name, cash FROM users WHERE server_id = {inter.guild.id} ORDER BY cash DESC LIMIT 10")
        result = cursor.fetchall()

        for row in result:
            counter += 1
            embed.add_field(
                name=f'# {counter} | ``{row[0]}``',
                value=f'Баланс: {row[1]} :leaves:',
                inline=False
            )

        await inter.response.send_message(embed=embed)

    @nextcord.slash_command(description="Команда передачи своих 🍃 другому пользователю", force_global=False)
    async def convey(
            self,
            inter: Interaction,
            user: nextcord.Member = SlashOption(
                name="ник",
                description="Укажите ник комы будет осуществлён перевод"
            ),
            amount: int = SlashOption(
                name="сколько",
                description="Укажите количество переводимых 🍃"
            )
    ):
        if user is inter.user:
            embed = nextcord.Embed(title="", color=0xaa0000)
            embed.add_field(name="⚠ Ошибка!", value="Ты не можешь перевести :leaves: самому себе!")
            await inter.response.send_message(embed=embed)
        elif amount <= 0:
            embed = nextcord.Embed(title="", color=0xaa0000)
            embed.add_field(name="⚠ Ошибка!", value="Количество :leaves: должно быть больше 0.")
            await inter.response.send_message(embed=embed)
        else:
            cursor.execute(f"SELECT cash FROM users WHERE id = {inter.user.id}")
            money = cursor.fetchone()[0]
            if money >= amount:
                cursor.execute(f"UPDATE users SET cash = cash + {amount} WHERE id = {user.id}")
                cursor.execute(f"UPDATE users SET cash = cash - {amount} WHERE id = {inter.user.id}")
                connection.commit()
                await inter.response.send_message(
                    embed=nextcord.Embed(
                        description="✅ Перевод прошёл успешно!",
                        color=0x00d166
                    )
                )
                channel = self.bot.get_channel(921364597888413766)
                await channel.send(f"{inter.user.mention} перевёл {user.mention} {amount} :leaves:.")
            elif amount >= money:
                embed = nextcord.Embed(title="", color=0xaa0000)
                embed.add_field(name="⚠ Ошибка!", value="Недостаточно средств!")
                await inter.response.send_message(embed=embed)

    @nextcord.slash_command(description="Магазин сервера", force_global=False)
    async def shop(self, inter: Interaction):
        embed = nextcord.Embed(title="Магазин", color=0x00d166)
        cursor.execute(
            f"SELECT item_num, role_id, cost, item_type, description FROM shop WHERE server_id = {inter.guild.id}")
        for row in cursor.fetchall():
            if row[3] == "role":
                embed.add_field(
                    name=f"Товар: ``{inter.guild.get_role(row[1])}``",
                    value=f"Стоимость: {row[2]} :leaves:"
                )
            else:
                embed.add_field(
                    name=f"Товар: ``{row[4]}``",
                    value=f"Стоимость: {row[2]} :leaves:"
                )
        view = Buttons()
        await inter.response.send_message(embed=embed, view=view)
        await view.wait()

        cursor.execute(f"SELECT item_type FROM shop WHERE item_num = {view.value}")
        itemType = cursor.fetchone()[0]
        cursor.execute(f"SELECT cost FROM shop WHERE item_num = {view.value}")
        cost = cursor.fetchone()[0]
        cursor.execute(f"SELECT role_id FROM shop WHERE item_num = {view.value}")
        role = inter.guild.get_role(cursor.fetchone()[0])
        cursor.execute(f"SELECT premium FROM users WHERE id = {inter.user.id}")
        isPremium = cursor.fetchone()[0]
        cursor.execute(f"SELECT cash FROM users WHERE id = {inter.user.id}")
        cash = cursor.fetchone()[0]
        cursor.execute(f"SELECT bad_omen FROM users WHERE id = {inter.user.id}")
        Bad_Omen = cursor.fetchone()[0]

        print(inter.user.name)

        if cash < cost:
            await inter.response.reply(f"{inter.user.mention}, у тебя недостаточно средств для покупки данного товара")
        else:
            if view.value == "1" or view.value == "2" or view.value == "3":
                if role in inter.user.roles:
                    await inter.followup.send(f"{inter.user.mention}, у вас уже имеется данная роль.")
                else:
                    await inter.user.add_roles(role)
                    cursor.execute(f"UPDATE users SET cash = cash - {cost} WHERE id = {inter.user.id}")
                    if isPremium is True:
                        cursor.execute(f"UPDATE users SET spent = spent + {cost} WHERE id = {inter.user.id}")
                    await inter.followup.send(
                        embed=nextcord.Embed(
                            description="✅ Покупка прошла успешно!",
                            color=0x00d166
                        )
                    )
                    msg = f"{inter.user.mention} преобрёл роль: \"{role.mention}\"."
                    channel = self.bot.get_channel(921364597888413766)
                    await channel.send(msg)
            elif view.value == "4":
                if isPremium == 1:
                    await inter.followup.send(f"{inter.user.mention}, у вас уже имеется премиум подписка.")
                else:
                    cursor.execute(f"UPDATE users SET premium = true WHERE id = {inter.user.id}")
                    cursor.execute(f"UPDATE users SET cash = cash - {cost} WHERE id = {inter.user.id}")
                    await inter.followup.send(
                        embed=nextcord.Embed(description="✅ Покупка прошла успешно!", color=0x00d166))
                    msg = f"{inter.user.mention} преобрёл \"Премиум подписку\"."
                    channel = self.bot.get_channel(921364597888413766)
                    await channel.send(msg)
            elif view.value == "5":
                if Bad_Omen == 0:
                    await inter.followup.send(f"{inter.user.mention}, у вас 0 уровень предупреждений.")
                else:
                    if isPremium == True:
                        cursor.execute(f"UPDATE users SET spent = spent + {cost} WHERE id = {inter.user.id}")
                    cursor.execute(f"UPDATE users SET bad_omen = bad_omen - 1 WHERE id = {inter.user.id}")
                    cursor.execute(f"UPDATE users SET cash = cash - {cost} WHERE id = {inter.user.id}")
                    await inter.followup.send(
                        embed=nextcord.Embed(
                            description="✅ Покупка прошла успешно!",
                            color=0x00d166
                        )
                    )
                    msg = f"{inter.user.mention} преобрёл \"Понижение уровня предупреждения\"."
                    channel = self.bot.get_channel(921364597888413766)
                    await channel.send(msg)
        connection.commit()


def checkTime():
    threading.Timer(1, checkTime).start()

    now = datetime.datetime.now()

    current_time = now.strftime("%H:%M:%S")
    currentDay = datetime.datetime.now().day

    if (current_time == '00:00:00'):
        print('Баллы были отправлены')
        cursor.execute(f"UPDATE users SET cash = cash + 10")
        print("Баллы из игру в brawlhalla были выданы")
        update_xp()
    if currentDay == 1 and current_time == '00:00:00':
        print("Jackpot был увеличен!")
        cursor.execute("UPDATE cashcasino SET cash = cash + cash")
        print("Кешбек был возвращен")
        cursor.execute(f'UPDATE users SET cash = cash + spent * 0.04')
        cursor.execute(f'UPDATE users SET spent = 0')
    connection.commit()


checkTime()

def update_xp():
    amount = len(cursor.execute(f"SELECT user_id FROM brawlhalla").fetchall())
    i = 0
    while i <= amount - 1:
        user_id = str(cursor.execute(f"SELECT user_id FROM brawlhalla").fetchall()[i])
        id = int(re.sub(r'[(,)]', '', user_id))
        i += 1

        xp = cursor.execute(f"SELECT xp FROM brawlhalla WHERE user_id = {id}").fetchone()[0]
        cursor.execute(f"UPDATE brawlhalla SET old_xp = {xp} WHERE `user_id` = {id}")

        brawlhalla_id = cursor.execute(f"SELECT brawlhalla_id FROM brawlhalla WHERE user_id = {id}").fetchone()[0]
        result = requests.get(f"https://api.brawlhalla.com/player/{brawlhalla_id}/stats?api_key={os.getenv('BRAWLHALLA_API')}")
        with open("user.json", "w") as user:
            user.write(result.text)
        with open("user.json", "r") as user:
            level = json.load(user)
        file = os.path.join("user.json")
        os.remove(file)
        cursor.execute(f"UPDATE brawlhalla SET xp = {level['xp']}, old_xp = {level['xp']} WHERE user_id = {id}")

        old_xp = cursor.execute(f"SELECT old_xp FROM brawlhalla WHERE user_id = {id}").fetchone()[0]
        xp = level['xp']
        cash = xp - old_xp
        prem = cursor.execute(f"SELECT premium FROM users WHERE id = {id}").fetchone()[0]
        if prem == 1:
            cash *= 0.15
        else:
            cash *= 0.1

        cursor.execute(f"UPDATE users SET cash = cash + {int(cash)}")
        connection.commit()


def setup(bot):
    bot.add_cog(events(bot))
