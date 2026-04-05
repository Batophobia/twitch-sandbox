from dotenv import load_dotenv
import os
import asyncio
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI import chat, oauth, twitch
import events
import counter
import replies

# https://dev.twitch.tv/console/apps

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_MANAGE_BROADCAST]

async def runBot():
  bot = await chat.Twitch(CLIENT_ID, CLIENT_SECRET)
  auth = oauth.UserAuthenticator(bot, USER_SCOPE)
  token, refreshToken = await auth.authenticate()
  await bot.set_user_authentication(token, USER_SCOPE, refreshToken)

  chatObj = await chat.Chat(bot)
  # EVENTS
  chatObj.register_event(ChatEvent.READY, events.onReady)
  chatObj.register_event(ChatEvent.MESSAGE, events.onMessage)
  chatObj.register_event(ChatEvent.SUB, events.onSub)

  # COMMANDS
  chatObj.register_command('lurk', replies.lurk)
  chatObj.register_command('hydrate', replies.hydrate)
  await counter.initCount()
  chatObj.register_command('plushie', counter.count)

  chatObj.start()

  try:
    input('press ENTER to stop\n')
  finally:
    chatObj.stop()
    await bot.close()

asyncio.run(runBot())