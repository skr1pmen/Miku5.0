import random
import nextcord
from discord.ext import commands
from nextcord import Interaction, SlashOption
from main import cursor, connection


class Buttons(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Орёл", style=nextcord.ButtonStyle.green)
    async def one(self, button: nextcord.ui.Button, inter: Interaction):
        self.value = "eagle"
        self.stop()

    @nextcord.ui.button(label="Решка", style=nextcord.ButtonStyle.green)
    async def two(self, button: nextcord.ui.Button, inter: Interaction):
        self.value = "tails"
        self.stop()


class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Игра в монетку", force_global=False)
    async def coin(
            self,
            inter: Interaction,
            coins: int = SlashOption(
                name="количество",
                description="Укажите количество 🍃 для ставки"
            )
    ):
        if coins <= 0:
            embed = nextcord.Embed(title="", color=0xaa0000)
            embed.add_field(name="⚠ Ошибка!", value="Ты должен поставить :leaves: больше чем 0!")
            await inter.response.send_message(embed=embed)
        cursor.execute(f"SELECT cash FROM users WHERE id = {inter.user.id}")
        results = cursor.fetchone()[0]
        if coins > results:
            embed = nextcord.Embed(title="", color=0xaa0000)
            embed.add_field(name="⚠ Ошибка!", value="Недостаточно :leaves: для ставки!")
            await inter.response.send_message(embed=embed)
        else:
            cursor.execute(f"SELECT premium FROM users WHERE id = {inter.user.id}")
            isPremium = cursor.fetchone()[0]

            view = Buttons()
            mes = await inter.response.send_message(f"Ты поставил {coins}:leaves:\nВыбери сторону монетки.", view=view)
            await view.wait()

            side_coin = random.randint(1, 2)
            if view.value == "eagle":
                if side_coin == 1:
                    await inter.followup.send(f"Ты выбрал Орёл!\nВыпала Орёл!\nТы выиграл {coins*2}")
                    cursor.execute(f"UPDATE users SET cash = cash + {coins} WHERE id = {inter.user.id}")
                    msg = f"{inter.user.mention} выиграл в монетку {coins * 2} :leaves:."
                else:
                    await inter.followup.send(f"Ты выбрал Орёл!\nВыпала Решка!\nТы проиграл {coins}")
                    cursor.execute(f"UPDATE users SET cash = cash - {coins} WHERE id = {inter.user.id}")
                    msg = f"{inter.user.mention} проиграл в монетку {coins} :leaves:."
            elif view.value == "tails":
                if side_coin == 1:
                    await inter.followup.send(f"Ты выбрал Решка!\nВыпала Решка!\nТы выиграл {coins*2}")
                    cursor.execute(f"UPDATE users SET cash = cash + {coins} WHERE id = {inter.user.id}")
                    msg = f"{inter.user.mention} выиграл в монетку {coins * 2} :leaves:."
                else:
                    await inter.followup.send(f"Ты выбрал Решка!\nВыпала Орёл!\nТы проиграл {coins}")
                    cursor.execute(f"UPDATE users SET cash = cash - {coins} WHERE id = {inter.user.id}")
                    msg = f"{inter.user.mention} проиграл в монетку {coins} :leaves:."
            await mes.delete()
            channel = self.bot.get_channel(921364597888413766)
            await channel.send(msg)
            if isPremium == 1:
                cursor.execute(f"UPDATE users SET spent = spent + {coins} WHERE id = {inter.user.id}")
        connection.commit()

    @nextcord.slash_command(description="Самое честное казино в мире", force_global=False)
    async def casino(
            self,
            inter: Interaction,
            number: int = SlashOption(
                name="число",
                description="Укажите какое число может выпасть в рулетке"
            )
    ):
        cursor.execute(f"SELECT cash FROM cashcasino WHERE server_id = {inter.guild.id}")
        Jackpot = cursor.fetchone()[0]
        cursor.execute(f"SELECT cash FROM users WHERE id = {inter.user.id}")
        balance = cursor.fetchone()[0]
        if number < 0 or number > 999:
            embed = nextcord.Embed(title="", color=0xaa0000)
            embed.add_field(name="⚠ Ошибка!", value="Необходимо указать число от 0 до 999!")
            await inter.response.send_message(embed=embed)
        else:
            casinoResult = int(random.randint(0, 999))
            cursor.execute(f"SELECT cash FROM users WHERE id = {inter.user.id}")
            results = cursor.fetchone()[0]
            cursor.execute(f"SELECT premium FROM users WHERE id = {inter.user.id}")
            isPremium = cursor.fetchone()[0]
            if 100 > results:
                embed = nextcord.Embed(title="", color=0xaa0000)
                embed.add_field(name="⚠ Ошибка!", value="Недостаточно денег для ставки! Цена ставки 100 :leaves:")
                await inter.response.send_message(embed=embed)
            else:
                if number == casinoResult:
                    cursor.execute(f"UPDATE users SET cash = cash + {Jackpot} WHERE id = {inter.user.id}")
                    cursor.execute(f"UPDATE cashcasino SET cash = 0 WHERE server_id = {inter.guild.id}")
                    cursor.execute(f"SELECT cash FROM cashcasino WHERE server_id = {inter.guild.id}")
                    Jackpot = cursor.fetchone()[0]
                    cursor.execute(f"SELECT cash FROM users WHERE id = {inter.user.id}")
                    balance = cursor.fetchone()[0]
                    await inter.response.send_message(f"Играет {inter.user.mention}\nТвоё число: {number}\nЧисло которое выпало: "
                                                      f"{casinoResult}\nПоздравляю, ты выиграл! Ты сорвал Jackpot в размере: {Jackpot}"
                                                      f":leaves:\nТвой баланс составляет: {balance}:leaves:")
                    msg = f"{inter.user.mention} выиграл в казино {Jackpot} :leaves:\nКак он это вообще сделал?!?."
                else:
                    cursor.execute(f"UPDATE users SET cash = cash - 100 WHERE id = {inter.user.id}")
                    cursor.execute(f"UPDATE cashcasino SET cash = cash + 100 WHERE server_id = {inter.guild.id}")
                    cursor.execute(f"SELECT cash FROM cashcasino WHERE server_id = {inter.guild.id}")
                    Jackpot = cursor.fetchone()[0]
                    cursor.execute(f"SELECT cash FROM users WHERE id = {inter.user.id}")
                    balance = cursor.fetchone()[0]
                    await inter.response.send_message(f"Играет {inter.user.mention}\nТвоё число: {number}\nЧисло "
                                                      f"которое выпало: {casinoResult}\nСожалею, но ты проиграл!\nСумма "
                                                      f"Jackpot'a теперь составляет: {Jackpot}:leaves:\nТвой баланс "
                                                      f"составляет: {balance}:leaves:")
                    msg = f"{inter.user.mention} проиграл в казино."
                channel = self.bot.get_channel(921364597888413766)
                await channel.send(msg)
                if isPremium == 1:
                    cursor.execute(f"UPDATE users SET spent = spent + 100 WHERE id = {inter.user.id}")
        connection.commit()


def setup(bot):
    bot.add_cog(games(bot))
