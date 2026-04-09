from twitchAPI import chat
import random
from random import randrange
from datetime import datetime

#https://pytwitchapi.dev/en/stable/modules/twitchAPI.chat.html#twitchAPI.chat.ChatMessage

async def lurk(cmd: chat.ChatCommand):
  await cmd.reply("Well lurk who's here")


async def chaotic(cmd: chat.ChatCommand):
  curDate = datetime.now().strftime("%d/%m/%Y")
  random.seed(f"chaos{cmd.user.name}{curDate}")
  batman = randrange(101)
  await cmd.reply(f"💥 {cmd.user.name} is {batman}% chaotic today 🧨")
async def cozy(cmd: chat.ChatCommand):
  curDate = datetime.now().strftime("%d/%m/%Y")
  random.seed(f"cozy{cmd.user.name}{curDate}")
  batman = randrange(101)
  await cmd.reply(f"☕ {cmd.user.name} is {batman}% cozy today 🧸")

####### HYDRATE BLOCK #######

HYDRATE_COOLDOWN = 60

async def hydrate(cmd: chat.ChatCommand):
  await cmd.reply(f"{cmd.user.name} wants everyone to stay hydrated.  Drink up!")

async def blockedHydrate(cmd: chat.ChatCommand):
  await cmd.reply(f"Hydrate command is currently on cooldown")

####### HYDRATE BLOCK #######