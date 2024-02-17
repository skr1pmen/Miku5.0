import json
import nextcord
import random
from nextcord.ext import commands, activities
from nextcord import Interaction, SlashOption
from dotenv import load_dotenv
from PIL import Image, ImageFont, ImageDraw, ImageChops
from main import cursor
import io

load_dotenv()


def circle(pfp, size=(215, 215)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")

    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Вывод всех команд сервера", force_global=False)
    async def help(self, inter: Interaction):
        with open('./other/help_command.json', "rb") as help_com:
            help_com = json.load(help_com)
        emb = nextcord.Embed(
            title="Список команд",
            colour=0xffff00
        )
        user_perm = inter.user.guild_permissions.administrator
        for i in help_com:
            if user_perm is False and i["is_admin"] is False:
                emb.add_field(name=f'{i["name"]}', value=f'{i["description"]}')
            elif user_perm is False and i["is_admin"] is True:
                continue
            else:
                emb.add_field(name=f'{i["name"]}', value=f'{i["description"]}')
        await inter.response.send_message(embed=emb)

    @nextcord.slash_command(description="Выдаст случайное число в заданных границах.", force_global=False)
    async def random(
            self,
            inter: Interaction,
            first_num: int = SlashOption(
                name='первое',
                description="Первое число для начальной точки рандома"
            ),
            second_num: int = SlashOption(
                name='второе',
                description="Второе число для конечной точки рандома"
            ), ):
        arg = random.randint(first_num, second_num)
        await inter.response.send_message("Твоё число: " + str(arg))

    @nextcord.slash_command(description="Получить список правил сервера", force_global=False)
    async def rules(self, inter: Interaction):
        with open("./other/rules.txt", "r", encoding="utf-8") as rules:
            rules_text = rules.read()
        rules = nextcord.Embed(
            title="В общем давай я расскажу тебе правила сервера.",
            description=rules_text,
            color=0x9932cc
        )
        rules.set_author(name="Привет, я Мику! Я управляющая этим сервером.\nНе считая skr1pmen и его команды Админов "
                              "конечно.")
        await inter.response.send_message(f'{inter.user.mention}, я выслала правила тебе в личку')
        await inter.user.send(embed=rules)

    @nextcord.slash_command(description="Удаление сообщений", force_global=False)
    @commands.has_any_role('Бето-тестер', '🔰 Бог', '🔘 Админ', '👑 Царь')
    async def clear(
            self,
            inter: Interaction,
            limit: int = SlashOption(
                name='количество',
                description="Указать количество сообщений для удаления"
            )):
        if limit < 0:
            embed = nextcord.Embed(color=0xaa0000)
            embed.add_field(name="⚠ Ошибка!", value=f"Невозможно удалить {limit} сообщений!")
            await inter.response.send_message(embed=embed)
        elif limit >= 100:
            embed = nextcord.Embed(color=0xaa0000)
            embed.add_field(name="⚠ Ошибка!",
                            value=f"К сожалению {limit} сообщений нельзя удалить за раз! Максимум 100")
            await inter.response.send_message(embed=embed)
        else:
            await inter.channel.purge(limit=limit)
            complete = nextcord.Embed(
                color=nextcord.Color.from_rgb(17, 255, 0)
            )
            complete.add_field(name="Успешно!", value="Команда успешно выполнена!")
            await inter.response.send_message(embed=complete)

    @nextcord.slash_command(description="Мику расскажет о себе в личных сообщениях", force_global=False)
    async def about(self, inter: Interaction):
        with open("./other/about.json", "rb") as about:
            about_text = json.load(about)

        about = nextcord.Embed(color=0x00bfff)
        about.set_author(name="Мику Хацунэ\nHatsune Miku",
                         url="https://ru.wikipedia.org/wiki/%D0%9C%D0%B8%D0%BA%D1%83_%D0%A5%D0%B0%D1%86%D1%83%D0%BD%D1%8D")
        for a in about_text:
            about.add_field(name=f"{a['name']}", value=f"{a['value']}", inline=False)
        about.set_thumbnail(
            url="https://raw.githubusercontent.com/SkripMen/mikubotskripmen/master/%D0%90%D0%92%D0%90%D0%A2%D0%90%D0%A0%D0%9C%D0%98%D0%9A%D0%A3.png")
        await inter.response.send_message(embed=about)

    @nextcord.slash_command(description="YouTube", force_global=False)
    async def activities(self,
                         inter: Interaction,
                         channel: nextcord.VoiceChannel,
                         activ: str = SlashOption(
                             name="активность",
                             description="Выберете активность",
                             choices={
                                 "YouTube": "1",
                                 "Putt Party": "2",
                                 "Sketch Heads": "3",
                                 "Poker Night": "4",
                                 "Chess In The Park": "5",
                                 "Land-io": "6",
                                 "Letter League": "7",
                                 "Checkers In The Park": "8"
                             }
                         )):
        if activ == "1":
            invite_link = await channel.create_activity_invite(activities.Activity.youtube)
        elif activ == "2":
            invite_link = await channel.create_activity_invite(activities.Activity.putt_party)
        elif activ == "3":
            invite_link = await channel.create_activity_invite(activities.Activity.sketch)
        elif activ == "4":
            invite_link = await channel.create_activity_invite(activities.Activity.poker)
        elif activ == "5":
            invite_link = await channel.create_activity_invite(activities.Activity.chess)
        elif activ == "6":
            invite_link = await channel.create_activity_invite(activities.Activity.land_io)
        elif activ == "7":
            invite_link = await channel.create_activity_invite(activities.Activity.letter_league)
        elif activ == "8":
            invite_link = await channel.create_activity_invite(activities.Activity.checkers)

        await inter.response.send_message(invite_link.url)

    @nextcord.slash_command(description="Выведет информацию о пользователе", force_global=False)
    async def info(
            self,
            inter: Interaction,
            user: nextcord.Member
    ):
        name, nick, id, status = str(user), user.display_name, str(user.id), str(user.status)
        created_at = user.created_at.strftime("%d.%m.%Y")
        joined_at = user.joined_at.strftime("%d.%m.%Y")
        cursor.execute(f"SELECT cash FROM users WHERE id = {user.id}")
        money = str(cursor.fetchone()[0])
        cursor.execute(f"SELECT premium FROM users WHERE id = {user.id}")
        prem = cursor.fetchone()[0]
        roles = str(len(user.roles)-1)
        base = Image.open('./other/base.png').convert('RGBA')
        background = Image.open('./other/bg.png').convert('RGBA')
        # pfp = inter.user.avatar(size=256)
        pfp = user.avatar
        data = io.BytesIO(await pfp.read())
        pfp = Image.open(data).convert('RGBA')
        name = f"{name[:13]}..." if len(name) > 16 else name
        nick = f"AKA:{nick[:17]}..." if len(nick) > 17 else f"AKA:{nick}"
        draw = ImageDraw.Draw(base)
        pfp = circle(pfp, size=(215, 215))
        online = Image.open('./other/online.png').convert('RGBA')
        offline = Image.open('./other/offline.png').convert('RGBA')
        idle = Image.open('./other/idle.png').convert('RGBA')
        dnd = Image.open('./other/dnd.png').convert('RGBA')
        premImg = Image.open('./other/prem.png').convert('RGBA')
        bad_omen = Image.open('./other/bad_omen.png').convert('RGBA')

        font = ImageFont.truetype('./other/arial.ttf', size=38)
        AKAfont = ImageFont.truetype('./other/arial.ttf', size=30)
        subfont = ImageFont.truetype('./other/arial.ttf', size=25)
        bad_omen_font = ImageFont.truetype('./other/minecraft.ttf', size=46)

        if status == 'online':
            pfp.paste(online, (140, 140), online)
        elif status == 'dnd':
            pfp.paste(dnd, (140, 140), dnd)
        elif status == 'offline':
            pfp.paste(offline, (140, 140), offline)
        elif status == 'idle':
            pfp.paste(idle, (140, 140), idle)

        if prem == 1:
            background.paste(premImg, (270, 175), premImg)

        cursor.execute(f"SELECT bad_omen FROM users WHERE id = {user.id}")
        Bad_Omen = cursor.fetchone()[0]
        offset = 3
        shadowColor = 'black'
        x = 100
        y = 94
        dict = {
            1: "I",
            2: "II",
            3: "III",
            4: "IV",
            5: "V",
        }
        for key, value in dict.items():
            if key == Bad_Omen:
                bad_omen_lvl = value
                for off in range(offset):
                    draw.text((x-off, y), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                    draw.text((x+off, y), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                    draw.text((x, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                    draw.text((x, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                    draw.text((x-off, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                    draw.text((x+off, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                    draw.text((x-off, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                    draw.text((x+off, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x, y), bad_omen_lvl, font=bad_omen_font)
                background.paste(bad_omen, (0, 0), bad_omen)

        draw.text((280, 240), name, font=font)
        draw.text((275, 320), nick, font=AKAfont)

        draw.text((65, 490), money, font=subfont)
        draw.text((395, 490), roles, font=subfont)

        draw.text((65, 618), created_at, font=subfont)
        draw.text((395, 618), joined_at, font=subfont)

        draw.text((65, 728), id, font=subfont)

        base.paste(pfp, (56, 158), pfp)

        background.paste(base, (0, 0), base)

        with io.BytesIO() as a:
            background.save(a, "png")
            a.seek(0)
            await inter.response.send_message(file=nextcord.File(a, "profile.png"))


def setup(bot):
    bot.add_cog(Basic(bot))
