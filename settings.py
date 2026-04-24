import json

COMMANDS_FILE = "./config/commands.json"

def init():
  global CONFIG_DATA
  with open(COMMANDS_FILE, 'r', encoding='utf-8') as file:
    CONFIG_DATA = json.load(file)
    if "__aliases" not in CONFIG_DATA:
      CONFIG_DATA["__aliases"] = {}

def addAlias(command, alias):
  global CONFIG_DATA
  CONFIG_DATA["__aliases"][alias] = command