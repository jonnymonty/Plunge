import discord
from discord.ext import commands, tasks
import random
import math
import json
import asyncio

####################
# Start Setup
####################

# The prefix for all the commands
prefix = "p."

# All active battles for a server
activeBattles = []

# All active users in a battle
activeUsers = []

# Sets the bots prefix and removes the help command for our own custom help command
client = commands.Bot(command_prefix = prefix, case_insensitive=True)
client.remove_command('help')

# The url for our logo
logourl = "https://i.imgur.com/tdbgl13.png"

# Reads the Auth.json File
with open('auth.json', 'r') as f:
    data = json.load(f)

# Displays that the bot is ready and loops through its statuses
@client.event
async def on_ready():
    client.loop.create_task(change_status())
    print('Bot is ready.')

####################
# End Setup
####################

#TODO: Re-write Embed Messages

####################
# Start Bot Methods
####################

# Updates and cycles the bots status
async def change_status():
    while True:
        await client.change_presence(
            activity=discord.Game('Dropped ' + str(await getInfo('drops')) + " times!")
        )

        await asyncio.sleep(15)

        guilds = str(len([g for g in client.guilds]))  # Gets length of all client's guilds
        
        users = 0
        for guild in client.guilds:
            users += len(guild.members)        # Gets how many users are in all of the guilds combined

        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"s: {guilds} • u: {users}")
        )

        await asyncio.sleep(15)

        await client.change_presence(
            activity=discord.Game(' p.help • p.verify • p.invite')
        )

        await asyncio.sleep(15)

        await client.change_presence(
            activity=discord.Game('Hosted ' + str(await getInfo('battles')) + " battles!")
        )

        await asyncio.sleep(15)

        await client.change_presence(
            activity=discord.Game(' p.drop • p.battle • p.stats')
        )

        await asyncio.sleep(15)

# Checks if the authorId is a dev's authorId
def isDev(authorId):
    if authorId == 260698008595726336 or authorId == 534099020230950923 or authorId == 290530439331053579:
        return True 
    else:
        return False

####################
# End Bot Methods
####################

####################
# Start Get Methods
####################

# Gets the bots drop count or the bots battle count
async def getInfo(info):
    with open('info.json', 'r') as f:
        drops = json.load(f)
    
    return drops[info]

# Function to get the keys (users ID) from the userInfo.json
async def getKeys(json):
    items = []
    for key, value in json:
        items.append(key)

    return items

# Function to get the values (server ID) from the userInfo.json
async def getValues(json):
    items = []
    for key, value in json:
        items.append(value)
    
    return items

# Function to get the weapons Rarity
async def getRarity(rarityId):
    with open('rarity.json', 'r') as f:
        rarity = json.load(f)

    return rarity[str(rarityId)]

# Function to get the weapons Range
async def getRange(rangeId):
    with open('ranges.json', 'r') as f:
        ranges = json.load(f)

    return ranges[str(rangeId)]

####################
# End Get Methods
####################

####################
# Start Add Methods
####################

# Adds to the drop counter
async def addDrop():
    with open('info.json', 'r') as f:
        drops = json.load(f)
        
        drops["drops"] += 1

        with open('info.json', 'w') as f:
            json.dump(drops, f, indent=4)

# Adds to the battle counter
async def addBattle():
    with open('info.json', 'r') as f:
        battles = json.load(f)
        
        battles["battles"] += 1

        with open('info.json', 'w') as f:
            json.dump(battles, f, indent=4)


####################
# End Add Methods
####################

####################
# Start User Helper Methods
####################

### Add and Remove Currency ###
# Add gold
async def addGold(userId, gold):
    with open('users.json', 'r') as f:
        data = json.load(f)
    
    data[str(userId)]['inventory']['gold'] += gold

    with open('users.json', 'w') as f:
        json.dump(data, f, indent=4)

# Add gems
async def addGems(userId, gems):
    with open('users.json', 'r') as f:
        data = json.load(f)
    
    data[str(userId)]['inventory']['gems'] += gems

    with open('users.json', 'w') as f:
        json.dump(data, f, indent=4)

# Remove gold
async def removeGold(userId, gold):
    with open('users.json', 'r') as f:
        data = json.load(f)
    
    data[str(userId)]['inventory']['gold'] -= gold

    with open('users.json', 'w') as f:
        json.dump(data, f, indent=4)

# Remove gems
async def removeGems(userId, gems):
    with open('users.json', 'r') as f:
        data = json.load(f)
    
    data[str(userId)]['inventory']['gems'] -= gems

    with open('users.json', 'w') as f:
        json.dump(data, f, indent=4)

####################
# End User Helper Methods
####################

####################
# Start Weapon Helper Methods
####################

####################
# End Weapon Helper Methods
####################

####################
# Start Client Event Methods
####################

# When the bot is directly mentioned "@Plunge", give a description about what the bot is about
@client.event
async def on_message(message):
    if message.content == '<@!732864657932681278>':
        embed=discord.Embed(title="Plunge", description=f"Hey {message.author.mention}, can't decide on where to drop in Fortnite? It happens to us all, we  are riding in the battle bus with our maps open but no location marked.  Before we know it, we are getting kicked off the bus with little to no options to land. Luckily, Plunge Bot can help. With a simple command `p.drop`, Plunge will randomly select a location for you to drop in Fortnite, making your next drop stress free.", color=0xfd5d5d)
        embed.add_field(name="!! Special !!", value="We are currently hosting a giveaway!\nDo `p.giveaway` for information on how to qualify.",inline=False)
        embed.add_field(name="Info", value="Use `p.help` to get started", inline=False)
        embed.set_thumbnail(url=logourl)
        embed.set_footer(text="Created by The Plunge Team")
        await message.channel.send(embed=embed)
    await client.process_commands(message)

# On guild removed, it removes the users role in Plunge development and removes them from the userInfo.json and sends the users effected a dm.
@client.event
async def on_guild_remove(guild):
    ourGuild = client.get_guild(733551377611096195)

    with open('userInfo.json', 'r') as f:
        userInfo = json.load(f)

    for key, value in list(userInfo.items()):
        if (value == str(guild.id)):
            userInfo.pop(key)

            with open('userInfo.json', 'w') as f:
                json.dump(userInfo, f, indent=4)

            await ourGuild.get_member(int(key)).remove_roles(ourGuild.get_role(733559654210207885), reason="They removed the bot from their server.")
            await ourGuild.get_member(int(key)).add_roles(ourGuild.get_role(733558248401272832), reason="They removed the bot from their server.")

            embed=discord.Embed(title="Plunge", color=0xfd5d5d)
            embed.set_thumbnail(url=logourl)
            embed.add_field(name="Verification Revoked", value="Hey, looks like you are no longer verified. The bot is no longer in the server you were verified in. Unfortunately, you have lost the User role in the Plunge Development server.\n\nYou can [invite the bot](https://discord.com/api/oauth2/authorize?client_id=732864657932681278&permissions=313408&scope=bot) to another server and use the `p.verify` command to get back the User role.", inline=False)

            await ourGuild.get_member(int(key)).send(embed=embed)

####################
# End Client Event Methods
####################

####################
# Start Bot Commands
####################

# Help Command
# p.help
# @client.command()
# async def help(ctx, setting = None):
#     if setting is None:
#         embed=discord.Embed(title="Plunge", description="List of Commands", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="General", value=f"`{prefix}drop` `{prefix}battle` `{prefix}help` `{prefix}feedback` `{prefix}invite` `{prefix}discord` `{prefix}verify` `{prefix}giveaway`", inline=False)
#         embed.add_field(name="Info", value=f"To get more help on a command or see the command's function, try: `p.help (command)`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "drop":
#         embed=discord.Embed(title="Plunge", description="Drop Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Gives you a random location to drop in Fortnite!", inline=False)
#         embed.add_field(name="Usage:", value="`p.drop`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "battle":
#         embed=discord.Embed(title="Plunge", description="Battle Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Starts a simulated battle royale for your server.", inline=False)
#         embed.add_field(name="Usage:", value="`p.battle`", inline=False)
#         embed.set_footer(text="p.stats • view your battle royale stats")
#         await ctx.send(embed=embed)
#     elif setting.lower() == "suggest":
#         embed=discord.Embed(title="Plunge", description="Suggest Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Sends your suggestion to the developers to review.", inline=False)
#         embed.add_field(name="Usage:", value="`p.suggest (your suggestion)`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "feedback":
#         embed=discord.Embed(title="Plunge", description="Feedback Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Sends your feedback for the developers to review.", inline=False)
#         embed.add_field(name="Usage:", value="`p.feedback (your feedback)`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "invite":
#         embed=discord.Embed(title="Plunge", description="Invite Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Gives you a link to invite this bot to your server!", inline=False)
#         embed.add_field(name="Usage:", value="`p.invite`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "discord":
#         embed=discord.Embed(title="Plunge", description="Discord Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Invites you to the bot's development server!", inline=False)
#         embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
#         embed.add_field(name="Aliases:", value="`p.server`, `p.join`, `p.support`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "server":
#         embed=discord.Embed(title="Plunge", description="Server Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Invites you to the bot's development server!", inline=False)
#         embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
#         embed.add_field(name="Aliases:", value="`p.discord`, `p.join`, `p.support`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "join":
#         embed=discord.Embed(title="Plunge", description="Join Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Invites you to the bot's development server!", inline=False)
#         embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
#         embed.add_field(name="Aliases:", value="`p.discord`, `p.server`, `p.support`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "support":
#         embed=discord.Embed(title="Plunge", description="Support Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Invites you to the bot's development server!", inline=False)
#         embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
#         embed.add_field(name="Aliases:", value="`p.discord`, `p.server`, `p.join`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "verify":
#         embed=discord.Embed(title="Plunge", description="Verify Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Verifies that you have the bot in your server, giving you the User Role in the Plunge Development server.", inline=False)
#         embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "giveaway":
#         embed=discord.Embed(title="Plunge", description="Giveaway Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Displays information about the current giveaway.", inline=False)
#         embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
#         await ctx.send(embed=embed)
#     else:
#         embed=discord.Embed(title="Plunge", description="Invalid Command Setting", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Try:", value=f"`p.help` or `p.help (command)`", inline=False)
#         await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    commands = f"`p.info` Gives instructions on how to use this bot\n`p.drop` Picks a random place for you to drop in Fortnite\n`p.battle` Starts a battle royale\n`p.shop` Displays the current shop items\n`p.profile` Shows your profile\n`p.inventory` Shows your inventory\n`p.chest` Opens a chest which contains gold and items\n`p.loadout` Pick your loadout items\n`p.perk` Pick a perk to equip\n`p.showcase` Pick your showcase items\n`p.title` Pick a title to equip\n`p.color` At level 100, change your profile color\n`p.leaderboard` Shows some of the best battle royale players\n`p.invite` Sends an invite link to have the bot join your own server\n`p.discord` Sends an invite link to join our discord server\n`p.verify` Gives you the user role in our discord server\n`p.giveaway` Gives information about the active giveaway"

    embed=discord.Embed(title="Plunge Help Page", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    embed.add_field(name="List of Commands", value=f"{commands}", inline=False)
    embed.add_field(name="Have feedback for us?", value=f"Use `p.feedback [your message]` to let us know what you would like to see in the future.", inline=False)
    await ctx.send(embed=embed)

# Command to let the user know where to drop using the drop command
# Can't decide on where to drop in Fortnite? It happens to us all, we  are riding in the battle bus with our maps open but no location marked.  
# Before we know it, we are getting kicked off the bus with little to no options to land. Luckily, Plunge Bot can help. With a simple command 
# "p.drop", Plunge will randomly select a location for you to drop in Fortnite, making your next drop stress free.
# p.drop
@client.command()
async def drop(ctx):
    # Call the add drop command to add to the counter
    await addDrop()

    # Removed: "The Shark"
    locations = ['Catty Corner', 'Frenzy Farm', 'Holly Hedges', 'Lazy Lake', 'Misty Meadows', 'Pleasant Park', 'Retail Row', 'Rickety Rig', 'Salty Springs', 'Steamy Stacks', 'Sweaty Sands', 'The Authority', 'The Fortilla', 'Risky Reels', 'The Yacht', 'Dirty Docks', 'Broken Castle', 'Pirate Barge']
    location = random.choice(locations)

    # locationurl = f'http://www.genplus.xyz/plunge/images/{location.replace(" ", "%20")}.png'
    locationurl = ''

    # Based on the location, set the image url
    if location == 'Catty Corner':
        locationurl = 'https://i.imgur.com/IN3zcJJ.png'
    elif location == 'Frenzy Farm':
        locationurl = 'https://i.imgur.com/c1pYdgs.png'
    elif location == 'Holly Hedges':
        locationurl = 'https://i.imgur.com/GX2A97E.png'
    elif location == 'Lazy Lake':
        locationurl = 'https://i.imgur.com/cNlKs5b.png'
    elif location == 'Misty Meadows':
        locationurl = 'https://i.imgur.com/QneWdkB.png'
    elif location == 'Pleasant Park':
        locationurl = 'https://i.imgur.com/cuIXiTM.png'
    elif location == 'Retail Row':
        locationurl = 'https://i.imgur.com/sIuNMV4.png'
    elif location == 'Rickety Rig':
        locationurl = 'https://i.imgur.com/tsJPpyn.png'
    elif location == 'Salty Springs':
        locationurl = 'https://i.imgur.com/KBFUFPN.png'
    elif location == 'Steamy Stacks':
        locationurl = 'https://i.imgur.com/QLPw5Bb.png'
    elif location == 'Sweaty Sands':
        locationurl = 'https://i.imgur.com/9eQBa08.png'
    elif location == 'The Authority':
        locationurl = 'https://i.imgur.com/JXWhuzJ.png'
    elif location == 'The Fortilla':
        locationurl = 'https://i.imgur.com/EOeio4u.png'
    elif location == 'Risky Reels':
        locationurl = 'https://i.imgur.com/K6Zwis8.png'
    elif location == 'The Yacht':
        locationurl = 'https://i.imgur.com/OLyro4T.png'
    elif location == 'Dirty Docks':
        locationurl = 'https://i.imgur.com/sPrr5rY.png'
    elif location == 'Broken Castle':
        locationurl = 'https://i.imgur.com/DocMZvk.png'
    elif location == 'Pirate Barge':
        locationurl = 'https://i.imgur.com/qpcf2bd.png'
    else:
        locationurl = ''

    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
    embed.add_field(name="You are dropping at:", value=location, inline=False)
    embed.set_thumbnail(url=logourl)
    embed.set_image(url=locationurl)
    await ctx.send(embed=embed)

# Command that simulates a battle royale
# TODO: add the random chest you can get in a game
# p.battle
@client.command()
async def battle(ctx):
    emoji = client.get_emoji(734656507194507275)

    # If the guild has an active battle royale... tell them.... Else start a battle royale
    if ctx.guild.id in list(activeBattles):
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle In Progress", value="There is already a battle in progress for this server, please wait until the current battle is complete", inline=False)
        await ctx.send(embed=embed)
    else:
        # add the guild to the active battles check
        activeBattles.append(ctx.guild.id)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 3 minutes!", inline=False)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('<:plunge:734656507194507275>')

        # await asyncio.sleep(60)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 2 minutes!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(60)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 1 minutes!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(30)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 30 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(10)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 20 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(10)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 10 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 9 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 8 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 7 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 6 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 5 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 4 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 3 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 2 seconds!", inline=False)
        # await msg.edit(embed=embed)

        await asyncio.sleep(1)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 1 seconds!", inline=False)
        await msg.edit(embed=embed)

        # Caches your message so you can get the reactions
        cache_msg = discord.utils.get(client.cached_messages, id = msg.id)
        
        # loops through the reactions
        for reaction in cache_msg.reactions:
            # if reaction is the plunge emoji...
            if str(reaction.emoji) == '<:plunge:734656507194507275>':
                # Grabs the users that used that reaction
                userObjects = await reaction.users().flatten()
                users = []

                # Makes a new list of just user.Id's
                for user in list(userObjects):
                    if user.id != 732864657932681278:
                        users.append(user.id)

                usersToAdd = 20 - len(users)

                if len(users) == 0:
                    # Battle wont start
                    await msg.delete(delay=None)
                    embed=discord.Embed(title="Plunge Error", color=0xfd5d5d)
                    embed.set_thumbnail(url=logourl)
                    embed.add_field(name="Not Enough Players", value=f"Make sure to react to the battle message to be entered in the battle royale.", inline=False)
                    msg = await ctx.send(embed=embed)
                    await msg.delete(delay=60)
                # If the list is larger than 20 start the battle, else
                elif len(users) > 20:
                    await msg.delete(delay=None)
                    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
                    embed.set_thumbnail(url=logourl)
                    embed.add_field(name="Battle In Progress...", value="Good Luck Everyone!", inline=False)
                    embed.set_footer(text=f"{len(users) - 1} Players")
                    await ctx.send(embed=embed)

                    # Pass the ctx and users list into the battleStart function
                    await battleStart(ctx, users)
                else:
                    await msg.delete(delay=None)
                    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
                    embed.set_thumbnail(url=logourl)
                    embed.add_field(name="Not Enough Players", value=f"Minimum players required: 20\n\nFilling the remaining {usersToAdd} slots with bots", inline=False)
                    await ctx.send(embed=embed)

                    await asyncio.sleep(5)
                    
                    # Add players to the list
                    i = 0
                    while i < usersToAdd:
                        users.append(i)
                        i += 1

                    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
                    embed.set_thumbnail(url=logourl)
                    embed.add_field(name="Battle In Progress...", value="Good Luck Everyone!", inline=False)
                    embed.set_footer(text=f"{len(users)} Players")
                    await ctx.send(embed=embed)

                    # Pass the ctx and users list into the battleStart function
                    await battleStart(ctx, users)

                
        # removes the guild from the active battles check (this comes last)
        activeBattles.remove(ctx.guild.id)

@client.command()
async def profile(ctx, args = None):
    # if no parameters, display the authors profile
    if args == None:
        await displayProfile(ctx, ctx.author.id)
    # else, display the passed in user
    else:
        # Format the mentioned user for easy lookup
        args = args.translate(dict.fromkeys(map(ord, '!@<>')))

        # Get the user object
        user = client.get_user(int(args))

        # If user is not None
        if user is not None:
            # Display passed in user
            await displayProfile(ctx, user.id)
        else:
            print("User not found. Profile Command.")

# Displays the users profile
async def displayProfile(ctx, userId):
    # Get the user
    user = client.get_user(userId)

    # Fetch the user from the list
    userProfile = await fetchUserProfile(userId)

    if userProfile is True:
        await ctx.send(f"{user.name}#{user.discriminator} has not yet played in a Battle Royale... Creating User...")
    else:
        # Get the users profile info
        name = userProfile["name"]

        titleId = userProfile["title"]
        title = await fetchTitleName(titleId)

        showcase1Id = userProfile["showcase1"]
        showcase2Id = userProfile["showcase2"]
        showcase3Id = userProfile["showcase3"]
        showcase1 = await fetchItem(showcase1Id)
        showcase2 = await fetchItem(showcase2Id)
        showcase3 = await fetchItem(showcase3Id)
        
        showcase1Emoji = client.get_emoji(showcase1["emojiId"])
        showcase1Name = showcase1["name"]

        showcase2Emoji = client.get_emoji(showcase2["emojiId"])
        showcase2Name = showcase2["name"]

        showcase3Emoji = client.get_emoji(showcase3["emojiId"])
        showcase3Name = showcase3["name"]

        wins = userProfile["stats"]["wins"]
        kills = userProfile["stats"]["kills"]
        deaths = userProfile["stats"]["deaths"]
        kd = await calcKD(kills, deaths)
        level = math.floor(userProfile["stats"]["totalExp"]/100)
        gamesPlayed = deaths + wins
        winPerc = await calcWinPerc(wins, gamesPlayed)

        slot1Id = userProfile["loadout"]["slot1"]
        slot2Id = userProfile["loadout"]["slot2"]
        slot3Id = userProfile["loadout"]["slot3"]
        slot4Id = userProfile["loadout"]["slot4"]
        perkId = userProfile["loadout"]["perk"]
        slot1 = await fetchItem(slot1Id)
        slot2 = await fetchItem(slot2Id)
        slot3 = await fetchItem(slot3Id)
        slot4 = await fetchItem(slot4Id)
        perk = await fetchItem(perkId)

        slot1Name = slot1["name"]
        slot1Emoji = client.get_emoji(slot1["emojiId"])
        slot1Rarity = await getRarity(slot1["rarityId"])
        slot1Threat = slot1Rarity["threat"]
        threat1 = slot1Threat
        if slot1Threat == 0:
            slot1Threat = ""
        else:
            slot1Threat = f"`+{slot1Threat * 10} threat`"

        slot2Name = slot2["name"]
        slot2Emoji = client.get_emoji(slot2["emojiId"])
        slot2Rarity = await getRarity(slot2["rarityId"])
        slot2Threat = slot2Rarity["threat"]
        threat2 = slot2Threat
        if slot2Threat == 0:
            slot2Threat = ""
        else:
            slot2Threat = f"`+{slot2Threat * 10} threat`"

        slot3Name = slot3["name"]
        slot3Emoji = client.get_emoji(slot3["emojiId"])
        slot3Rarity = await getRarity(slot3["rarityId"])
        slot3Threat = slot3Rarity["threat"]
        threat3 = slot3Threat
        if slot3Threat == 0:
            slot3Threat = ""
        else:
            slot3Threat = f"`+{slot3Threat * 10} threat`"

        slot4Name = slot4["name"]
        slot4Emoji = client.get_emoji(slot4["emojiId"])
        slot4Rarity = await getRarity(slot4["rarityId"])
        slot4Threat = slot4Rarity["threat"]
        threat4 = slot4Threat
        if slot4Threat == 0:
            slot4Threat = ""
        else:
            slot4Threat = f"`+{slot4Threat * 10} threat`"

        perkName = perk["name"]
        perkEmoji = client.get_emoji(perk["emojiId"])
        perkBonus = await getPerkBonus(perkId)

        totalWeapons = len(userProfile["inventory"]["weapons"])
        totalPerks = len(userProfile["inventory"]["perks"])
        totalUmbrellas = len(userProfile["inventory"]["umbrellas"])
        totalTitles = len(userProfile["inventory"]["titles"])
        totalChests = userProfile["inventory"]["chests"]
        totalPickaxes = len(userProfile["inventory"]["pickaxes"])
        inventorySize = totalWeapons + totalPerks + totalUmbrellas + totalTitles + totalChests + totalPickaxes

        gold = userProfile["inventory"]["gold"]
        gems = userProfile["inventory"]["gems"]
        goldEmoji = client.get_emoji(736439923095109723)
        gemEmoji = client.get_emoji(736451870016405655)

        totalThreat = threat1 + threat2 + threat3 + threat4

        if perkId == 1000:
            totalThreat = totalThreat + 2

        # Sets Color based off level
        if level < 10:
            color = 2433568
        elif level > 9 and level < 20:
            color = 14885182
        elif level > 19 and level < 30:
            color = 16407354
        elif level > 29 and level < 40:
            color = 16764160
        elif level > 39 and level < 50:
            color = 31530
        elif level > 49 and level < 60:
            color = 37347
        elif level > 59 and level < 70:
            color = 8476113
        elif level > 69 and level < 80:
            color = 14702034
        elif level > 79 and level < 90:
            color = 6363698
        elif level > 89 and level < 100:
            color = 14673631
        elif level >= 100:
            color = int(userProfile["color"], 16)

        embed=discord.Embed(title=f"{name}\'s Profile", color=color)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name=f"Level: {level}\nThreat: {totalThreat * 10}", value=f"{title} {name}#{user.discriminator}\n\n**Gold:** {gold} {goldEmoji}\n**Gems:** {gems} {gemEmoji}\n\n ", inline=False),
        embed.add_field(name=f"__Stats__", value=f"Wins: {wins}\nKills: {kills}\nDeaths: {deaths}\nK/D Ratio: {kd}\nGames Played: {gamesPlayed}\nWin Percent: {winPerc}%\n\n", inline=True)
        embed.add_field(name=f"__Showcase__", value=f"{showcase1Emoji} {showcase1Name}\n{showcase2Emoji} {showcase2Name}\n{showcase3Emoji} {showcase3Name}", inline=True)
        embed.add_field(name=f"__Loadout__", value=f"**1.** {slot1Emoji} {slot1Name} {slot1Threat}\n**2.** {slot2Emoji} {slot2Name} {slot2Threat}\n**3.** {slot3Emoji} {slot3Name} {slot3Threat}\n**4.** {slot4Emoji} {slot4Name} {slot4Threat}\n", inline=False)
        embed.add_field(name=f"__Perk__", value=f"{perkEmoji} {perkName} {perkBonus}", inline=False)        
        embed.set_footer(text=f"Inventory ({inventorySize})")
        await ctx.send(embed=embed)

# Fetches the user.. if not found, creates a new user
async def fetchUserProfile(userId):
    # Opens the users.json file and reads it
    with open('users.json', 'r') as f:
        userData = json.load(f)

    # Checks if userId is in the userData list
    if str(userId) in list(userData.keys()):
        return userData[str(userId)]
    # else create new user
    else:
        # Creates a user
        await createNewUser(userId)
        return True

# Fetches The Title Name
async def fetchTitleName(titleId):
    # Opens the titles.json
    with open('titles.json', 'r') as f:
        titleData = json.load(f)

    if str(titleId) in list(titleData.keys()):
        title = titleData[str(titleId)]["title"]
        
        if title != "":
            title = "`[" + title + "]`"

        return title
    else:
        print("Title name not found. fetchTitleName error.")

# Fetchs an item based on its ID
async def fetchItem(itemId):
    if itemId < 1000:
        with open('weapons.json', 'r') as f:
            weaponData = json.load(f)

        if str(itemId) in list(weaponData.keys()):
            return weaponData[str(itemId)]
        else:
            print("Weapon not found. fetchItem error.")
    elif itemId > 999 and itemId < 2000:
        with open('perks.json', 'r') as f:
            perkData = json.load(f)

        if str(itemId) in list(perkData.keys()):
            return perkData[str(itemId)]
        else:
            print("Perk not found. fetchItem error.")
    elif itemId > 1999 and itemId < 3000:
        with open('umbrellas.json', 'r') as f:
            umbrellaData = json.load(f)

        if str(itemId) in list(umbrellaData.keys()):
            return umbrellaData[str(itemId)]
        else:
            print("Umbrella not found. fetchItem error.")
    elif itemId > 2999 and itemId < 4000:
        with open('titles.json', 'r') as f:
            titleData = json.load(f)

        if str(itemId) in list(titleData.keys()):
            return titleData[str(itemId)]
        else:
            print("Title not found. fetchItem error.")
    elif itemId > 3999 and itemId < 5000:
        with open('chests.json', 'r') as f:
            chestData = json.load(f)

        if str(itemId) in list(chestData.keys()):
            return chestData[str(itemId)]
        else:
            print("Chest not found. fetchItem error.")
    else:
        with open('pickaxes.json', 'r') as f:
            pickData = json.load(f)

        if str(itemId) in list(pickData.keys()):
            return pickData[str(itemId)]
        else:
            print("Pick not found. fetchItem error.")

# Create a new user in the users.json
async def createNewUser(userId):
    # Opens the users.json file and read it
    with open('users.json', 'r') as f:
        userData = json.load(f)
    
    # If user is not in the list, add a new user
    if str(userId) not in list(userData.keys()):
        # Gets the users name
        user = client.get_user(userId)

        stats = {
            "wins": 0,
            "kills": 0,
            "deaths": 0,
            "totalExp": 0
        }
        matchStats = {
            "placement": 0,
            "killsEarned": 0,
            "goldEarned": 0,
            "expEarned": 0,
            "itemsEarned": []
        }
        loadout = {
            "slot1": 999,
            "slot2": 999,
            "slot3": 999,
            "slot4": 999,
            "perk": 1999
        }
        inventory = {
            "weapons": [],
            "perks": [],
            "umbrellas": [],
            "titles": [],
            "chests": [],
            "pickaxes": [5000],
            "gold": 250,
            "gems": 0
        }

        userData[str(userId)] = {
            "name": user.name,
            "title": 3999,
            "color": "0c0d0c",
            "showcase1": 999,
            "showcase2": 999,
            "showcase3": 999,
            "stats": stats,
            "matchStats": matchStats,
            "loadout": loadout,
            "inventory": inventory
        }
    
        with open('users.json', 'w') as f:
            json.dump(userData, f, indent=4)
    else:
        # print("User already created. createUser Error.")
        return

# Get the users kill death ratio
async def calcKD(kills, deaths):
    if kills > 0 and deaths > 0:
        kd = kills / deaths
    elif deaths == 0:
        kd = kills
    else:
        kd = 0

    return round(kd, 2)

# Get the users win percentage
async def calcWinPerc(wins, gamesPlayed):
    if wins > 0 and gamesPlayed > 0:
        winperc = wins / gamesPlayed * 100
    else:
        winperc = 0

    return round(winperc)

# Gets the bonus of the perk you have equipped
async def getPerkBonus(perkId):
    if perkId == 1999:
        return ""
    elif perkId == 1000:
        return "`+20 Threat`"
    elif perkId == 1001:
        return "`+10% Gold`"
    elif perkId == 1002:
        return "`+10% Exp`"

# Command that gets the users inventory
@client.command()
async def inventory(ctx):
    # Fetch the user from the list
    userProfile = await fetchUserProfile(ctx.author.id)

    if userProfile is True:
        await ctx.send(f"{ctx.author.name}#{ctx.author.discriminator} does not have an inventory yet... Creating User...")
    else:
        # Get the users profile info
        name = userProfile["name"]

        titleId = userProfile["title"]
        title = await fetchTitleName(titleId)

        weaponList = userProfile["inventory"]["weapons"]
        perkList = userProfile["inventory"]["perks"]
        umbrellaList = userProfile["inventory"]["umbrellas"]
        titleList = userProfile["inventory"]["titles"]
        chests = userProfile["inventory"]["chests"]
        pickaxeList = userProfile["inventory"]["pickaxes"]
        gold = userProfile["inventory"]["gold"]
        gems = userProfile["inventory"]["gems"]

        # returns a string based on the weapons in the list
        weapons = fetchWeapons(weaponList)
        perks = fetchPerks(perkList)
        umbrellas = fetchUmbrellas(umbrellaList)
        titles = fetchTitles(titleList)
        pickaxes = fetchPickaxes(pickaxeList)

        embed=discord.Embed(title=f"{title} {name}\'s Inventory", color=0xfd5d5d)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name=f"__Weapons__", value=f"{weapons}", inline=False)
        embed.add_field(name=f"__Pickaxes__", value=f"{pickaxes}", inline=False)
        embed.add_field(name=f"__Perks__", value=f"{perks}", inline=False)
        embed.add_field(name=f"__Umbrellas__", value=f"{umbrellas}", inline=False)
        embed.add_field(name=f"__Titles__", value=f"{titles}\n\n**Gold:** {gold}\n**Gems:** {gems}\n**Chests:** {chests}", inline=False)
        await ctx.send(embed=embed)

# Takes a list of weapons and returns a formated string
def fetchWeapons(weapons):
    value = ''

    with open('weapons.json', 'r') as f:
        data = json.load(f)

    with open('rarity.json', 'r') as r:
        rarity = json.load(r)

    for weaponId in weapons:
        emojiId = data[str(weaponId)]['emojiId']
        emoji = client.get_emoji(emojiId)
        name = data[str(weaponId)]['name']
        rarityId = data[str(weaponId)]['rarityId']
        threat = rarity[str(rarityId)]['threat'] * 10

        value += f'{emoji} {name} `+{threat} threat`\n'
    
    if value == '':
        return 'None'
    else:
        return value


# Takes a list of perks and returns a formated string
def fetchPerks(perks):
    value = ''

    with open('perks.json', 'r') as f:
        data = json.load(f)
    
    for perkId in perks:
        emojiId = data[str(perkId)]['emojiId']
        emoji = client.get_emoji(emojiId)
        name = data[str(perkId)]['name']

        if perkId == 1000:
            bonus = f'`+20 threat`'
        elif perkId == 1001:
            bonus = f'`+10% gold`'
        elif perkId == 1002:
            bonus = f'`+10% exp`'

        value += f'{emoji} {name} {bonus}\n'

    if value == '':
        return 'None'
    else:
        return value

# Takes a list of umbrellas and returns a formated string
# TODO: update the umbrella emoji's
def fetchUmbrellas(umbrellas):
    value = ''

    with open('umbrellas.json', 'r') as f:
        data = json.load(f)

    for umbrellaId in umbrellas:
        emojiId = data[str(umbrellaId)]['emojiId']
        # Get emoji here
        name = data[str(umbrellaId)]['name']

        value += f'{name}\n'

    if value == '':
        return 'None'
    else:
        return value

# Takes a list of titles and returns a formated string
def fetchTitles(titles):
    value = ''

    with open('titles.json', 'r') as f:
        data = json.load(f)

    for titleId in titles:
        name = data[str(titleId)]['title']

        value += f'`{name}` '

    if value == '':
        return 'None'
    else:
        return value


# Takes a list of pickaxes and returns a formated string
def fetchPickaxes(pickaxes):
    value = ''

    with open('pickaxes.json', 'r') as f:
        data = json.load(f)

    for pickaxeId in pickaxes:
        emojiId = data[str(pickaxeId)]['emojiId']
        # Get the emoji for the pickaxe once added
        name = data[str(pickaxeId)]['name']

        value += f'{name}\n'

    if value == '':
        return 'None'
    else:
        return value


####################
# End Bot Commands
####################

####################
# Start Mod Commands
####################

@client.command()
async def updates(ctx):
    if isDev(ctx.author.id):
        updates = client.get_channel(733858209046986863) # Gets #updates channel in Plunge Development
        embed=discord.Embed(title="Plunge (BETA v1.0.0)", description="Bot Released with features", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Added", value="`p.drop` - Gives a random location to drop in Fortnite!\n`p.battle` - Starts a simulated battle royale for your server.\n`p.help` - Shows a list of all commands\n", inline=False)
        await updates.send(embed=embed)
    else:
        # If people are trying to use this command and are not dev, tell them its an unknown command
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Command Not Found", value="Try `p.help` for a list of all commands.", inline=False)
        await ctx.send(embed=embed)

####################
# End Mod Commands
####################

# Command to invite the bot to your server
# p.invite
@client.command()
async def invite(ctx):
    embed=discord.Embed(title="Plunge Invite Link", description="If you'd like to invite this bot to your own server, [click here](https://discord.com/api/oauth2/authorize?client_id=732864657932681278&permissions=313408&scope=bot) for an invite", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    await ctx.send(embed=embed)

# Command to see how many servers the bot is in
# p.servers, p.botservers, p.botserver
@client.command(aliases=['botservers', 'botserver'])
async def servers(ctx):
    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    embed.add_field(name="Plunge is in:", value=f"{str(len(client.guilds))} servers", inline=False)
    for guild in client.guilds:
        print(guild.name)
    await ctx.send(embed=embed)

# Command to verify they added the bot to the server
# p.verify
@client.command()
@commands.has_guild_permissions(manage_guild=True)
async def verify(ctx):
    # print(ctx.guild.get_member(ctx.author.id).guild_permissions) # This returns the value of your permissions Elyxirs -> value=2147483647
    ourGuild = client.get_guild(733551377611096195)

    users = []

    for user in ourGuild.members:
        users.append(user.id)

    if (ctx.author.id in users):
        await ourGuild.get_member(ctx.author.id).add_roles(ourGuild.get_role(733559654210207885), reason="Used the verify command")
        await ourGuild.get_member(ctx.author.id).remove_roles(ourGuild.get_role(733558248401272832), reason="Used the verify command")

        with open('userInfo.json', 'r') as f:
            userInfo = json.load(f)

        keys = await getKeys(userInfo.items())

        # if the user is already verified tell them... else verify them
        if (str(ctx.author.id) in keys):
            embed=discord.Embed(title="Plunge", color=0xfd5d5d)
            embed.set_thumbnail(url=logourl)
            embed.add_field(name="Already Verified", value=f"{ctx.author.mention}, you are already verified and have the User role in the Plunge Development server.\n\nHead over to the Plunge Development server to see!", inline=False)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Plunge", color=0xfd5d5d)
            embed.set_thumbnail(url=logourl)
            embed.add_field(name=f"Verified", value=f"{ctx.author.mention}, you are now verified and have the User role in the Plunge Development server.\n\nHead over to the Plunge Development server to see!", inline=False)
            await ctx.send(embed=embed)

        # Update the users info in the userInfo.json anyway
        userInfo[str(ctx.author.id)] = str(ctx.guild.id)

        with open('userInfo.json', 'w') as f:
            json.dump(userInfo, f, indent=4)
    else:
        embed=discord.Embed(title="Plunge", description=f"{ctx.author.mention}, you are not in the Plunge Development server. [Click here](https://discord.gg/mjr6nUU) to join!\n\nAfter you are in the Plunge Development server, run the `p.verify` command again to get your role.", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        await ctx.send(embed=embed)
    
# Command to join the developer discord
# p.server, p.join, p.discord
@client.command(aliases=['join', 'discord'])
async def server(ctx):
    embed=discord.Embed(title="Plunge Development", description="To join our discord, [click here](https://discord.gg/mjr6nUU) for an invite", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    await ctx.send(embed=embed)

# Command that leaves a suggestion for the bot
# p.suggest (suggestion)  p.feedback (feedback)
@client.command(aliases=['feedback'])
async def suggest(ctx, *, suggestion = None):
    if suggestion is None:
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Invalid Command Format", value="Try: `p.suggest (suggestion)` or `p.feedback (feedback)`", inline=False)
        await ctx.send(embed=embed)
    else:
        # On Suggestion command, ping private discord channel 733592146308890675 with the details
        channelId = client.get_channel(733592146308890675) #suggestions in Plunge Development

        # Response to user's message
        reply=discord.Embed(title="Plunge", color=0xfd5d5d)
        reply.set_thumbnail(url=logourl)
        reply.add_field(name=f"Sent", value=f"Thanks for your submission!", inline=False)
        reply.set_footer(text="p.invite • Invites this bot to your server")
        await ctx.send(embed=reply)
        
        # Suggestion added to suggestions channel
        suggested=discord.Embed(title="Plunge", description=f"Submitted by {ctx.author.name}#{ctx.author.discriminator}", color=0xfd5d5d)
        suggested.set_thumbnail(url=ctx.author.avatar_url)
        suggested.add_field(name="Suggestion / Feedback", value=suggestion, inline=False)
        await channelId.send(embed=suggested)

# Command that gives the user information about the giveaway
# p.giveaway 
@client.command()
async def giveaway(ctx):
    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    embed.add_field(name="Giveaway Information", value="Giving away `3x Discord Nitro` in the Plunge Development server.\n", inline=False)
    embed.add_field(name="To Qualify", value="1. Join the [Plunge Development server](https://discord.gg/mjr6nUU) and be sure to read the server rules.\n\n2. You need the Plunge bot in a server you own or are administrator of. Use `p.invite` or invite the bot by clicking [here](https://discord.com/api/oauth2/authorize?client_id=732864657932681278&permissions=313408&scope=bot).\n\n3. In your server, run the `p.verify` command. This will give you the User role in the Plunge Development server.\n\n4. Head back over to the giveaways channel in the [Plunge Development server](https://discord.gg/mjr6nUU) and enter the giveaway.", inline=False)
    embed.add_field(name="Note", value="If the bot is removed from the server where you used `p.verify` you will lose the User role in the Plunge Development server.", inline=False)
    await ctx.send(embed=embed)

#####################################################################
#####################################################################
##                                                                 ##
##                      Battle Royale                              ##
##                                                                 ##
#####################################################################
#####################################################################


# TODO: Match summary (kills, xp, gold, items if any)

# TODO: Add a shop with items
######### ITEMS/SHOP ITEMS ##########
#  TIERS: Common - 0, Uncommon - 1, Rare - 2, Epic - 3, Legendary - 4, POSSIBLY MYTHIC - 5 (NOT RELEASED)
#  
#  Weapon Categories: Shotgun, Smg, Ar, Sniper
#
#  Perks: Extra gold at end of game, Extra Threat for the game, Extra Experience per game
#
# TODO: Add special Umbrella when you win


####################
# Start Battle commands
####################

# Battle function
async def battleStart(ctx, users):
    # TODO: More custom messages... more related to fortnite I guess...

    # weapons = ['a Pistol', 'a Pickaxe', 'an Assault Rifle', 'an Auto Rifle', 'a Sniper Rifle', 'a Paintball Gun', 'a Rock', 'an Arrow', 'a Blow Dart Gun', 'a Rocket Launcher', 
    # 'a Grenade', 'a Grenade Launcher', 'a Shotgun', 'Hand to Hand Combat', 'a Submachine Gun', 'a Light Machine Gun', 'a Stick', 'an Eye Poke', 'a Karate Chop']

    # eliminations = ['eliminated', 'destroyed', 'annihilated', 'obliterated', 'got rid of', 'beamed', 'ended', 'finished off', 'murdered', 'killed', 'erased']

    funny = ['took an arrow to the knee', 'forgot they can\'t fly', 'starved to death', 'was eliminated for cheating', 
    'went off the deep end', 'drowned', 'fell', 'died', 'mysteriously disappeared', 'fled from battle', 'was pecked to death by a bird',
    'sunk in quick sand', 'was trampled by rhinos', 'died from the unknown', 'fell in the void', 'got a deadly infection', 'was squashed',
    'was poisoned', 'choked on a raisin', 'didn\'t make it', 'hyperventilated and died', 'was eliminated for tax evasion']

    # Adds to the battle counter
    await addBattle()

    # Checks the users in the list... removes Plunge Bot
    for userId in list(users):
        if userId > 20:
            await createNewUser(userId)

    # TODO: Fix whatever mess this is
    newList = users
    totalPlayers = len(list(newList))
    PlayersForXp = list(newList)
    
    while len(newList) > 1:
        with open('users.json', 'r') as f:
            data = json.load(f)

        userId1 = random.choice(users)
        userId2 = random.choice(users)

        battleRange = random.randint(1, 150)

        await asyncio.sleep(random.randint(4,8)) # Randomly select the message delay between 4-8 numbers

        # Prevents them from randomly dying without getting eleminated when its in the final 5
        if len(newList) <= 5:
            i = 0
            while i < 3 and userId1 == userId2:
                userId1 = random.choice(newList)
                userId2 = random.choice(newList)
                i+=1

        if userId1 == userId2:

            if userId1 > 20:
                user1 = client.get_user(userId1)
                if user1 is not None:
                    user1Name = f'{user1.mention}'
                else:
                    print('but something went wrong 1260')
                    user1Name = data[str(userId1)]['name']
            else:
                user1Name = data[str(userId1)]['name']

            await addDeath(userId1, len(newList))
            embed=discord.Embed()
            embed.add_field(name="Elimination", value=f'**{user1Name}** {random.choice(funny)}', inline=False)
            embed.set_footer(text=f"{len(newList) - 1} Remaining")
            msg = await ctx.send(embed=embed)
            await msg.delete(delay=120)

            # Updates the list by removing the user that got eliminated
            newList.remove(userId2)
        else:
            # Call the method that calculates who wins the battle (returns the elimination message)
            elimMessage = userBattle(userId1, userId2, battleRange)
            addKill(elimMessage[1])
            await addDeath(elimMessage[2], len(newList))
            embed=discord.Embed()
            embed.add_field(name="Elimination", value=f'{elimMessage[0]}', inline=False)
            embed.set_footer(text=f"{len(newList) - 1} Remaining")
            msg = await ctx.send(embed=embed)
            await msg.delete(delay=120)
            
            # Updates the list by removing the user that got eliminated
            newList.remove(elimMessage[2])

    await asyncio.sleep(3)


    winner = newList[0]

    await addWin(winner)

    # Get the winners name
    if winner > 20:
        winnerUser = client.get_user(winner)
        winnerName = f'{winnerUser.mention}'
    else:
        winnerName = data[str(winner)]['name']
    
    winnerKills = getGameKills(winner)

    #TODO: Put crown for thumbnail url in embed message. add other emojis for victory

    embed=discord.Embed(title="Battle Royale Victory", description=f"The winner of {ctx.guild.name}\'s Battle Royale is **{winnerName}**\n\n**{winnerName}** had {winnerKills} kills", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    embed.set_footer(text=f"{totalPlayers} players participated")
    await ctx.send(embed=embed)

    for userId in PlayersForXp:
        await resetMatchStats(userId)


def userBattle(userId1, userId2, battleRange):
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    with open('ranges.json', 'r') as f:
        ranges = json.load(f)

    # Variables
    eliminations = ['eliminated', 'destroyed', 'annihilated', 'obliterated', 'got rid of', 'beamed', 'ended', 'finished off', 'murdered', 'killed', 'erased']

    # Get user1's weapon loadout
    user1Loadout = []
    user1Loadout.append(users[str(userId1)]['loadout']['slot1'])
    user1Loadout.append(users[str(userId1)]['loadout']['slot2'])
    user1Loadout.append(users[str(userId1)]['loadout']['slot3'])
    user1Loadout.append(users[str(userId1)]['loadout']['slot4'])

    # Get desired weapon for user 1
    user1Weapon = desiredWeapon(user1Loadout, battleRange)

    # Get weapon emoji
    user1WeaponEmojiId = user1Weapon['emojiId']
    user1WeaponEmoji = client.get_emoji(user1WeaponEmojiId)

    # Get weapon name
    user1WeaponName = user1Weapon['name']

    # Get user1's weapon ranges
    user1MinRange = ranges[str(user1Weapon['rangeId'])]['minRange']
    user1MaxRange = ranges[str(user1Weapon['rangeId'])]['maxRange']
    user1RangeBonusThreat = 0

    # Get user1's bonus threat if any
    if battleRange <= user1MaxRange and battleRange >= user1MinRange:
        user1RangeBonusThreat = ranges[str(user1Weapon['rangeId'])]['bonusThreat']

    # Get user1's loadout threat
    user1LoadoutThreat = getUsersThreat(users[str(userId1)])

    # Get user2's weapon loadout
    user2Loadout = []
    user2Loadout.append(users[str(userId2)]['loadout']['slot1'])
    user2Loadout.append(users[str(userId2)]['loadout']['slot2'])
    user2Loadout.append(users[str(userId2)]['loadout']['slot3'])
    user2Loadout.append(users[str(userId2)]['loadout']['slot4'])

    # Get desired weapon for user 2
    user2Weapon = desiredWeapon(user2Loadout, battleRange)

    # Get weapon emoji
    user2WeaponEmojiId = user2Weapon['emojiId']
    user2WeaponEmoji = client.get_emoji(user2WeaponEmojiId)

    # Get weapon name
    user2WeaponName = user2Weapon['name']

    # Get user2's weapon ranges
    user2MinRange = ranges[str(user2Weapon['rangeId'])]['minRange']
    user2MaxRange = ranges[str(user2Weapon['rangeId'])]['maxRange']
    user2RangeBonusThreat = 0

    # Get user2's bonus threat if any
    if battleRange <= user2MaxRange and battleRange >= user2MinRange:
        user2RangeBonusThreat = ranges[str(user2Weapon['rangeId'])]['bonusThreat']

    # Get user2's ladout threat
    user2LoadoutThreat = getUsersThreat(users[str(userId2)])

    # Get user2's total threat
    user2TotalThreat = user2RangeBonusThreat + user2LoadoutThreat

    # Get user1's total threat
    user1TotalThreat = user1RangeBonusThreat + user1LoadoutThreat

    # Get the odds per user
    if user1TotalThreat > user2TotalThreat:
        difference = user1TotalThreat - user2TotalThreat
        user1odds = (100 + difference) / 2
        user2odds = (100 - difference) / 2
    elif user1TotalThreat == user2TotalThreat:
        user1odds = 50
        user2odds = 50
    else:
        difference = user2TotalThreat - user1TotalThreat
        user2odds = (100 + difference) / 2
        user1odds = (100 - difference) / 2

    weightedList = [userId1, userId2]

    winningId = random.choices(weightedList, weights=(user1odds, user2odds))
    
    # Fetch the users names to use
    if userId1 > 20:
        user1 = client.get_user(userId1)
        user1Name = f'{user1.mention}'
    else:
        user1Name = users[str(userId1)]['name']

    if userId2 > 20:
        user2 = client.get_user(userId2)
        user2Name = f'{user2.mention}'
    else:
        user2Name = users[str(userId2)]['name']

    if winningId[0] == userId1:
        # User1 wins
        return f'**{user1Name}** {random.choice(eliminations)} **{user2Name}** with {user1WeaponEmoji} {user1WeaponName} (*{battleRange}m*)', userId1, userId2
    else:
        # User2 wins
        return f'**{user2Name}** {random.choice(eliminations)} **{user1Name}** with {user2WeaponEmoji} {user2WeaponName} (*{battleRange}m*)', userId2, userId1

# Gets a users total threat
def getUsersThreat(user):
    with open('weapons.json', 'r') as f:
        weapons = json.load(f)
    
    with open('rarity.json', 'r') as f:
        rarity = json.load(f)

    totalThreat = 0

    # Get users loadout
    userLoadout = []
    userLoadout.append(user['loadout']['slot1'])
    userLoadout.append(user['loadout']['slot2'])
    userLoadout.append(user['loadout']['slot3'])
    userLoadout.append(user['loadout']['slot4'])

    for weaponId in userLoadout:
        totalThreat += rarity[str(weapons[str(weaponId)]['rarityId'])]['threat']
    
    if user['loadout']['perk'] == 1000:
        totalThreat += 2

    return totalThreat

# Gets the desired weapon for the user to use for the engagement
def desiredWeapon(weaponIdList, battleRange):
    with open('weapons.json', 'r') as f:
        weapons = json.load(f)
    
    with open('ranges.json', 'r') as f:
        ranges = json.load(f)

    # average list
    averageRanges = []

    # get the average of the ranges and add them to the list
    for weaponId in weaponIdList:
        if weaponId != 999:
            rangeId = weapons[str(weaponId)]['rangeId']

            averageRange = ranges[str(rangeId)]['averageRange']

            averageRanges.append(averageRange)
            

    # weaponRange to use
    rangeToUse = closest(averageRanges, battleRange)

    for weaponId in weaponIdList:
        rangeId = weapons[str(weaponId)]['rangeId']
        
        if rangeToUse == ranges[str(rangeId)]['averageRange']:
            return weapons[str(weaponId)]


def closest(lst, distance):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-distance))]

# Method that gets the current Game Kills
def getGameKills(userId):
    with open('users.json', 'r') as f:
        data = json.load(f)

    kills = data[str(userId)]['matchStats']['killsEarned']

    return kills

# Method that updates your stats at the end of the game
async def resetMatchStats(userId):
    with open('users.json', 'r') as f:
        data = json.load(f)

    data[str(userId)]['matchStats']['placement'] = 0
    data[str(userId)]['matchStats']['killsEarned'] = 0
    data[str(userId)]['matchStats']['goldEarned'] = 0
    data[str(userId)]['matchStats']['expEarned'] = 0
    data[str(userId)]['matchStats']['itemsEarned'] = []

    with open('users.json', 'w') as f:
        json.dump(data, f, indent=4)

# Method that updates the users kills
def addKill(userId):
    with open('users.json', 'r') as f:
        data = json.load(f)

    data[str(userId)]['stats']['kills'] += 1
    data[str(userId)]['matchStats']['killsEarned'] += 1
    data[str(userId)]['stats']['totalExp'] += 1
    data[str(userId)]['matchStats']['expEarned'] += 1
    data[str(userId)]['inventory']['gold'] += 10
    data[str(userId)]['matchStats']['goldEarned'] += 10

    with open('users.json', 'w') as f:
        json.dump(data, f, indent=4)

# Method that updates the users wins
async def addWin(userId):
    with open('users.json', 'r') as f:
        data = json.load(f)

    data[str(userId)]['stats']['wins'] += 1
    data[str(userId)]['matchStats']['placement'] = 1
    data[str(userId)]['stats']['totalExp'] += 10
    data[str(userId)]['matchStats']['expEarned'] += 10
    data[str(userId)]['inventory']['gold'] += 150
    data[str(userId)]['matchStats']['goldEarned'] += 150

    with open('users.json', 'w') as f:
        json.dump(data, f, indent=4)

# Method that updates the users deaths
async def addDeath(userId, placement):
    with open('users.json', 'r') as f:
        data = json.load(f)

    data[str(userId)]['matchStats']['placement'] = placement
    data[str(userId)]['stats']['deaths'] += 1
    data[str(userId)]['stats']['totalExp'] += 5
    data[str(userId)]['matchStats']['expEarned'] += 5
    data[str(userId)]['inventory']['gold'] += 50
    data[str(userId)]['matchStats']['goldEarned'] += 50

    with open('users.json', 'w') as f:
        json.dump(data, f, indent=4)

####################
# End Battle commands
####################

####################
# Start Error Handling
####################

# Command Not Found Error Handler
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Command Not Found", value="Try `p.help` for a list of all commands.", inline=False)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        pass
    else:
        raise error

# On verify command error
@verify.error
async def verify_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Missing Permissions", value="To verify for the User role in the Plunge Development server, you need to be an administrator or have permissions to manage the server you are currently in.", inline=False)
        embed.add_field(name="To Verify", value="[Invite the bot](https://discord.com/api/oauth2/authorize?client_id=732864657932681278&permissions=313408&scope=bot) to a server you own or are administrator of and use `p.verify` there.", inline=False)
        await ctx.send(embed=embed)

####################
# End Error Handling
####################

# Runs the bot
client.run(data['token'])