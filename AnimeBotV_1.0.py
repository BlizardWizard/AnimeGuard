import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from AnimeBotV1 import servers
from AnimeBotV1 import filter

Client = discord.Client()
bot = commands.Bot(command_prefix="%")



def inRoles(checkRole, user):
    for role in user.roles:
        if role.id == checkRole:
            return True



def parseTxt(file):
    commandsString = ""
    commands_file = open(file, "r")
    for line in commands_file:
        commandsString += line
    commands_file.close()
    return commandsString

bypass_list = ["511625958764314653"]
chat_banned_roles = ["511630140065972226"]
polls = []
lockDown = [2, True, False]
noPerms = "```You do not have permission to use that command```"
filter_bans = [' ', '@', '_', '-', '.', '/', '`', ':', ';', '(', ')', '#', '$', '%', '^', '&', '*', '[', ']', '{', '}', '?', '=', '+']
server_list = []

class Poll:
    def __init__(self, origMessage, chatPoll):
        self.user = origMessage.author.id
        self.origMessage = origMessage
        self.chatPoll = chatPoll
        self.upVote = 0
        self.downVote = 0

@bot.event
async def on_ready():
    print("AnimeGuard is ready")
    print("I am running on client: " + bot.user.name)
    print("With the ID: " + bot.user.id)
    await bot.change_presence(game=discord.Game(name="do \'.help\'"))
    servers.update_servers(bot)


@bot.event
async def on_message(message):
    servers.setup_dir(message.server.id)
    if not servers.isSetup(message.server.id) and message.author.id != bot.user.id and message.content.startswith('.') and not message.content.upper().startswith(".SETUP MODERATOR"):
        await bot.send_message(message.channel, "```ERROR: Server does not yet have a moderator role assigned!\n\n"
                                                "To properly use AnimeGuard, there must be an assigned moderator role. "
                                                "To assign a role as moderator, simply use the command:\n\n"
                                                "'.setup moderator {@rolename}'\n\n"
                                                "where you @mention the role in place of the brackets.\n\n"
                                                "You can use any role as moderator, but it is reccomended to use a high ranking or specially made role \n**(keep in mind that the role must be mentionable)**\n\n"
                                                "A user with the moderator role is able to use the '.lockdown' and '.setup' commands```")

    # All commands and features fall under this section of code, which only runs if the bot is not the message sender
    elif message.author.id != bot.user.id:


    # Help command
        if (message.content.upper().startswith(servers.get_setting('prefix', str(message.server.id)) + 'HELP') or message.content.upper().startswith('.HELP')) and message.author.id != bot.user.id:
            await bot.send_message(message.channel, "```---------------------Your server's prefix is '" + servers.get_setting('prefix', message.server.id) + "'---------------------\n\n" + parseTxt("server_commands_help.txt") + "```")

    # .setup command, various setup commands for per server bot settings
        if message.content.upper().startswith(servers.get_setting('prefix', message.server.id) + 'SETUP') and message.author.id != bot.user.id:
            subCommand = message.content.upper().replace(servers.get_setting('prefix', message.server.id) + 'SETUP ', '')

        # '.setup prefix' sub-command that allows the server to have its own custom command prefix
            if subCommand.startswith('PREFIX'):
                for server in servers.get_servers():
                    if server == message.server.id:
                        prefix = message.content.upper().replace(servers.get_setting('prefix', message.server.id) + 'SETUP PREFIX ', '')
                        servers.replace_setting('prefix', prefix, message.server.id)
                        await bot.send_message(message.channel, "```Successfully changed prefix to '%s'```" % prefix)
        # '.setup approval' sub-command for setting the approval reaction for the '.lockdown' command
            elif subCommand.startswith('APPROVAL'):
                setEmoji = subCommand.replace('APPROVAL ', '')
                if setEmoji.startswith('<'):
                    setEmoji = setEmoji.replace('<', '').replace('>', '')
                servers.replace_setting('approval', setEmoji, message.server.id)
                await bot.send_message(message.channel, "```\'.lockdown\' approval reaction set to \':approved1:\'```")
        # '.setup moderator' sub-command to set the moderator rank for the server. Allows access to various commands
            elif subCommand.startswith('MODERATOR'):
                setRank = subCommand.replace('MODERATOR <@&', '').replace('>', '')
                roles = message.server.roles
                for role in roles:
                    if role.id == setRank:
                        servers.replace_setting('moderator', setRank, message.server.id)
                        await bot.send_message(message.channel, "```Moderator rank set to '" + role.name + "'```")
        # '.setup parole' sub-command to set the parole rank fot the server. Disallows the ability to chat for users with this rank.
            elif subCommand.startswith('PAROLE'):
                setRank = subCommand.replace('PAROLE <@&', '').replace('>', '')
                roles = message.server.roles
                for role in roles:
                    if role.id == setRank:
                        servers.replace_setting('parole', setRank, message.server.id)
                        await bot.send_message(message.channel, "```Parole rank set to: " + role.name + "```")

        # '.setup help' sub-command that displays the setup help window
            elif subCommand.startswith('HELP') or subCommand.startswith(''):
                await bot.send_message(message.channel,
                                       "```----------User must have admin role to use '.setup' commands----------\n\n" + open(
                                           "server_setup_help.txt", 'r').read() + "```")


    # Filters out words from the chat filter
        approval = True
        if servers.get_setting('lockdown', message.server.id):
            chat_filter = filter.get_filter(message.server.id)
            for term in chat_filter:
                if message.content.upper().find(term) != -1:
                    if message.author.id not in bypass_list:
                        try:
                            userid = message.author.id
                            await bot.delete_message(message)
                            await bot.send_message(message.channel, "<@%s> ```Anime Detected! Please consult the server rules - do \'.rules\'```" % userid)
                            approval = False
                        except:
                            return

            contents = message.content.split(" ")
            for word in contents:
                if word.upper() in chat_filter:
                    if message.author.id not in bypass_list:
                        try:
                            userid = message.author.id
                            await bot.delete_message(message)
                            await bot.send_message(message.channel, "<@%s> ```Anime Detected! Please consult the server rules - do \'.rules\'```" % (userid))
                            approval = False
                        except:
                            return
        # approval reaction for messages that are not filtered out during '.lockdown' mode
            if approval and (message.author != bot.user):
                await bot.add_reaction(message, servers.get_setting("approval", message.server.id))

    # lockdown toggle command, for the approval stamps
        if message.content.upper().startswith(servers.get_setting('prefix', message.server.id) + 'LOCKDOWN'): # and inRoles("512120756507770891", message.author):
            if servers.get_setting('lockdown', message.server.id):
                servers.replace_setting('lockdown', False, message.server.id)
                await bot.send_message(message.channel, "```Lockdown Mode Disabled```")
            elif not servers.get_setting('lockdown', message.server.id):
                servers.replace_setting('lockdown', True, message.server.id)
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
        if message.content.upper().startswith(servers.get_setting('prefix', message.server.id) + 'RULES'):
            await bot.send_file(message.channel, "assets/rules.png")
            await bot.send_message(message.channel, "```^The Sacred Texts^```")

    # Anime eye image command
        if message.content.upper().startswith(servers.get_setting('prefix', message.server.id) + 'GUARD'):
            await bot.send_file(message.channel, "assets/AnimeEyes.png")
            await bot.send_message(message.channel, "```I'm Always Watching```")

    # Plays Despacito
        if message.content.upper().startswith(".PLAY DESPACITO"):
            await bot.send_message(message.channel, "https://www.youtube.com/watch?v=kJQP7kiw5Fk")

    # Poll command
        pollUser = message.author.id
        if message.content.upper().startswith(servers.get_setting('prefix', message.server.id) + 'POLL'):
            if len(polls) != 0:
                for poll in polls:
                    if poll.user == message.author.id:
                        await bot.send_message(message.channel, "```You have already made a poll --- do \'.tally\' to see the results!```")
                    else:
                        query = message.content.upper().replace(servers.get_setting('prefix', message.server.id) + 'POLL', '')
                        response = await bot.send_message(message.channel, "```Poll query!\n" + query + "```")
                        await bot.add_reaction(response, ":thumbsup1:511780305833558026")
                        await bot.add_reaction(response, ":thumbsdown1:511780358690439168")
                        polls.add(Poll(message, response))
            else:
                query = message.content.upper().replace(servers.get_setting('prefix', message.server.id) + 'POLL ', '')
                response = await bot.send_message(message.channel, "```Poll query!\n     " + query + "```")
                await bot.add_reaction(response, ":thumbsup1:511780305833558026")
                await bot.add_reaction(response, ":thumbsdown1:511780358690439168")
                polls.append(Poll(message, response))

    # Tally command, works with poll command
        if message.content.upper().startswith(servers.get_setting('prefix', message.server.id) + 'TALLY'):
            for poll in polls:
                if poll.user == message.author.id:
                    yay = poll.upVote
                    nay = poll.downVote
                    await bot.send_message(message.channel, "```The Results To \"" + poll.origMessage.content.upper().replace(servers.get_setting('prefix', message.server.id) + 'POLL ', '') + "\" Are in!\nYay -- " + str(yay) + "\nNay -- " + str(nay) + "```")
                    polls.remove(poll)

    # Chat filter commands
        if message.content.upper().startswith(servers.get_setting('prefix', message.server.id) + 'FILTER'): # and inRoles("512120756507770891", message.author):
            filterArgs = message.content.upper().replace(servers.get_setting('prefix', message.server.id) + 'FILTER ', '')
            # '.filter add {}' command
            if filterArgs.startswith('ADD') and filter.isValidFilter(message.content.upper().replace(servers.get_setting('prefix', message.server.id) + 'FILTER ADD ', ''), filter_bans) and filterArgs.replace('ADD ', '') not in filter.get_filter(message.server.id):
                term = filterArgs.replace('ADD ', '').upper()
                filter.add_filter(term, message.server.id)
                await bot.send_message(message.channel, "```Term \'%s\' Added to Chat Filter```" % term)
            # errors for '.filter add {}' command
            elif filterArgs.startswith('ADD') and not filter.isValidFilter(message.content.upper().replace(servers.get_setting('prefix', message.server.id) + 'FILTER ADD ', ''), filter_bans): # invalid filter characters
                await bot.send_message(message.channel, "```Invaild Filter Input\nPlease only use alphanumeric characters a-z, 0-9```")
            elif filterArgs.startswith('ADD') and message.content.upper().replace(servers.get_setting('prefix', message.server.id) + 'FILTER ADD ', '') in filter.get_filter(message.server.id): # term already in filter list
                await bot.send_message(message.channel, "```Term is already in filter list```")
            # '.filter remove {}' command
            elif filterArgs.startswith('REMOVE'):
                term = message.content.upper().replace(servers.get_setting('prefix', message.server.id) + 'FILTER REMOVE ', '')
                filter.filter_remove(term, message.server.id)
                await bot.send_message(message.channel, "```Term \'%s\' Removed```" % term)
            # displays a list of current filtered words
            elif filterArgs.startswith('LIST'):
                await bot.send_message(message.channel, "```" + str(filter.get_filter(message.server.id)) + "```")
            # clears server filter list
            elif filterArgs.startswith('CLEAR'):
                open("servers/" + message.server.id + "/chat_filter.txt", 'w').close()
                await bot.send_message(message.channel, "```Filter list cleared```")
        elif message.content.upper().startswith(servers.get_setting('prefix', message.server.id) + 'FILTER') and not inRoles("512120756507770891", message.author) and message.author.id != bot.user.id:
            await bot.send_message(message.channel, noPerms)

# on reaction event, particularly for the '.poll' command
@bot.event
async def on_reaction_add(reaction, user):
    if (user.id != bot.user.id) and (reaction.emoji == "<:thumbsup1:511780305833558026>" or "<:thumbsdown1:511780358690439168>"):
        for poll in polls:
            if reaction.message.id == poll.chatPoll.id:
                if str(reaction.emoji) == "<:thumbsup1:511780305833558026>":
                    poll.upVote += 1
                    await bot.add_reaction(reaction.message, ":thumbsup1:511780305833558026")
                elif str(reaction.emoji) == "<:thumbsdown1:511780358690439168>":
                    poll.downVote += 1
                    await bot.add_reaction(reaction.message, ":thumbsdown1:511780358690439168")





bot.run("")




