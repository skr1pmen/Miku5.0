import os
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from main import cursor, connection


class commands_for_admins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Кик участника сервера", force_global=False)
    async def kick(self,
                   inter: Interaction,
                   user: nextcord.Member = SlashOption(
                       name="имя",
                       description="Укажите имя жертвы",
                       required=False
                   ),
                   reason: str = SlashOption(
                       name="причина",
                       description="Укажите причину кика с сервера",
                       required=False
                   )):
        if inter.user.guild_permissions.administrator:
            try:
                embed = nextcord.Embed(title="", color=0x00ff00)
                embed.add_field(name="Кик", value=f"Пользователь {user.mention} отключён от сервера!")
                if reason is not None:
                    await user.kick(reason=reason)
                    embed.add_field(name="Причина:", value=f"{reason}")
                else:
                    await user.kick(reason="Причина не указана.")
                    embed.add_field(name="Причина:", value="Причина не указана.")
            except AttributeError:
                embed = nextcord.Embed(title="", color=0xaa0000)
                embed.add_field(name="⚠ Ошибка!", value="Неправильное имя пользователя!")
        else:
            embed = nextcord.Embed(title="", color=0xaa0000)
            embed.add_field(name="⚠ Ошибка!", value="Недостаточно прав!")

        await inter.response.send_message(embed=embed)

    @nextcord.slash_command(description="Бан участника сервера", force_global=False)
    async def ban(self,
                  inter: Interaction,
                  user: nextcord.Member = SlashOption(
                      name="имя",
                      description="Укажите имя жертвы"
                  ),
                  reason: str = SlashOption(
                      name="причина",
                      description="Укажите причину кика с сервера",
                      required=False
                  )):
        if inter.user.guild_permissions.administrator:
            embed = nextcord.Embed(title="", color=0x00ff00)
            embed.add_field(name="Бан", value=f"Пользователь {user.mention} заблокирован!")

            if reason is None:
                reason = "Причина не указана."

            await user.ban(reason=reason)
            embed.add_field(name="Причина:", value=f"{reason}")

            complete = nextcord.Embed(
                color=nextcord.Color.from_rgb(17, 255, 0)
            )
            complete.add_field(name="Успешно!", value="Команда успешно выполнена!")
            await inter.response.send_message(embed=complete)
        else:
            embed = nextcord.Embed(title="", color=0xaa0000)
            embed.add_field(name="⚠ Ошибка!", value="Недостаточно прав!")
            await inter.response.send_message(embed=embed)

        channel = self.bot.get_channel(921364597888413766)
        await channel.send(embed=embed)

    @nextcord.slash_command(description="Разблокировка участника сервера", force_global=False)
    async def unban(self,
                    inter: Interaction,
                    user: nextcord.Member = SlashOption(
                        name="имя",
                        description="Укажите имя жертвы"
                    )):
        if inter.user.guild_permissions.administrator:
            embed = nextcord.Embed(title="", color=0x00ff00)
            embed.add_field(name="Разбан", value=f"Пользователь {user.mention} разблокирован!")
            await user.unban()

            complete = nextcord.Embed(
                color=nextcord.Color.from_rgb(17, 255, 0)
            )
            complete.add_field(name="Успешно!", value="Команда успешно выполнена!")
            await inter.response.send_message(embed=complete)
        else:
            embed = nextcord.Embed(title="", color=0xaa0000)
            embed.add_field(name="⚠ Ошибка!", value="Недостаточно прав!")
            await inter.response.send_message(embed=embed)

        channel = self.bot.get_channel(921364597888413766)
        await channel.send(embed=embed)

    # @nextcord.slash_command(description="Узнать список заблокированных пользователей сервера", force_global=False)
    # @commands.has_permissions(administrator=True)
    # async def mute(self,
    #                inter: Interaction,
    #                user: nextcord.Member = SlashOption(
    #                    name="имя",
    #                    description="Укажите имя жертвы",
    #                    required=False
    #                ),
    #                time: int = SlashOption(
    #                    name="время",
    #                    description="Укажите время мута"
    #                )):
    #     role = user.guild.get_role(874610184692072478)
    #     embed = nextcord.Embed(title="", color=0x00ff00)
    #     embed.add_field(name="Помолчи ка:", value=f'{user} получил мут на {time} минут')
    #     await inter.response.send_message(embed=embed)
    #     msg = f"{user.author.mention} заткнул {user.mention} на {time} минут."
    #     channel = self.bot.get_channel(921364597888413766)
    #     await channel.send(msg)
    #     await user.add_roles(role)
    #     await asyncio.sleep(time * 60)
    #     await user.remove_roles(role)
    #     embed = nextcord.Embed(title="", color=0x00ff00)
    #     embed.add_field(name="Научился говорить:", value=f'{user} наконец-то нашёл кнопку включения микрофона')
    #     await inter.response.send_message(embed=embed)
    #     msg = f"{user.mention} научился говорить после того как {user.author.mention} заткнул его."
    #     channel = self.bot.get_channel(921364597888413766)
    #     await channel.send(msg)

    # @nextcord.slash_command(description="Выдача таймаута участнику", force_global=False)
    # @commands.has_permissions(administrator=True)
    # async def timeout(self):

    @nextcord.slash_command(description="Изменение статуса Мику", force_global=False)
    async def status(
            self,
            inter: Interaction,
            activ: str = SlashOption(
                name="активность",
                description="Выберете активность",
                choices={"Игра": "game", "Стрим": "stream", "Сброс": "default"}
            ),
            name: str = SlashOption(
                name="название",
                description="Название активности для статуса",
                required=False
            ),
            url: str = SlashOption(
                name="ссылка",
                description="Ссылка на стрим",
                required=False
            )):
        if inter.user.guild_permissions.administrator:
            if activ == "game":
                if name is not None:
                    await self.bot.change_presence(activity=nextcord.Game(name=name))

                    complete = nextcord.Embed(
                        color=nextcord.Color.from_rgb(17, 255, 0)
                    )
                    complete.add_field(name="Успешно!", value="Команда успешно выполнена!")
                    await inter.response.send_message(embed=complete)
                else:
                    await inter.response.send_message(f"{inter.user.mention}, поле название не должно быть пустым!")
            elif activ == "stream":
                if name is not None:
                    if url is not None:
                        await self.bot.change_presence(activity=nextcord.Streaming(name=name, url=url))

                        complete = nextcord.Embed(
                            color=nextcord.Color.from_rgb(17, 255, 0)
                        )
                        complete.add_field(name="Успешно!", value="Команда успешно выполнена!")
                        await inter.response.send_message(embed=complete)
                    else:
                        await inter.response.send_message(f"{inter.user.mention}, поле ссылка не должно быть пустым!")
                else:
                    await inter.response.send_message(f"{inter.user.mention}, поле название не должно быть пустым!")
            else:
                await self.bot.change_presence(activity=nextcord.Game(name=f"v{os.getenv('VERSION')}"))

                complete = nextcord.Embed(
                    color=nextcord.Color.from_rgb(17, 255, 0)
                )
                complete.add_field(name="Успешно!", value="Команда успешно выполнена!")
                await inter.response.send_message(embed=complete)
        else:
            embed = nextcord.Embed(title="", color=0xaa0000)
            embed.add_field(name="⚠ Ошибка!", value="Недостаточно прав!")
            await inter.response.send_message(embed=embed)

    @nextcord.slash_command(description="Выдача предупреждения участнику", force_global=False)
    async def warn(self,
                     inter: Interaction,
                     user: nextcord.Member = SlashOption(
                         name="имя",
                         description="Введите имя жертвы"
                     ),
                     reason: str = SlashOption(
                         name="причина",
                         description="Введите причину выдачи предупреждения",
                         required=False
                     )):
        if inter.user.guild_permissions.administrator:
            cursor.execute(f"UPDATE users SET warns = warns + 1 WHERE id = {user.id}")

            cursor.execute(f"SELECT warns FROM users WHERE id = {user.id}")
            Warns = cursor.fetchone()[0]
            cursor.execute(f"SELECT bad_omen FROM users WHERE id = {user.id}")
            Bad_Omen = cursor.fetchone()[0]

            if reason is None:
                reason = "Причина не указана"

            complete = nextcord.Embed(
                color=nextcord.Color.from_rgb(17, 255, 0)
            )
            complete.add_field(name="Успешно!", value="Команда успешно выполнена!")
            await inter.response.send_message(embed=complete)

            msg = f"{inter.user.mention} выдал {Warns} предупреждение {user.mention} {Bad_Omen} уровня.\nПричина: {reason}."
            channel = self.bot.get_channel(921364597888413766)
            await channel.send(msg)

            if Bad_Omen == 0 or Bad_Omen == 1 or Bad_Omen == 2 or Bad_Omen == 3 or Bad_Omen == 4:
                if Warns >= 5:
                    cursor.execute(f"UPDATE users SET bad_omen = bad_omen + 1 WHERE id = {user.id}")
                    cursor.execute(f"UPDATE users SET warns = 0 WHERE id = {user.id}")
            elif Bad_Omen == 5:
                if Warns >= 10:
                    cursor.execute(f"UPDATE users SET bad_omen = 0 WHERE id = {user.id}")
                    cursor.execute(f"UPDATE users SET warns = 0 WHERE id = {user.id}")

                    emb = nextcord.Embed(title="Оповещение от Мику!",
                                         description="Терпению админов пришёл конец.",
                                         color=0xff0000)
                    emb.add_field(name="Вам был выдан бан", value=f"Причина: {reason}", inline=False)
                    await user.send(embed=emb)

                    await user.ban(reason=reason)

                    msg = f"{inter.user.mention} выдал последнее предупреждение {user.mention} и тот был отправлен"\
                          f"в бан, по причине {reason}."
                    channel = self.bot.get_channel(921364597888413766)
                    await channel.send(msg)
            connection.commit()
        else:
            embed = nextcord.Embed(title="", color=0xaa0000)
            embed.add_field(name="⚠ Ошибка!", value="Недостаточно прав!")
            await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(commands_for_admins(bot))
