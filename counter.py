from twitchAPI import chat

COUNTER_FILE = "./count.txt"
CURRENT_COUNTER = 0

async def count(cmd: chat.ChatCommand):
  global CURRENT_COUNTER
  print("Adding to counter")
  CURRENT_COUNTER += 1
  with open(COUNTER_FILE, 'w') as output:
    output.write(str(CURRENT_COUNTER))

async def initCount():
  global CURRENT_COUNTER
  print("Initializing counter")
  with open(COUNTER_FILE, "r") as f:
    countFile = f.read()
    CURRENT_COUNTER = int(countFile)
  print(f"Counter initialized to {CURRENT_COUNTER}")
