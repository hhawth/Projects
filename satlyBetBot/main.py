import json
import re
import socket
import logging
import sys

from predictor import fight_predictions as fp

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

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
    logger.info("Bot starting")
    # if missed fight start
    home = ""
    away = ""
    with open("data.txt") as json_file:
        data = json.load(json_file)

    irc = connect()

    while True:
        readbuffer_join = irc.recv(1024)
        readbuffer_join = readbuffer_join.decode()
        if not readbuffer_join:
            logger.warning("Socket potentially down reconnecting ...")
            irc = connect()
        for line in readbuffer_join.split("\n"):
            if (":waifu4u!waifu4u@waifu4u.tmi.twitch.tv PRIVMSG #saltybet :Bets are OPEN for" in line) and ("exhibition" not in line):
                if ("tournament" in line):
                    fight = line.replace(":waifu4u!waifu4u@waifu4u.tmi.twitch.tv PRIVMSG #saltybet :Bets are OPEN for ","").replace(") tournament bracket: http://www.saltybet.com/shaker?bracket=1","").replace("! ("," vs ").split(" vs ")
                    home, away, tier = fight[0], fight[1], fight[2].rstrip()
                else:
                    fight = line.replace(") (matchmaking) www.saltybet.com","").replace(":waifu4u!waifu4u@waifu4u.tmi.twitch.tv PRIVMSG #saltybet :Bets are OPEN for ","").replace("! ("," vs ").split(" vs ")
                    home, away, tier = fight[0], fight[1], fight[2].rstrip()
                logger.info(f"{home} vs {away},  tier: {tier}")
                logger.info(f"{fp(home, away, tier)}")
            elif ("wins! Payouts" in line) and ("exhibition" not in line):
                winner = line.replace(":waifu4u!waifu4u@waifu4u.tmi.twitch.tv PRIVMSG #saltybet :","").split(" wins! Payouts")[0]
                logger.info(f"winner: {winner}")

                # in the case when starting up you missed a fight start
                if winner != home and winner != away:
                    continue

                if winner == home:
                    loser = away
                else:
                    loser = home

                d_win = data['tiers'].get(tier).get(winner) if winner in data['tiers'].get(tier) else False
                d_lose = data['tiers'].get(tier).get(loser) if loser in data['tiers'].get(tier) else False

                if d_win:
                    d_win['total_games'] = d_win.get('total_games') + 1
                    d_win['win'] = d_win.get('win') + 1
                    if loser in d_win['opponents']:
                        d_win['opponents'].get(loser)["win"] = d_win.get("opponents").get(loser).get("win") + 1
                    else:
                        d_win['opponents'][f"{loser}"] = {"win": 1, "lose": 0}
                else:
                    data['tiers'].get(tier)[f"{winner}"] = {"total_games": 1, "win": 1, "lose": 0, "opponents": {f"{loser}": {"win": 1, "lose": 0}}}

                if d_lose:
                    d_lose['total_games'] = d_lose.get('total_games') + 1
                    d_lose['lose'] = d_lose.get('lose') + 1
                    if winner in d_lose['opponents']:
                        d_lose['opponents'].get(winner)["lose"] = d_win.get("opponents").get(loser).get("lose") + 1
                    else:
                        d_lose['opponents'][f"{winner}"] = {"win": 0, "lose": 1}
                else:
                    data['tiers'].get(tier)[f"{loser}"] = {"total_games": 1, "win": 0, "lose": 1, "opponents": {f"{winner}": {"win": 0, "lose": 1}}}

                with open('data.txt', 'w') as file:
                    file.write(json.dumps(data))


joinchat()