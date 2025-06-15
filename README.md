# 🧠 Discord Mental Wellness & Pokémon Bot

A powerful and interactive Discord chatbot built in Python using `discord.py`, designed to support emotional well-being and add fun through Pokémon and Dragon Ball API integrations.

## 🌟 Features

### 🧠 Mental Wellness Support
- Detects negative emotions in messages (e.g., *"sad"*, *"depressed"*) and responds with positive encouragement.
- Users can:
  - `$new <message>` – Add their own uplifting messages to the bot.
  - `$del <index>` – Remove a specific custom message.
  - `$list` – View the current list of encouragement messages.
  - `$responding true/false` – Enable or disable automatic emotional support.

### 🔁 Persistent Customization
- Uses Replit DB to store custom user messages and bot state between restarts.

---

### 🔍 Pokémon Interaction (via PokéAPI)
- `$pokemon <name>` – Fetches a Pokémon's name, sprite, and base stats.
- `$pokemonRandom` – Returns a random Pokémon with its sprite and cry.
- `$pokeLine <name>` – Displays the full **evolution chain** of a Pokémon, including:
  - Branching evolutions (e.g., Eevee)
  - Sprites and names of each stage

> Case-insensitive commands supported (e.g., `$pokeLine CharmAnder` works fine).

---

### 🐉 Dragon Ball Fun
- `$ball` – Fetches a random **Dragon Ball character**, showing name, KI level, and an image.

---

## 🔧 Tech Stack
- **Language:** Python
- **Framework:** `discord.py`
- **APIs:**
  - [PokéAPI](https://pokeapi.co)
  - [Dragon Ball API](https://dragonball-api.com/)
- **Database:** [Replit DB](https://docs.replit.com/programming-ide/storing-persistent-data)

---

## 🧪 Example Commands

```bash
$pokemon Pikachu
$pokemonRandom
$pokeLine Eevee
$ball

$new You’re stronger than you think.
$del 0
$list
$responding false

