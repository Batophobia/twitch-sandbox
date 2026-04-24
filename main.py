from dotenv import load_dotenv
import os
import asyncio
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI import chat, oauth, twitch
from twitchAPI.chat.middleware import StreamerOnly, GlobalCommandCooldown, ChannelUserCommandCooldown
import code.events as events
import code.replies as replies
import code.counter as counter
import code.giveaway as giveaway
import settings

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
#TODO: `!commands` command

async def handle_command_blocked(cmd: chat.ChatCommand):
  if cmd.name == "plushie":
    await counter.blocked(cmd)
  elif cmd.name == "hydrate" or cmd.name == "drink":
    await replies.blockedHydrate(cmd)
  else:
    await cmd.reply(f'You are not allowed to use {cmd.name}!')

async def setupCommand(chatObj, command, config):
  middleWare = None
  # Cooldown Middleware
  #https://pytwitchapi.dev/en/stable/modules/twitchAPI.chat.middleware.html
  if "cooldown" in config:
    cooldownSeconds = int(config["cooldown"]["seconds"])
    match config["cooldown"]["type"]:
      case "user":
        middleWare = [ChannelUserCommandCooldown(cooldownSeconds)]
      case _:
        middleWare = [GlobalCommandCooldown(cooldownSeconds)]
  
  # Restriction Middleware
  if "restriction" in config:
    match config["restriction"]["type"]:
      case "STREAMER_ONLY":
        middleWare = [StreamerOnly()]

  # Get the correct function to run
  commandFunction = replies.reply
  match config["type"]:
    case "reply":
      commandFunction = replies.reply
    case "counter":
      if config["user-based"]:
        commandFunction = counter.userCount
      else:
        commandFunction = counter.count
  
  # Register the command
  #https://pytwitchapi.dev/en/stable/modules/twitchAPI.chat.html#twitchAPI.chat.Chat.register_command
  chatObj.register_command(command, commandFunction, middleWare)
  if "alias" in config:
    for alias in config["alias"]:
      settings.addAlias(command, alias)
      chatObj.register_command(alias, commandFunction, middleWare)

async def runBot():
  # init modules
  settings.init()
  await counter.initCount()
  await giveaway.init()

  # Setup Twitch connection
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
  for command in settings.CONFIG_DATA:
    if command.startswith("__"):
      continue

    print(f"Setting up {command}")
    await setupCommand(chatObj, command, settings.CONFIG_DATA[command])
    print("-------------------------------------")
  
  # TESTING COMMANDS
  chatObj.register_command("test", replies.test)

  # Blocked and restricted
  chatObj.default_command_execution_blocked_handler = handle_command_blocked

  chatObj.start()

  try:
    while True:
      await asyncio.sleep(1)
  except KeyboardInterrupt:
    pass
  finally:
    chatObj.stop()
    await bot.close()

asyncio.run(runBot())