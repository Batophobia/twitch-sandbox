import random
from random import randrange
import re
from twitchAPI import chat

def replaceRandom(match: str):
	minVal, maxVal = match.groups()
	return str(randrange(int(minVal), int(maxVal)+1))

async def replaceVars(cmd: chat.ChatCommand, inString: str, randSeed: str = None):
  if(randSeed != None):
    random.seed(randSeed)
  
  # RANDOM_NUMBER:0-100
  rgx = re.compile(r'\{\{RANDOM_NUMBER\:(\d+)\-(\d+)\}\}')
  inString = rgx.sub(replaceRandom, inString)

  return inString.replace("{{USERNAME}}", cmd.user.name)

def getConfigText(filename: str):
  with open(filename, "r", encoding='utf-8') as file:
    resp = file.read()
    return resp