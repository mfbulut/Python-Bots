import discord
import asyncio

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_voice_state_update(member, before, after):
    if not after.self_mute:
        return

    delay = 10
    await asyncio.sleep(30)

    while member.name == 'mfurkan' and member.voice.self_mute:
        await member.send('Kendini susturmuşsun Açmayı unutma')
        await asyncio.sleep(delay)
        delay += 10
    

client.run('MTA1Mjk0MTk3NTUyNTAwMzMzNA.GiK244.N2W7Mc6onFp2_j6tgd7BkirxrZ6-pjqK8IeV9c')
