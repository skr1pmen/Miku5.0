import os
import sqlite3
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()
intents = nextcord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="•", intents=intents, activity=nextcord.Game(name=f"v{os.getenv('VERSION')}"))
bot.remove_command('help')

global connection
global cursor

connection = sqlite3.connect('./database.db', check_same_thread=False)
cursor = connection.cursor()


@bot.event
async def on_ready():
    print(f'Бот {bot.user.name} запущен!')


initial_extensional = []

for fn in os.listdir('./cogs'):
    if fn.endswith('.py'):
        initial_extensional.append(f'cogs.{fn[:-3]}')

# Создание Комнаты
default_rooms_initted = False
default_room_category_id = 888417923151044608
default_room_creator_id = 888418406469079050

room_category = None
room_creator = None


async def delete_channel(guild, channel_id):
    channel = guild.get_channel(channel_id)
    await channel.delete()


async def create_voice_channel(guild, channel_name):
    channel = await guild.create_voice_channel(channel_name, category=room_category)
    return channel


def init_rooms():
    if default_room_category_id != -1:
        category_channel = bot.get_channel(default_room_category_id)
        if category_channel:
            global room_category
            room_category = category_channel

    if default_room_creator_id != -1:
        create_channel = bot.get_channel(default_room_creator_id)
        if create_channel:
            global room_creator
            room_creator = create_channel

    global default_rooms_initted
    default_rooms_initted = True


@bot.command(aliases=['temp_category_set'])
async def __temp_category_set(ctx, id):
    category_channel = bot.get_channel(int(id))
    if category_channel:
        global room_category
        room_category = category_channel


@bot.command(aliases=['temp_rooms_set'])
async def __temp_rooms_set(ctx, id):
    create_channel = bot.get_channel(int(id))
    if create_channel:
        global room_creator
        room_creator = create_channel


@bot.event
async def on_voice_state_update(member, before, after):
    if not default_rooms_initted:
        init_rooms()

    if not room_category:
        print("Set 'Temp rooms category' id first (temp_category_set)")
        return False

    if not room_creator:
        print("Set 'Temp rooms creator' id first (temp_rooms_set)")
        return False

    if member.bot:
        return False

    if after.channel == room_creator:
        channel = await create_voice_channel(after.channel.guild, f'Комната {member.name}')
        if channel is not None:
            await member.move_to(channel)
            await channel.set_permissions(member, manage_channels=True)

    if before.channel is not None:
        if before.channel != room_creator and before.channel.category == room_category:
            if len(before.channel.members) == 0:
                await delete_channel(before.channel.guild, before.channel.id)


if __name__ == '__main__':
    for extension in initial_extensional:
        bot.load_extension(extension)
    bot.run(os.getenv('TOKEN'))
