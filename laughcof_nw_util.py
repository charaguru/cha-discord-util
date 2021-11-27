import discord
from datetime import datetime, timedelta
import os
import traceback
import yaml

settings = {}

with open('./settings.yaml', 'r', encoding="utf-8") as f:
    settings = yaml.safe_load(f)['settings']

token = settings['token']

server_id = int(settings['server_id'])

attack_tx_id = int(settings['attack_tx_id'])
defence_tx_id = int(settings['defence_tx_id'])
flanker_tx_id = int(settings['flanker_tx_id'])

attack_vc_id = int(settings['attack_vc_id'])
defence_vc_id = int(settings['defence_vc_id'])
flanker_vc_id = int(settings['flanker_vc_id'])

listen_only_member_ids = settings['listen_only_member_ids']

default_party = {}

client = discord.Client()

# 起動確認
@client.event
async def on_ready():
    print("起動しました")
    await client.get_channel(attack_tx_id).send('起動しました')

# コマンド設定
@client.event
async def on_message(message):
    # メッセージの送信者がbot自身で無い
    if message.author == client.user:
        return

    # チャンネルが拠点戦チャットのいずれか
    if message.channel.id not in (attack_tx_id, defence_tx_id, flanker_tx_id):
        return 

    # 全集合
    if message.content.startswith('$group all'):
        attack_vc = client.get_channel(attack_vc_id)
        defence_vc = client.get_channel(defence_vc_id)
        flanker_vc = client.get_channel(flanker_vc_id)

        print('---------')
        print(attack_vc)
        print(defence_vc)
        print(flanker_vc)

        print(attack_vc.members)
        print(defence_vc.members)
        print(flanker_vc.members)
        print('---------')

        for member in attack_vc.members:
            default_party[member] = attack_vc
            await member.move_to(attack_vc)
        
        for member in defence_vc.members:
            print(member)
            default_party[member] = defence_vc
            await member.move_to(attack_vc)

        for member in flanker_vc.members:
            default_party[member] = flanker_vc
            await member.move_to(attack_vc)

        print('default_party = ')
        print(default_party)

    # 部隊戻し
    if message.content.startswith('$back'):
        attack_vc = client.get_channel(attack_vc_id)
        defence_vc = client.get_channel(defence_vc_id)
        flanker_vc = client.get_channel(flanker_vc_id)

        for member, vc in default_party.items():
            if vc is not None:
                await member.move_to(vc)

client.run(token)