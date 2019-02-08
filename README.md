# AnimeGuard

Uses Discord API to collect chat messages and information sent through connected servers. Then, the bot will look into a filter list of all words selected by server admins on that server, and remove the message if it matches any part of that list. Also has various other commands for general ease of use and quality of life in managing a Discord server.

Learned about using an API, and looking through documentation of other libraries. Also learned about using puthon to create, store, and modify local files to keep track of information.


<hr/>


AnimeGuard discord bot using python

The default command prefix is '.'

use '.help' in discord or look in 'server_commands_help.txt' to see commands and uses


<hr/>

## Bot Commands:
.help --- displays this window; works with '.' prefix or custom prefix <br/>
.setup help --- displays commands for server settings; must have admin rank <br/>
.rules --- server rules <br/>
.guard --- official AnimeGuard logo <br/>
.play despacito --- plays despacito <br/>
.poll --- runs a poll yes or no poll, only one per user at a time <br/>
.tally --- tallys the results from a poll <br/>
.lockdown --- toggles server lockdown mode (disables words from the chat filter and displays approval reactions) <br/>
.filter add [term] --- adds a given term to the chat filter (only alphanumeric characters a-z, 0-9) <br/>
.filter remove [term] --- removes a given term from the chat filter <br/>

### Some commands may be implemented, but not updated in this list of commands
