def get_servers():
  server_list = []
  server_list_file = open("server_list.txt", "r")
  for line in server_list_file.readlines():
    server_list.append(line.replace('\n', ''))
  server_list_file.close()
  return server_list

def update_servers(bot):
  server_list_file = open("serrver_list.txt", "w")
  for server in bot.servers
