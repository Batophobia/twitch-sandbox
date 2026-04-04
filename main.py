from dotenv import load_dotenv
import os
import asyncio
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI import chat, oauth, twitch

# https://dev.twitch.tv/console/apps

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_MANAGE_BROADCAST]
TARGET_CHANNEL = os.getenv('TAGET_CHANNEL')

COUNTER_FILE = "./count.txt"
CURRENT_COUNTER = 0

async def lurk(cmd: chat.ChatCommand):
  print(cmd)
  await cmd.reply("Well lurk who's here")

async def hydrate(cmd: chat.ChatCommand):
  await cmd.reply(f"{cmd.user.name} wants everyone to stay hydrated.  Drink up!")

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


async def onMessage(msg: chat.ChatMessage):
  print(f'{msg.user.display_name} - {msg.text}')

async def onReady(event: chat.EventData):
  await event.chat.join_room(TARGET_CHANNEL)
  print("Bot connected to chat")

async def runBot():
  bot = await chat.Twitch(CLIENT_ID, CLIENT_SECRET)
  auth = oauth.UserAuthenticator(bot, USER_SCOPE)
  token, refreshToken = await auth.authenticate()
  await bot.set_user_authentication(token, USER_SCOPE, refreshToken)

  chatObj = await chat.Chat(bot)
  # EVENTS
  chatObj.register_event(ChatEvent.READY, onReady)
  chatObj.register_event(ChatEvent.MESSAGE, onMessage)

  # COMMANDS
  chatObj.register_command('lurk', lurk)
  chatObj.register_command('hydrate', hydrate)
  await initCount()
  chatObj.register_command('plushie', count)

  chatObj.start()

  try:
    input('press ENTER to stop\n')
  finally:
    chatObj.stop()
    await bot.close()

asyncio.run(runBot())