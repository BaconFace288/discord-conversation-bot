"""
Discord Conversation Bot
An AI-powered Discord bot that can hold conversations using OpenAI's GPT models.
"""

import os
import discord
from discord.ext import commands
from openai import OpenAI
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables from .env file
load_dotenv()

# Configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate tokens
if not DISCORD_TOKEN:
    raise ValueError("[ERROR] DISCORD_TOKEN not found! Please add it to your .env file.")
if not OPENAI_API_KEY:
    raise ValueError("[ERROR] OPENAI_API_KEY not found! Please add it to your .env file.")

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Bot configuration
SYSTEM_PROMPT = """You are a friendly and helpful Discord bot assistant. You engage in natural conversations 
and help users with various tasks.

RESPONSE GUIDELINES:
- When asked questions, provide DETAILED and COMPREHENSIVE information
- Include relevant examples, explanations, and context to fully answer the question
- Break down complex topics into easy-to-understand parts
- Use bullet points, numbered lists, or formatting to organize information clearly
- Be thorough but still conversational and friendly
- Use occasional emojis to maintain an engaging tone
- If a topic is broad, cover multiple aspects of it

IMPORTANT CONTENT GUIDELINES - YOU MUST FOLLOW THESE STRICTLY:
- Keep ALL responses appropriate for PG-13 audiences (suitable for ages 13+)
- Do NOT use profanity, explicit language, or crude humor
- Avoid discussing violence, gore, or disturbing content in detail
- Do not engage with requests for adult content, illegal activities, or harmful information
- Keep discussions family-friendly and appropriate for all ages
- If asked about inappropriate topics, politely decline and redirect to appropriate conversation
- Be respectful and maintain a positive, wholesome tone at all times"""

MAX_HISTORY_LENGTH = 20  # Maximum messages to remember per user
MODEL = "gpt-3.5-turbo"  # Can change to "gpt-4" for better responses

# Store conversation history per user
# Format: {user_id: [{"role": "user/assistant", "content": "message"}, ...]}
conversation_history = defaultdict(list)

# Set up Discord bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
intents.dm_messages = True      # Required for DM support

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


def get_ai_response(user_id: int, user_message: str) -> str:
    """
    Get an AI response for a user's message, maintaining conversation history.
    
    Args:
        user_id: The Discord user's ID
        user_message: The message from the user
        
    Returns:
        The AI's response as a string
    """
    # Add user message to history
    conversation_history[user_id].append({
        "role": "user",
        "content": user_message
    })
    
    # Trim history if it's too long (keep recent messages)
    if len(conversation_history[user_id]) > MAX_HISTORY_LENGTH:
        conversation_history[user_id] = conversation_history[user_id][-MAX_HISTORY_LENGTH:]
    
    # Build messages for API call
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(conversation_history[user_id])
    
    try:
        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        # Extract the response text
        ai_message = response.choices[0].message.content
        
        # Add AI response to history
        conversation_history[user_id].append({
            "role": "assistant",
            "content": ai_message
        })
        
        return ai_message
        
    except Exception as e:
        # Remove the user message we added since the request failed
        conversation_history[user_id].pop()
        return f"Sorry, I encountered an error: {str(e)}"


def reset_conversation(user_id: int) -> None:
    """Clear the conversation history for a user."""
    conversation_history[user_id] = []


@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord."""
    print(f"{'='*50}")
    print(f"[BOT] Bot is online!")
    print(f"[NAME] Logged in as: {bot.user.name}")
    print(f"[ID] Bot ID: {bot.user.id}")
    print(f"{'='*50}")
    print(f"[OK] Ready to chat! Mention me or send a DM.")
    print(f"{'='*50}")


@bot.event
async def on_message(message: discord.Message):
    """Handle incoming messages."""
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Process commands first (like !reset, !help)
    await bot.process_commands(message)
    
    # Check if this is a command (starts with prefix)
    if message.content.startswith(bot.command_prefix):
        return
    
    # Determine if we should respond
    should_respond = False
    user_message = message.content
    
    # Always respond in DMs
    if isinstance(message.channel, discord.DMChannel):
        should_respond = True
    
    # Respond in servers when mentioned
    elif bot.user.mentioned_in(message):
        should_respond = True
        # Remove the mention from the message
        user_message = message.content.replace(f"<@{bot.user.id}>", "").strip()
        user_message = message.content.replace(f"<@!{bot.user.id}>", "").strip()
    
    if should_respond and user_message:
        # Show typing indicator while generating response
        async with message.channel.typing():
            response = get_ai_response(message.author.id, user_message)
        
        # Send the response
        # Discord has a 2000 character limit, so split long messages
        if len(response) <= 2000:
            await message.reply(response)
        else:
            # Split into chunks
            chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
            for i, chunk in enumerate(chunks):
                if i == 0:
                    await message.reply(chunk)
                else:
                    await message.channel.send(chunk)


@bot.command(name="reset")
async def reset_command(ctx: commands.Context):
    """Reset the conversation history for the user."""
    reset_conversation(ctx.author.id)
    await ctx.reply("🔄 Conversation reset! I've forgotten our previous chat. Let's start fresh!")


@bot.command(name="help")
async def help_command(ctx: commands.Context):
    """Show help information."""
    embed = discord.Embed(
        title="🤖 Conversation Bot Help",
        description="I'm an AI-powered bot that can chat with you!",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="💬 How to Chat",
        value="• **In DMs**: Just send me a message!\n• **In servers**: @mention me with your message",
        inline=False
    )
    
    embed.add_field(
        name="📝 Commands",
        value="• `!reset` - Clear our conversation history\n• `!help` - Show this help message",
        inline=False
    )
    
    embed.add_field(
        name="🧠 Memory",
        value=f"I remember up to {MAX_HISTORY_LENGTH} messages per conversation. Use `!reset` to start fresh!",
        inline=False
    )
    
    embed.set_footer(text="Powered by OpenAI GPT")
    
    await ctx.reply(embed=embed)


# Run the bot
if __name__ == "__main__":
    print("[STARTING] Discord Conversation Bot...")
    bot.run(DISCORD_TOKEN)
