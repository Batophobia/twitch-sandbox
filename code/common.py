import random
from random import randrange
import re
import settings
from datetime import datetime
from twitchAPI import chat

def replaceRandomNumber(match: str):
	minVal, maxVal = match.groups()
	return str(randrange(int(minVal), int(maxVal)+1))

def replaceVars(cmd: chat.ChatCommand, inString: str):
  curDate = datetime.now().strftime("%d/%m/%Y")
  
  inString = inString.replace("{{USERNAME}}", cmd.user.name)
  inString = inString.replace("{{NOW_DATE}}", curDate)

  return inString

def replaceRandom(cmd: chat.ChatCommand, inString: str, randSeed: str = None):
  if(randSeed != None):
    random.seed(replaceVars(cmd, randSeed))
  
  # RANDOM_NUMBER:0-100
  rgx = re.compile(r'\{\{RANDOM_NUMBER\:(\d+)\-(\d+)\}\}')
  return rgx.sub(replaceRandomNumber, inString)

def getConfigText(filename: str):
  with open(filename, "r", encoding='utf-8') as file:
    resp = file.read()
    return resp

def getCommandData(cmd: chat.ChatCommand):
  commandName = cmd.name
  if commandName in settings.CONFIG_DATA["__aliases"]:
    commandName = settings.CONFIG_DATA["__aliases"][cmd.name]

  if commandName in settings.CONFIG_DATA:
    return settings.CONFIG_DATA[commandName]
  
  print(f"ERROR: command {commandName} not found")
  return None