import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import os
import json


def get_setting(settingRequest, serverid):
    with open("servers/" + str(serverid) + "/settings.json", 'r') as server_json_settings:
        server_settings = json.load(server_json_settings)
        server_json_settings.close()
        for setting in server_settings:
            if setting == settingRequest:
                return server_settings[setting]

def replace_setting(settingRequest, settingReplace, serverid):
    with open("servers/" + str(serverid) + "/settings.json", 'r') as server_json_settings:
        server_settings = json.load(server_json_settings)
        server_json_settings.close()
        for setting in server_settings:
            if setting == settingRequest:
                server_settings[setting] = settingReplace
        with open("servers/" + str(serverid) + "/settings.json", 'w') as server_json_settings:
            json.dump(server_settings, server_json_settings, indent=2)
            server_json_settings.close()



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


