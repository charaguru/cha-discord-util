import discord
from datetime import datetime, timedelta
import os
import traceback


# token = os.environ['DISCORD_BOT_TOKEN']
token = 'OTEzNzcxMTMxNjEyMzAzMzYx.YaDVrg.I2m5KKdqWjYcxXNCQWa9PUAb860' # bot トークン

# server_id = os.environ['SERVER_ID']

# server_id = 749892029995024414

# テスト用
server_id = 519741240611438592

# attack_tx_id = 893449686730559488
# defence_tx_id = 911447824376414228
# flanker_tx_id = 911446932667371550

# テスト用
attack_tx_id = 913777189571424316
defence_tx_id = 913777204851269712
flanker_tx_id = 913777225315287060

# attack_vc_id = 893449861712736326
# defence_vc_id = 911235942998765658
# flanker_vc_id = 911194715444101140

# テスト用
attack_vc_id = 913777726060642314
defence_vc_id = 913777742858838066
flanker_vc_id = 913777759015288862

default_party = {}

listen_only_member_ids = (
    911883459465728030, # きゃら
    911274250533486613  # えんそく
)

client = discord.Client()

# 起動確認
@client.event
async def on_ready():
    print("起動しました")
    await client.get_channel(attack_tx_id).send('起動しました')

# コマンド設定
@client.event
async def on_message(message):
    print('Message: ')
    print(message.content)

    # メッセージの送信者がbot自身で無い
    if message.author == client.user:
        return

    # チャンネルが拠点戦チャットのいずれか
    if message.channel.id not in (attack_tx_id, defence_tx_id, flanker_tx_id):
        return 

    # テスト
    if message.content.startswith('$hello'):
        await message.channel.send('Hello World!')

    # 全集合
    if message.content.startswith('$group all'):
        attack_vc = client.get_channel(attack_vc_id)
        defence_vc = client.get_channel(defence_vc_id)
        flanker_vc = client.get_channel(flanker_vc_id)

        for member in attack_vc.members:
            default_party[member] = attack_vc
            await member.move_to(attack_vc)
        
        for member in defence_vc.members:
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