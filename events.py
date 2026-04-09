# Events for Twitch
from twitchAPI import chat
from dotenv import load_dotenv
import os

load_dotenv()
TARGET_CHANNEL = os.getenv('TARGET_CHANNEL')

async def onFirstTimeMessage(msg: chat.ChatMessage):
  print(f'first time message')

#https://pytwitchapi.dev/en/stable/modules/twitchAPI.chat.html#twitchAPI.chat.ChatSub
async def onSub(msg: chat.ChatSub):
  print(f'New subscription in {sub.room.name}:\n'
          f'  Type: {sub.sub_plan}\n'
          f'  Message: {sub.sub_message}')

async def onMessage(msg: chat.ChatMessage):
  # print(f'{msg.user.display_name} - {msg.text}')
  if msg.first:
    await onFirstTimeMessage(msg)


async def onReady(event: chat.EventData):
  global TARGET_CHANNEL
  await event.chat.join_room(TARGET_CHANNEL)
  print("Bot connected to chat")
