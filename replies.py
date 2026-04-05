from twitchAPI import chat

async def lurk(cmd: chat.ChatCommand):
  print(cmd)
  await cmd.reply("Well lurk who's here")

async def hydrate(cmd: chat.ChatCommand):
  await cmd.reply(f"{cmd.user.name} wants everyone to stay hydrated.  Drink up!")
