import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import os

class Server:
    def __init__(self, serverIN):
        self.server = serverIN.id
        self.serverIndex = retrieve_server(serverIN)
        self.prefix
        self.approval
        self.upvote
        self.downvote

    def replace_setting(self, datatype):
        if datatype == "prefix":
            10

    def get_settings(self):
        5
def get_server(id):
    server_file = open("servers/" + str(id) + "/test.txt", "r+")
    return server_file.readline()

def get_servers():
    server_list = []
    server_list_file = open("server_list.txt", "r")
    for line in server_list_file.readlines():
      server_list.append(line.replace('\n', ''))
    server_list_file.close()
    return server_list

def update_servers(bot):
    server_list_file = open("server_list.txt", "w")
    for server in bot.servers:
      server_list_file.write(server.id + "\n")
    server_list_file.close()

def retrieve_server(serverid):
    n = 0
    for id, n in get_servers():
        if serverid == id:
            return n

def setup_dir(id):
    directory = "servers/" + str(id)
    if not os.path.exists(directory):
        os.makedirs(directory)
    print(directory)
    if not os.path.exists(directory + "/test.txt"):
        open(directory + "/test.txt", 'a+').close()


