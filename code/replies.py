from twitchAPI import chat
import random
from random import randrange
from datetime import datetime
from code.common import replaceVars
from code.common import getConfigText

#https://pytwitchapi.dev/en/stable/modules/twitchAPI.chat.html#twitchAPI.chat.ChatMessage

async def lurk(cmd: chat.ChatCommand):
  configString = getConfigText("./config/chaotic.txt")
  resp = await replaceVars(cmd, configString)
  await cmd.reply(resp)

async def chaotic(cmd: chat.ChatCommand):
  curDate = datetime.now().strftime("%d/%m/%Y")
  configString = getConfigText("./config/chaotic.txt")
  resp = await replaceVars(cmd, configString, f"chaos{cmd.user.name}{curDate}")
  await cmd.reply(resp)
async def cozy(cmd: chat.ChatCommand):
  curDate = datetime.now().strftime("%d/%m/%Y")
  configString = getConfigText("./config/cozy.txt")
  resp = await replaceVars(cmd, configString, f"cozy{cmd.user.name}{curDate}")
  await cmd.reply(resp)

####### HYDRATE BLOCK #######

HYDRATE_COOLDOWN = 60

async def hydrate(cmd: chat.ChatCommand):
  configString = getConfigText("./config/hydrate.txt")
  resp = await replaceVars(cmd, configString)
  await cmd.reply(resp)

async def blockedHydrate(cmd: chat.ChatCommand):
  configString = getConfigText("./config/hydrate-cooldown.txt")
  resp = await replaceVars(cmd, configString)
  await cmd.reply(resp)

####### HYDRATE BLOCK #######