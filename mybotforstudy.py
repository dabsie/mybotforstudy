import os
import twitchio
import random
import datetime
import aiohttp
import requests
from twitchio.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('Oauth_TOKEN')
bot_nick = 'mybotforstudy'
client_id = os.getenv('CLIENT_ID1')
channel_name = 'shep4rd_gg'
bot_token1 = os.getenv('Oauth_TOKEN1')
followageID = os.getenv('followageClientID')
headers = {
    'Client-ID': followageID,
    'Authorization': f'Bearer {bot_token1}'
}


class Bot(twitchio.Client):

    def __init__(self):
        super().__init__(
            token=bot_token,
            client_secret=client_id,
            initial_channels=[channel_name]        
            )

    async def event_ready(self):
        print(f"{bot_nick} is ready to work on {channel_name}!")

    async def event_message(self, message):
        if message.author.name.lower() == bot_nick.lower():
            # игнорируем сообщения бота на себя же
            return
        else:
            if "!hello" in message.content.lower():
                await message.channel.send(f"Hello {message.author.name}!")

                
            elif "!socials" in message.content.lower():
                await message.channel.send("Мои соц. сети")
                await message.channel.send("VK: https://vk.com/dabsie")
                await message.channel.send("Instagram: instagram.com/666sdab")

            elif "!член" in message.content.lower():
                penis = random.randint(1, 30)
                await message.channel.send(f"Твой член: {penis}см")

            elif message.content.startswith('!followage'):
                await self.followage(message)

            elif "!commands" in message.content.lower():
                await message.channel.send("!followage - сколько ты подписан на меня")
                await message.channel.send("!hello - я затэгаю тебя")
                await message.channel.send("!socials - мои соц сетки")
                await message.channel.send("!член - твой огурчик в см")
    
    async def followage(self, message):
        # Получаем юзернэйм того кто затригерил
        follower_name = message.author.name
        
        # получаем id юзернэйма
        async with aiohttp.ClientSession() as session:
            user_info_url = f'https://api.twitch.tv/helix/users?login={follower_name}'
            headers = {'Client-Id': followageID, 'Authorization': f'Bearer {bot_token1}'}
            async with session.get(user_info_url, headers=headers) as response:
                user_info = await response.json()
                if 'data' not in user_info:
                    print(user_info)
                    return await message.channel.send(f'Error getting user ID for {follower_name}')
                user_id = user_info['data'][0]['id']
                print(user_id)

        # получаем id канала
        async with aiohttp.ClientSession() as session:
            channel_info_url = f'https://api.twitch.tv/helix/search/channels?query={channel_name}'
            headers = {'Client-Id': followageID, 'Authorization': f'Bearer {bot_token1}'}
            async with session.get(channel_info_url, headers=headers) as response:
                channel_info = await response.json()
                if 'data' not in channel_info:
                    print(channel_info)
                    return await message.channel.send(f'Error getting channel ID for {channel_name}')
                for streamer in channel_info['data']:
                    if streamer['broadcaster_login'] == channel_name:
                        channel_id = streamer['id']
                        print(channel_id)
                

        # узнаем статус фолова у юзера
        follow_info_url = 'https://api.twitch.tv/helix/users/follows'
        query_params = {'from_id': user_id, 'to_id': channel_id}
        response = requests.get(follow_info_url, headers=headers, params=query_params)
        data = response.json()

        if data['total'] > 0:
            # если фоловер то
            follow_date = data['data'][0]['followed_at']
            follow_date_time = datetime.datetime.fromisoformat(follow_date[:-1])
            current_date_time = datetime.datetime.utcnow()
            follow_age = current_date_time - follow_date_time
            
            # вывод
            days = follow_age.days
            hours = follow_age.seconds // 3600
            minutes = (follow_age.seconds // 60) % 60
            follow_age_string = f'@{follower_name} has been following for {days} days, {hours} hours, and {minutes} minutes.'
            await message.channel.send(follow_age_string)
        else:
            # юзел лох без фолова
            await message.channel.send(f'@{follower_name} are not following this channel.')


bot = Bot()
bot.run()
