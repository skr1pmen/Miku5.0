import json
import os
from urllib.request import urlopen
from xml.etree import ElementTree
import requests
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from dotenv import load_dotenv
from main import cursor, connection

load_dotenv()


class BrawlHalla(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Добавление аккаунта BrawlHalla для получения дополнительных :leaves:", force_global=False)
    async def brawlhalla(self,
            inter: Interaction,
            url: str = SlashOption(
                name='ссылка',
                description="Введите ссылку на свою страницу стима"
            ),):
        game_id = len(cursor.execute(f"SELECT brawlhalla_id FROM brawlhalla WHERE user_id = {inter.user.id}").fetchall())

        if game_id == 0:
            cursor.execute(f"INSERT INTO brawlhalla VALUES ({inter.user.id},0,0,0,0,'{url}')")

            with urlopen(f"{url}/?xml=1") as user:
                tree = ElementTree.parse(user)
                root = tree.getroot()
            xml = root[0].text
            cursor.execute(f"UPDATE brawlhalla SET steam_id = {xml} WHERE user_id = {inter.user.id}")

            result = requests.get(f"https://api.brawlhalla.com/search?steamid={xml}&api_key={os.getenv('BRAWLHALLA_API')}")
            with open("user.json", "w") as user:
                user.write(result.text)
            with open("user.json", "r") as user:
                id = json.load(user)
            id = id['brawlhalla_id']
            cursor.execute(f"UPDATE brawlhalla SET brawlhalla_id = {id} WHERE user_id = {inter.user.id}")

            result = requests.get(f"https://api.brawlhalla.com/player/{id}/stats?api_key={os.getenv('BRAWLHALLA_API')}")
            with open("user.json", "w") as user:
                user.write(result.text)
            with open("user.json", "r") as user:
                level = json.load(user)
            # print(level["xp"])
            file = os.path.join("user.json")
            os.remove(file)
            cursor.execute(f"UPDATE brawlhalla SET xp = {level['xp']}, old_xp = {level['xp']} WHERE user_id = {inter.user.id}")

            embed = nextcord.Embed(color=0xffff00)
            embed.add_field(name="Соединение с BrawlHalla", value=f"Успешно!")
            await inter.response.send_message(embed=embed)
        else:
            embed = nextcord.Embed(color=0xffff00)
            embed.add_field(name="Соединение с BrawlHalla", value=f"Уже было выполнено ранее!")
            await inter.response.send_message(embed=embed)

        connection.commit()


def setup(bot):
    bot.add_cog(BrawlHalla(bot))