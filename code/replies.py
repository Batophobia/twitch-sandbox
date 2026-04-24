from twitchAPI import chat
from code.common import replaceVars
from code.common import replaceRandom
from code.common import getCommandData

#https://pytwitchapi.dev/en/stable/modules/twitchAPI.chat.html#twitchAPI.chat.ChatMessage

async def reply(cmd: chat.ChatCommand):
  # Get command config
  cmdData = getCommandData(cmd)
  
  # Get random seed if needed
  randSeed = None
  if("seed" in cmdData):
    randSeed = cmdData["seed"]
  
  # Generate response
  resp = cmdData["response"]
  resp = replaceVars(cmd, resp)
  resp = replaceRandom(cmd, resp, randSeed)
  await cmd.reply(resp)

async def blocked(cmd: chat.ChatCommand):
  # Get command config
  cmdData = getCommandData(cmd)
  
  # Get random seed if needed
  randSeed = None
  if("seed" in cmdData):
    randSeed = cmdData["seed"]
  
  # Generate response
  resp = cmdData["response"]
  resp = replaceVars(cmd, resp)
  resp = replaceRandom(cmd, resp, randSeed)
  await cmd.reply(resp)


async def test(cmd: chat.ChatCommand):
  await cmd.chat.send_message(cmd.room, "line 1")
  await cmd.chat.send_message(cmd.room, "line 2")
  await cmd.reply("line 3")
