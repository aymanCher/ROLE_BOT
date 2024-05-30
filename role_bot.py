import discord
from discord.ext import commands

TOKEN = 'DISCORD_BOT_TOKEN'  
GUILD_ID = 11123  
PUG_ROLE = 'Pug'  
NAGA_ROLE = 'Naga'  
password = '12345'  

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.event
async def on_member_join(member):
    if member.guild.id == GUILD_ID:
        guild = bot.get_guild(GUILD_ID)
        pug_role = discord.utils.get(guild.roles, name=PUG_ROLE)
        if pug_role:
            await member.add_roles(pug_role)
            try:
                await member.send(
                    'Welcome to the server! You have been given the "Pug" role. Please provide the password to receive your "Naga" role.'
                )
            except discord.Forbidden:
                print(f"Couldn't send message to {member.name}.")
        else:
            print(f'Role {PUG_ROLE} not found in guild.')

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
        code = message.content.strip()
        if code == password:
            guild = bot.get_guild(GUILD_ID)
            member = guild.get_member(message.author.id)
            naga_role = discord.utils.get(guild.roles, name=NAGA_ROLE)
            if member and naga_role:
                await member.add_roles(naga_role)
                await message.author.send(f'Role {naga_role.name} has been granted to you.')
            else:
                await message.author.send('Could not find the member or role.')
        else:
            await message.author.send('Invalid code. Please provide a valid 5-digit code.')

bot.run(TOKEN)

