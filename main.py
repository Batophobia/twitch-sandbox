from dotenv import load_dotenv
import os
import asyncio
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI import chat, oauth, twitch
from twitchAPI.chat.middleware import StreamerOnly, GlobalCommandCooldown, ChannelUserCommandCooldown
import events
import counter
import replies

# https://dev.twitch.tv/console/apps

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_MANAGE_BROADCAST]

#TODO: Song Requests
#TODO: Early-viewer VIP
#TODO: Community loyalty
#TODO: Twitch Ads
#TODO: Daily redeem counter
#TODO: Chat follower
#TODO: New Subscriber - onSub
#TODO: Re-Subscriber
#TODO: Gift sub to specific user
#TODO: Gift sub to community
#TODO: Bits
#TODO: Raids
#TODO: Ad break notification
#TODO: Command aliases

async def handle_command_blocked(cmd: chat.ChatCommand):
  if cmd.name == "plushie":
    await counter.blocked(cmd)
  elif cmd.name == "hydrate" or cmd.name == "drink":
    await replies.blockedHydrate(cmd)
  else:
    await cmd.reply(f'You are not allowed to use {cmd.name}!')

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
  #https://pytwitchapi.dev/en/stable/modules/twitchAPI.chat.html#twitchAPI.chat.Chat.register_command
  #https://pytwitchapi.dev/en/stable/modules/twitchAPI.chat.middleware.html
  chatObj.register_command('lurk', replies.lurk)
  chatObj.register_command('hydrate', replies.hydrate, [GlobalCommandCooldown(replies.HYDRATE_COOLDOWN)])
  chatObj.register_command('drink', replies.hydrate, [GlobalCommandCooldown(replies.HYDRATE_COOLDOWN)])
  chatObj.register_command('chaotic', replies.chaotic)
  chatObj.register_command('cozy', replies.cozy)
  await counter.initCount()
  chatObj.register_command('plushie', counter.count, [StreamerOnly()])
  chatObj.register_command('daily', counter.userCount, [ChannelUserCommandCooldown(86400)])
  
  chatObj.default_command_execution_blocked_handler = handle_command_blocked

  chatObj.start()

  try:
    input('press ENTER to stop\n')
  finally:
    chatObj.stop()
    await bot.close()

asyncio.run(runBot())