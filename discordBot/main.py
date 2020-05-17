import socket
import logging
import sys

import discord
from discord.ext import commands

TOKEN = "NzA4NDk1MzE3MjUwNzM2MjE5.XrYMBA.FaVTkwsRqjuYYALfGhiQ3yYYxOs"
GUILD = "Dota"

client = discord.Client()

SERVER = "irc.twitch.tv"
PORT = 6667
PASS = "oauth:txn9h654a11lm8g68e887xxnm6svuk"
BOT = "Hezza_bot"
CHANNEL = "saltybet"

logger = logging.getLogger(__name__)

def connect():
    irc = socket.socket()
    irc.connect((SERVER,PORT))
    irc.send(("PASS " + PASS + "\n" + "NICK " + BOT + "\n" + "JOIN #" + CHANNEL + "\n").encode())
    return irc

def joinchat():
    irc = connect()

    while True:
        readbuffer_join = irc.recv(1024)
        readbuffer_join = readbuffer_join.decode()
        if not readbuffer_join:
            logger.warning("Socket potentially down reconnecting ...")
            irc = connect()
        for line in readbuffer_join.split("\n"):
            if (":waifu4u!waifu4u@waifu4u.tmi.twitch.tv PRIVMSG #saltybet :" in line) and ("until the next tournament!"in line):
                matches_left = [int(s) for s in line.split() if s.isdigit()]
                if matches_left[0] <= 3:
                    return True

@client.event
async def on_message(message):
    # id = client.get_guild(296654019600842765)
    # print(message.content)
    while True:
        if joinchat():
            await message.channel.send("@here Tournament on salty starting soon ...")

client.run(TOKEN)

