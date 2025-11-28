# bot.py (run this locally)
from email.mime import message
import discord
import importlib
import json
import os
from dotenv import load_dotenv
from state_manager import StateManager

load_dotenv()

# load token from env for safety
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print('ERROR: set DISCORD_TOKEN in your environment')
    raise Exception('No DISCORD_TOKEN')


sm = StateManager('state.json')

class TutorBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (id: {self.user.id})')


    async def on_message(self, message):
        # ignore ourselves
        if message.author.id == self.user.id:
            return

        # simple command prefix to trigger students: !run <text>
        content = message.content.strip()
        if not content.startswith('!run'):
            return

        payload = content[len('!run'):].strip()
        # load student code fresh each message
        try:
            import student_code
            importlib.reload(student_code)
        except Exception as e:
            await message.channel.send(f'Bot error loading student code: {e}')
            return


        user_state = sm.get_state(str(message.author.id))
        try:
            result = student_code.student_handle(payload, user_state)
        except Exception as e:
            await message.channel.send(f'Error in student code: {e}')
            return


        # Expect result to be dict with output and state
        if not isinstance(result, dict) or 'output' not in result:
            await message.channel.send('student_handle must return a dict with key "output"')
            return

        sm.set_state(str(message.author.id), result.get('state', user_state))
        await message.channel.send(result['output'])


intents = discord.Intents.default()
intents.message_content = True


client = TutorBot(intents=intents)
client.run(TOKEN)