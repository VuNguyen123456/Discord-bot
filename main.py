import discord
import os
import requests  # allows us to get information from the web (we will use this for getting the dog pictures)
import json
import random
from replit import db
from requests.sessions import HTTPAdapter
from keep_alive import keep_alive

depresses = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing", "sadge"]
anti_depresses = ["do it", "love u", "don't do it", "kys (keep yourself safe)", "you are my friend", "keep walking"]

# To turn on and of if the bot is responsding to you or not
if "responding" not in db.keys():
  db["responding"] = True

# Add a new message to the db of healing
def update_healing(healing_msg):
  if "healing" in db.keys(): # check if the key exists
    healing = db["healing"] # get the current value
    healing.append(healing_msg) # add the new message to the list
    db["healing"] = healing # update the database
  else:
    db["healing"] = [healing_msg] #create a db with the key

# Delete a message from the db of healing
def delete_healing(index):
  healing = db["healing"]  # Get the list of depress in db
  index = int(index)
  if len(healing) > index:  # Check if the index is valid
    del healing[index]  # Delete the message at the given index
    db["healing"] = healing


def get_ball():
  page = random.randint(1, 12)
  url = f"https://dragonball-api.com/api/characters?page={page}&limit=5"
  response = requests.get(url)
  if response.status_code == 200:  # Success
    json_data = json.loads(response.text)
    return json_data["items"]  # return list of character under "items" key
  else:
    print(f"Error: Unable to fetch data. Status code: {response.status_code}")
    return None

def get_pokemon_random():
  random_id = random.randint(1, 1025)
  url = f"https://pokeapi.co/api/v2/pokemon/{random_id}"
  response = requests.get(url)
  if response.status_code == 200:
    json_data = response.json()
    name = json_data["species"]["name"]
    art = json_data["sprites"]["front_default"]
    cries = json_data["cries"]["legacy"]
    return name, art, cries
  else:
    print(f"Error: Unable to fetch data. Status code: {response.status_code}")
    return None

def get_pokemon(name):
  url = f"https://pokeapi.co/api/v2/pokemon/{name}"
  response = requests.get(url)
  if response.status_code == 200:
    json_data = response.json()
    name = json_data["species"]["name"]
    art = json_data["sprites"]["front_default"]
    stats = json_data["stats"]
    return name, art, stats
  else:
    print(f"Error: Unable to fetch data. Status code: {response.status_code}")
    return None

def get_pokemon_evolution_line(name):
  gettingChain = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{name}")
  name = gettingChain.json()["name"]
  evolution_chain_url = gettingChain.json()["evolution_chain"]["url"]
  pokedex_number = gettingChain.json()["id"]
  # json_data = gettingId.json()
  # id = json_data["id"]
  response = requests.get(evolution_chain_url)
  if response.status_code == 200:
    return response.json(), name, pokedex_number

intents = discord.Intents.default()
intents.message_content = True  # Specify that the bot needs to read message content

client = discord.Client(intents=intents)


@client.event  #this is how you define an event
async def on_ready():  #this is the event
  print('We have logged in as {0.user}.format(client)'
        )  #this is what the bot will say when it logs in


@client.event
async def on_message(
    message):  # triggers when a message is received but not from ourself
  if message.author == client.user:
    return
  options = anti_depresses
  if "healing" in db.keys():
    options = options + list(db["healing"]) # Add the default list with the user new stuff they added
  msg = message.content
  if message.content.startswith(
      '$nah'):  # this show that the bot have received something $
    await message.channel.send("Nah I'd Win")
  ############################ Add new word ############################
  if msg.startswith("$new"):
    healing_msg = msg.split("$new ", 1)[1]  # break off the message so we don't add $new into the db
    update_healing(healing_msg)
    await message.channel.send(f"New healing message **{healing_msg}** added.")
   ############################ Remove new word ############################
  if msg.startswith("$del"):
    if "healing" in db.keys(): # if the delete element exist in the db
      index = msg.split("$del ", 1)[1]
      if index.isdigit():
        delete_healing(index)
      else:
        await message.channel.send("Please enter a valid index.")
      healing_after_change = db["healing"]
      await message.channel.send(f"Healing list: {healing_after_change}")
    else:
      await message.channel.send("No index found")
   ############################ Get the list of word############################
  if msg.startswith("$list"):
    healing = []
    if "healing" in db.keys():
      healing = db["healing"]
    await message.channel.send(healing)
  ############################ Turn off or on the responding mode############################
  if msg.startswith("$responding"):
    value = msg.split("$responding ", 1)[1]
    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is **on**.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is **off**.")
  ############################ DRAGON BALL ############################
  if msg.startswith('$ball'):
    characters = get_ball()
    if characters:
      char = random.choice(characters)
      name = char.get("name", "Unknown")
      ki = char.get("ki", "Unknown")
      image_url = char.get("image", "Unknown")
      await message.channel.send(f"**{name}**")
      await message.channel.send(f"KI: **{ki}**")
      await message.channel.send(image_url)
  ############################ Random Pokemon ############################
  if msg.startswith('$pokemonRandom'):
    pokemon_data = get_pokemon_random()
    if pokemon_data:
      name, art, cries = pokemon_data
      await message.channel.send(f"**{name}**")
      await message.channel.send(art)
      if cries:
        await message.channel.send(f"🔊 Cry: {cries}")
      else:
        await message.channel.send("No cry found.")
  ############################ Pokemon Line ############################
  if msg.startswith('$pokeLine'):
    name = message.content[len("$pokeLine "):].strip()
    pokemon_data = get_pokemon_evolution_line(name)
    if pokemon_data:
      evolution_chain, name, pokedex_number = pokemon_data
      stack = [evolution_chain["chain"]]  # start with the root node
      while stack:
        current = stack.pop()
        species_name = current["species"]["name"]
        pokemon = get_pokemon(species_name)
        art = pokemon[1] if pokemon else None

        await message.channel.send(f"**{species_name.title()}**")
        await message.channel.send(f"**Pokedex Number: {pokedex_number}**")
        if art:
          await message.channel.send(art)

        # Add all evolutions to the stack to process next
        for evo in current["evolves_to"]:
          stack.append(evo)
        
      
      
    
  ############################ Pokemon ############################
  if msg.startswith('$pokemon'):
    name = message.content[len("$pokemon "):].strip()
    pokemon_data = get_pokemon(name)
    if pokemon_data:
      name, art, stats = pokemon_data
      await message.channel.send(f"**{name}**")
      await message.channel.send(art)
      await message.channel.send("**STAT:**")
      for i in range(6):
        await message.channel.send(f"{stats[i]['stat']['name']}: {stats[i]['base_stat']}")
    else:
      await message.channel.send("**Write correctly Bozo**")
  ############################ Response to sad Word ############################
  if any(word in msg for word in depresses) and db["responding"]:  # if the message contains any word in the list
    await message.channel.send(random.choice(options))
# Still need to run the bot
token = os.getenv('TOKEN')  # Hide token
if token is None:
  raise ValueError("TOKEN environment variable not set")

keep_alive()
client.run(token)
