import discord
from datetime import datetime, timedelta
import os
import traceback

token = os.environ['DISCORD_BOT_TOKEN']
server_id = os.environ['SERVER_ID']

client = discord.Client()

@client.event
async def on_voice_state_update(member, before, after): 
    if member.guild.id == server_id and (before.channel != after.channel):
        now = datetime.utcnow() + timedelta(hours=9)
        alert_channel = client.get_channel('vc-announce')
        if before.channel is None: 
            embed = discord.Embed()
            embed.set_author(name=f'{member.name} が {after.channel.name} に入室しました',icon_url=member.avatar_url)
            embed.set_footer(text=f'{now:%m/%d-%H:%M}', icon_url='https://i.imgur.com/W8GarKw.png')
            await alert_channel.send(embed=embed)
        elif after.channel is None: 
            embed = discord.Embed()
            embed.set_author(name=f'{member.name} が {after.channel.name} から退出しました',icon_url=member.avatar_url)
            embed.set_footer(text=f'{now:%m/%d-%H:%M}', icon_url='https://i.imgur.com/AgUTwvD.png')
            await alert_channel.send(embed=embed)

client.run(token)