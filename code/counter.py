from twitchAPI import chat
import json

USER_COUNTER_FILE = "./countUser.json"
DAILY_COUNT_MESSAGE = "[[USER]] has eaten [[COUNT]] glizzies"
COUNTER_FILE = "./code/count.txt"
CURRENT_COUNTER = 0

async def blocked(cmd: chat.ChatCommand):
  await cmd.reply(f"Nice try {cmd.user.name}")

async def count(cmd: chat.ChatCommand):
  # if not cmd.user.mod:
  #   return
  
  global CURRENT_COUNTER
  print("Adding to counter")
  CURRENT_COUNTER += 1
  with open(COUNTER_FILE, 'w') as file:
    file.write(str(CURRENT_COUNTER))

async def initCount():
  global CURRENT_COUNTER
  print("Initializing counter")
  with open(COUNTER_FILE, "r") as file:
    countFile = file.read()
    CURRENT_COUNTER = int(countFile)
  print(f"Counter initialized to {CURRENT_COUNTER}")


async def userCount(cmd: chat.ChatCommand):
  print(f"Updating count for {cmd.user.name}")
  with open(USER_COUNTER_FILE, 'r') as file:
    data = json.load(file)
  print(f"Loaded data")
  if cmd.user.id not in data:
    data[cmd.user.id] = 0
  data[cmd.user.id] += 1
  
  with open(USER_COUNTER_FILE, 'w') as file:
    file.write(json.dumps(data))
  await cmd.reply(DAILY_COUNT_MESSAGE.replace("[[USER]]", cmd.user.name).replace("[[COUNT]]", str(data[cmd.user.id])))