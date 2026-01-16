# Discord Conversation Bot 🤖

An AI-powered Discord bot that can hold intelligent conversations using OpenAI's GPT models.

## Features

- 💬 **Intelligent Conversations**: Uses OpenAI's GPT for natural responses
- 🧠 **Memory**: Remembers conversation context per user
- 📨 **DM Support**: Chat privately with the bot
- 📢 **Server Support**: @mention the bot in any channel
- 🔄 **Reset Command**: Clear conversation history anytime

## Setup Instructions

### 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** and give it a name
3. Go to **"Bot"** section in the left sidebar
4. Click **"Reset Token"** and copy your bot token (save it!)
5. Enable these **Privileged Gateway Intents**:
   - ✅ Message Content Intent
6. Go to **"OAuth2" → "URL Generator"**:
   - Select scopes: `bot`
   - Select bot permissions: `Send Messages`, `Read Message History`
7. Copy the generated URL and open it to invite the bot to your server

### 2. Get OpenAI API Key

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key and copy it

### 3. Install & Run

```bash
# Navigate to project folder
cd discord-conversation-bot

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
copy .env.example .env

# Edit .env and add your tokens
notepad .env

# Run the bot
python bot.py
```

## Usage

| Action | How |
|--------|-----|
| Chat in DM | Just send a message to the bot |
| Chat in Server | @mention the bot with your message |
| Clear History | Type `!reset` |
| Get Help | Type `!help` |

## Example Conversation

```
You: @ConvoBot What's the capital of France?
Bot: The capital of France is Paris! 🗼

You: @ConvoBot Tell me more about it
Bot: Paris is not only the capital but also the largest city in France...
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Bot doesn't respond | Make sure Message Content Intent is enabled |
| "Invalid token" error | Double-check your DISCORD_TOKEN in .env |
| OpenAI error | Verify your OPENAI_API_KEY and check your credits |

## Files

```
discord-conversation-bot/
├── bot.py           # Main bot code
├── .env.example     # Environment template
├── .env             # Your secrets (create from template)
├── requirements.txt # Python dependencies
└── README.md        # This file
```
