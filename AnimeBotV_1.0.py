import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from AnimeBotV1 import animeCommands


Client = discord.Client()
bot = commands.Bot(command_prefix="%")

# sets up the chat filter list from the chat_filter.txt file
def update_filter():
    chat_filter = []
    filter_file = open("chat_filter.txt", "r")
    for line in filter_file.readlines():
        chat_filter.append(line.replace("\n", ''))
    filter_file.close()
    return chat_filter

def inRoles(checkRole, user):
    for role in user.roles:
        if role.id == checkRole:
            return True

def validFilter(term):
    for element in filter_bans:
        if element in term:
            return False
    return True

def parseHelp():
    commandsString = ""
    commands_file = open("server_commands_help.txt", "r")
    for line in commands_file:
        commandsString += line
    return commandsString

chat_filter = update_filter()

bypass_list = ["511625958764314653"]
chat_banned_roles = ["511630140065972226"]
polls = []
hashes = {":thumbsup1:511780305833558026": hash(":thumbsup1:511780305833558026"), ":thumbsdown1:511780358690439168": hash(":thumbsdown1:511780358690439168")}
lockDown = [2, True, False]
noPerms = "```You do not have permission to use that command```"
filter_bans = [' ', '@', '_', '-', '.', '/', '`', ':', ';', '(', ')', '#', '$', '%', '^', '&', '*', '[', ']', '{', '}', '?', '=', '+']

class Poll:
    def __init__(self, origMessage, chatPoll):
        self.user = origMessage.author.id
        self.origMessage = origMessage
        self.chatPoll = chatPoll
        self.upVote = 1
        self.downVote = 1

@bot.event
async def on_ready():
    print("AnimeGuard is ready")
    print("I am running on client: " + bot.user.name)
    print("With the ID: " + bot.user.id)
    await bot.change_presence(game=discord.Game(name="do \'.help\'"))

@bot.event
async def on_message(message):
    contents = message.content.split(" ")
# Help command
    if message.content.upper().startswith('.HELP'):
        await bot.send_message(message.channel, "```" + parseHelp() + "```")

# Filters out words from the chat filter
    approval = True
    if lockDown[0] == 1:
        chat_filter = update_filter()
        print(chat_filter)
        for term in chat_filter:
            if message.content.upper().find(term) != -1:
                if message.author.id not in bypass_list:
                    try:
                        userid = message.author.id
                        await bot.delete_message(message)
                        await bot.send_message(message.channel, "<@%s> ```Anime Detected! Please consult rules #1 and #2 - do \'.rules\'```" % userid)
                        approval = False
                    except:
                        return

        for word in contents:
            if word.upper() in chat_filter:
                if message.author.id not in bypass_list:
                    try:
                        userid = message.author.id
                        await bot.delete_message(message)
                        await bot.send_message(message.channel, "<@%s> ```Anime Detected! Please consult rules #1 and #2 - do \'.rules\'```" % (userid))
                        approval = False
                    except:
                        return
        if approval and (message.author != bot.user):
            await bot.add_reaction(message, ":approved1:512134336519340033")

# lockdown toggle command, for the approval stamps
    if message.content.upper().startswith('.LOCKDOWN') and inRoles("512120756507770891", message.author):
        if lockDown[0] == 1:
            lockDown[0] = 2
            await bot.send_message(message.channel, "```Lockdown Mode Disabled```")
        elif lockDown[0] == 2:
            lockDown[0] = 1
            await bot.send_message(message.channel, "```Lockdown Mode Enabled```")

# mutes members of the "AnimePaorle" rank
    userRoles = [role.id for role in message.author.roles]
    for role in chat_banned_roles:
        if role in userRoles:
            try:
                userName = message.author.name
                await bot.delete_message(message)
                await bot.send_message(message.channel, "```Hi %s, I am your parole officer.```" % (userName))
            except:
                return

# Rules image command
    if message.content.upper().startswith('.RULES'):
        await bot.send_file(message.channel, "assets/rules.png")
        await bot.send_message(message.channel, "```^The Sacred Texts^```")

# Anime eye image command
    if message.content.upper().startswith('.GUARD'):
        await bot.send_file(message.channel, "assets/AnimeEyes.png")
        await bot.send_message(message.channel, "```I'm Always Watching```")

# Plays Despacito
    if message.content.upper().startswith(".PLAY DESPACITO"):
        await bot.send_message(message.channel, "https://www.youtube.com/watch?v=kJQP7kiw5Fk")

# Poll command
    pollUser = message.author.id
    if message.content.upper().startswith('.POLL'):
        if len(polls) != 0:
            for poll in polls:
                if poll.user == message.author.id:
                    await bot.send_message(message.channel, "```You have already made a poll --- do \'.tally\' to see the results!```")
                else:
                    query = message.content.upper().replace('.POLL', '')
                    response = await bot.send_message(message.channel, "```Poll query!\n" + query + "```")
                    await bot.add_reaction(response, ":thumbsup1:511780305833558026")
                    await bot.add_reaction(response, ":thumbsdown1:511780358690439168")
                    polls.add(Poll(message, response))
        else:
            query = message.content.upper().replace('.POLL ', '')
            response = await bot.send_message(message.channel, "```Poll query!\n     " + query + "```")
            await bot.add_reaction(response, ":thumbsup1:511780305833558026")
            await bot.add_reaction(response, ":thumbsdown1:511780358690439168")
            polls.append(Poll(message, response))

# Tally command, works with poll command
    if message.content.upper().startswith('.TALLY'):
        for poll in polls:
            if poll.user == message.author.id:
                yay = poll.upVote
                nay = poll.downVote
                await bot.send_message(message.channel, "```The Results To \"" + poll.origMessage.content.upper().replace('.POLL ', '') + "\" Are in!\nYay -- " + str(yay) + "\nNay -- " + str(nay) + "```")
                polls.remove(poll)

# Chat filter commands
    if message.content.upper().startswith('.FILTER') and inRoles("512120756507770891", message.author):
        if message.content.upper().replace('.FILTER ', '').startswith('ADD') and validFilter(message.content.upper().replace('.FILTER ADD ', '')):
            await bot.send_message(message.channel, "```Term \'%s\' Added to Chat Filter```" % message.content.upper().replace('.FILTER ADD ', ''))
            filter_file = open("chat_filter.txt", "a")
            filter_file.write("\n" + message.content.upper().replace('.FILTER ADD ', ''))
            filter_file.close()
        elif message.content.upper().replace('.FILTER ', '').startswith('ADD') and not validFilter(message.content.upper().replace('.FILTER ADD ', '')):
            await bot.send_message(message.channel, "```Invaild Filter Input\nPlease only use alphanumeric characters a-z, 0-9```")
        elif message.content.upper().replace('.FILTER ', '').startswith('REMOVE'):
            print("help")
            await bot.send_message(message.channel, "```Term \'%s\' Removed```" % "balls")
    elif message.content.upper().startswith('.FILTER') and not inRoles("512120756507770891", message.author) and message.author.id != bot.user.id:
        await bot.send_message(message.channel, noPerms)

# on reaction event, particularly for the '.poll' command
@bot.event
async def on_reaction_add(reaction, user):
    print(hash(reaction.emoji))
    print(hashes[":thumbsup1:511780305833558026"])
    if (user.id != bot.user.id) and (hash(reaction.emoji) == hashes[":thumbsup1:511780305833558026"] or hashes[":thumbsdown1:511780358690439168"]):
        for poll in polls:
            if reaction.message.id == poll.chatPoll.id:
                if hash(reaction.emoji) == hashes[":thumbsup1:511780305833558026"]:
                    print("up before")
                    poll.upVote += 1
                    await bot.add_reaction(reaction.message, ":thumbsup1:511780305833558026")
                    await bot.remove_reaction(reaction.message, ":thumbsup1:511780305833558026", user.id)
                    print("up")
                elif reaction.emoji == hashes[":thumbsdown1:511780358690439168"]:
                    poll.downVote -= 1
                    await bot.add_reaction(reaction.message, ":thumbsdown1:511780358690439168")
                    await bot.remove_reaction(reaction.message, ":thumbsdown1:511780358690439168", user.id)
                    print("down")




bot.run("NTExNjI1OTU4NzY0MzE0NjUz.Dstojg.epmW544akvZJ-pAWWCaldKpDuS4")




