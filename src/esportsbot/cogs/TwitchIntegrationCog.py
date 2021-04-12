import os
import time

import requests
from discord import Embed
from discord.ext import commands, tasks

from ..base_functions import get_cleaned_id
from ..db_gateway import db_gateway

EMPTY_EMBED = Embed(title="This is the stream title!",
                    url="https://twitch.tv/uoyesports")
EMPTY_EMBED.set_thumbnail(url="http://fragsoc.co.uk/wpsite/wp-content/uploads/2020/08/logo1-450x450.png")
EMPTY_EMBED.set_author(name="UoY Esports",
                       icon_url="http://fragsoc.co.uk/wpsite/wp-content/uploads/2020/08/logo1-450x450.png")
EMPTY_EMBED.add_field(name="Game", value="Game placeholder", inline=True)
EMPTY_EMBED.set_image(url="https://cdn.pixabay.com/photo/2014/02/27/16/10/tree-276014__340.jpg")
EMPTY_EMBED.set_footer(text="Come support our streamers!")


class TwitchIntegrationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twitch_handler = TwitchAPIHandler()
        self.live_checker.start()

    def cog_unload(self):
        self.live_checker.cancel()

    @commands.command()
    async def addtwitch(self, ctx, twitch_handle=None, announce_channel=None):
        if twitch_handle is not None and announce_channel is not None:
            # Check if Twitch channel has already been added
            twitch_in_db = db_gateway().get('twitch_info', params={
                'guild_id': ctx.author.guild.id, 'twitch_handle': twitch_handle.lower()})
            cleaned_channel_id = get_cleaned_id(
                announce_channel)
            channel_mention = "<#" + str(cleaned_channel_id) + ">"
            if not twitch_in_db:
                # Check user exists
                user_exists = bool(
                    self.twitch_handler.request_user(twitch_handle))
                if user_exists:
                    # Get live status of the channel
                    live_status = bool(self.twitch_handler.request_data(
                        [twitch_handle]))
                    # Insert Twitch channel into DB
                    db_gateway().insert('twitch_info', params={
                        'guild_id': ctx.author.guild.id, 'channel_id': cleaned_channel_id,
                        'twitch_handle': twitch_handle.lower(), 'currently_live': live_status})
                    await ctx.channel.send(
                        f"{twitch_handle} is valid and has been added, their notifications will be placed in {channel_mention}")
                else:
                    await ctx.channel.send(f"{twitch_handle} is not a valid Twitch handle")
            else:
                await ctx.channel.send(f"{twitch_handle} is already configured to {channel_mention}")
        else:
            await ctx.channel.send("You need to provide a Twitch handle and a channel")

    @commands.command()
    async def addcustomtwitch(self, ctx, twitch_handle=None, announce_channel=None, custom_message=None):
        if None not in (twitch_handle, announce_channel, custom_message):
            # Check if Twitch channel has already been added
            twitch_in_db = db_gateway().get('twitch_info', params={
                'guild_id': ctx.author.guild.id, 'twitch_handle': twitch_handle.lower()})
            cleaned_channel_id = get_cleaned_id(
                announce_channel)
            channel_mention = "<#" + str(cleaned_channel_id) + ">"
            if not twitch_in_db:
                # Check user exists
                user_exists = bool(
                    self.twitch_handler.request_user(twitch_handle))
                if user_exists:
                    # Get live status of the channel
                    live_status = bool(self.twitch_handler.request_data(
                        [twitch_handle]))
                    # Insert Twitch channel into DB
                    db_gateway().insert('twitch_info', params={
                        'guild_id': ctx.author.guild.id, 'channel_id': cleaned_channel_id,
                        'twitch_handle': twitch_handle.lower(), 'currently_live': live_status,
                        'custom_message': custom_message})
                    await ctx.channel.send(
                        f"{twitch_handle} is valid and has been added, their notifications will be placed in {channel_mention}")
                    sample_message = custom_message.format(
                        handle="TwitchHandle", game="Game/Genre", link="StreamLink", title="Title")
                    sample_embed = await self.create_embed(stream_title="Stream title here",
                                                           stream_thumbnail="http://fragsoc.co.uk/wpsite/wp-content/uploads/2020/08/logo1-450x450.png",
                                                           user_name="UoYEsports",
                                                           user_profile="http://fragsoc.co.uk/wpsite/wp-content/uploads/2020/08/logo1-450x450.png",
                                                           stream_game="Placeholder Game")
                    await ctx.channel.send(content=f"Sample custom message below\n {sample_message}",
                                           embed=sample_embed)
                else:
                    await ctx.channel.send(f"{twitch_handle} is not a valid Twitch handle")
            else:
                await ctx.channel.send(f"{twitch_handle} is already configured to {channel_mention}")
        else:
            await ctx.channel.send("You need to provide a Twitch handle, text channel and custom message")

    @commands.command()
    async def editcustomtwitch(self, ctx, twitch_handle=None, custom_message=None):
        if twitch_handle is not None and custom_message is not None:
            # Check if Twitch channel has already been added
            twitch_in_db = db_gateway().get('twitch_info', params={
                'guild_id': ctx.author.guild.id, 'twitch_handle': twitch_handle.lower()})
            if twitch_in_db:
                # Make DB edit
                db_gateway().update('twitch_info', set_params={
                    'custom_message': custom_message}, where_params={'guild_id': ctx.author.guild.id,
                                                                     'twitch_handle': twitch_handle.lower()})
                sample_message = custom_message.format(
                    handle="TwitchHandle", game="Game/Genre", link="StreamLink", title="Title")
                sample_embed = await self.create_embed(stream_title="Stream title here",
                                                       stream_thumbnail="http://fragsoc.co.uk/wpsite/wp-content/uploads/2020/08/logo1-450x450.png",
                                                       user_name="UoYEsports",
                                                       user_profile="http://fragsoc.co.uk/wpsite/wp-content/uploads/2020/08/logo1-450x450.png",
                                                       stream_game="Placeholder Game")
                await ctx.channel.send(content=f"Sample custom message below\n {sample_message}",
                                       embed=sample_embed)
            else:
                await ctx.channel.send("That Twitch handle is not configured in this server")
        else:
            await ctx.channel.send("You need to provide a Twitch handle, text channel and custom message")

    @commands.command()
    async def edittwitch(self, ctx, twitch_handle=None, announce_channel=None):
        if twitch_handle is not None and announce_channel is not None:
            # Check if Twitch channel has already been added
            twitch_in_db = db_gateway().get('twitch_info', params={
                'guild_id': ctx.author.guild.id, 'twitch_handle': twitch_handle.lower()})
            cleaned_channel_id = get_cleaned_id(
                announce_channel)
            channel_mention = "<#" + str(cleaned_channel_id) + ">"
            if twitch_in_db:
                # Make DB edit
                db_gateway().update('twitch_info', set_params={
                    'channel_id': cleaned_channel_id}, where_params={'guild_id': ctx.author.guild.id,
                                                                     'twitch_handle': twitch_handle.lower()})
                await ctx.channel.send(f"Changed the alerts for {twitch_handle} to {channel_mention}")
            else:
                await ctx.channel.send("The Twitch user mentioned is not configured in this server")
        else:
            await ctx.channel.send("You need to provide a Twitch handle and a channel")

    @commands.command()
    async def removetwitch(self, ctx, twitch_handle=None):
        if twitch_handle is not None:
            # Entered a Twitter handle
            twitch_handle = twitch_handle.lower()
            handle_exists = db_gateway().get('twitch_info', params={
                'guild_id': ctx.author.guild.id, 'twitch_handle': twitch_handle.lower()})
            if handle_exists:
                # Handle exists
                db_gateway().delete('twitch_info',
                                    where_params={'guild_id': ctx.author.guild.id,
                                                  'twitch_handle': twitch_handle.lower()})
                await ctx.channel.send(f"Alerts for {twitch_handle} have been removed from this server")
            else:
                await ctx.channel.send("Entered Twitch handle is not configured in this server")
        else:
            await ctx.channel.send("You need to provide a Twitch handle")

    @commands.command()
    async def removealltwitch(self, ctx):
        db_gateway().delete('twitch_info', where_params={
            'guild_id': ctx.author.guild.id})
        await ctx.channel.send("Removed all Twitch alerts from this server")

    @commands.command()
    async def getalltwitch(self, ctx):
        returned_val = db_gateway().get('twitch_info', params={
            'guild_id': ctx.author.guild.id})
        all_handles = "** **\n__**Twitch Alerts**__\n"
        for each in returned_val:
            channel_mention = "<#" + str(each['channel_id']) + ">"
            all_handles += f"{each['twitch_handle']} is set to alert in {channel_mention}\n"
        await ctx.channel.send(all_handles)

    @commands.command()
    async def test(self, ctx):
        await ctx.channel.send("TEST")
        returned_data = self.twitch_handler.request_data(["ryth_cs"])
        returned_user = self.twitch_handler.request_user("ryth_cs")
        print(f"DATA - {returned_data}")
        print(f"USER - {returned_user}")

    @tasks.loop(seconds=50)
    async def live_checker(self):
        print('TWITCH: Retrieving current statuses')
        time_taken = await self.get_and_compare_statuses(True)
        print(f'TWITCH: Retrieved current statuses in {time_taken}s')

    @live_checker.before_loop
    async def before_live_checker(self):
        print('TWITCH: Waiting until bot is ready')
        await self.bot.wait_until_ready()
        print('TWITCH: Updating current statuses')
        time_taken = await self.get_and_compare_statuses(False)
        print(f'TWITCH: Updated current statuses in {time_taken}s')

    async def get_and_compare_statuses(self, alert):
        start_time = time.time()
        all_twitch_handles = db_gateway().pure_return(
            'SELECT DISTINCT twitch_handle FROM "twitch_info"')
        if all_twitch_handles:
            # Create list of all twitch handles in the database
            twitch_handle_arr = list(x['twitch_handle']
                                     for x in all_twitch_handles)
            # Create dict consisting of twitch handles and live statuses
            twitch_status_dict = dict()
            all_twitch_statuses = db_gateway().pure_return(
                'SELECT DISTINCT twitch_handle, currently_live FROM "twitch_info"')
            for twitch_user in all_twitch_statuses:
                twitch_status_dict[twitch_user['twitch_handle']
                ] = twitch_user['currently_live']
            # Query Twitch to receive array of all live users
            returned_data = self.twitch_handler.request_data(
                twitch_handle_arr)
            # Loop through all users comparing them to the live list
            for twitch_handle in twitch_handle_arr:
                # if any(obj['user_name'].lower() == twitch_handle for obj in returned_data):
                handle_live = (next(
                    (obj for obj in returned_data if obj['user_name'].lower() == twitch_handle), False))
                print(handle_live)
                if handle_live:
                    # User is live
                    if not twitch_status_dict[f'{twitch_handle}']:
                        # User was not live before but now is
                        db_gateway().update('twitch_info', set_params={
                            'currently_live': True}, where_params={'twitch_handle': twitch_handle.lower()})
                        if alert:
                            # Grab all channels to be alerted
                            all_channels = db_gateway().get('twitch_info', params={
                                'twitch_handle': twitch_handle.lower()})
                            # Grab information on user
                            user_info = self.twitch_handler.request_user(handle_live['user_name'])
                            for each in all_channels:
                                # Send alert to specified channel to each['channel_id']
                                if each['custom_message'] is not None:
                                    custom_message = each['custom_message'].format(handle=handle_live['user_name'],
                                                                                   game=handle_live['game_name'],
                                                                                   link=f"https://twitch.tv/{handle_live['user_name']}",
                                                                                   title=handle_live['title'])
                                else:
                                    custom_message = f"** **\n{handle_live['user_name']} has just gone live!"
                                stream_embed = await self.create_embed(stream_title=handle_live['title'],
                                                                       stream_thumbnail=handle_live['thumbnail_url'],
                                                                       user_name=handle_live['user_name'],
                                                                       user_profile=user_info[0]['profile_image_url'],
                                                                       stream_game=handle_live['game_name'])
                                await self.bot.get_channel(each['channel_id']).send(content=custom_message,
                                                                                    embed=stream_embed)
                else:
                    # User is not live
                    db_gateway().update('twitch_info', set_params={
                        'currently_live': False}, where_params={'twitch_handle': twitch_handle.lower()})
        return round(time.time() - start_time, 3)

    async def create_embed(self, stream_title, stream_thumbnail, user_name, user_profile, stream_game):
        embed = Embed(title=stream_title, url=f"https://twitch.tv/{user_name}")
        embed.set_thumbnail(url=user_profile)
        embed.set_author(name=user_name, icon_url=user_profile)
        embed.add_field(name="Game", value=stream_game, inline=True)
        embed.set_image(url=stream_thumbnail.format(width="1920", height="1080"))
        embed.set_footer(text="Come support our streamers!")
        return embed


class TwitchAPIHandler:

    def __init__(self):
        self.client_id = os.getenv('TWITCH_CLIENT_ID')
        self.client_secret = os.getenv('TWITCH_CLIENT_SECRET')
        self.params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        self.token = None

    def base_headers(self):
        return {
            'Authorization': f'Bearer {self.token.get("access_token")}',
            'Client-ID': self.client_id
        }

    def generate_new_oauth(self):
        OAuthURL = 'https://id.twitch.tv/oauth2/token'
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        oauth_response = requests.post(OAuthURL, params)
        if oauth_response.status_code == 200:
            oauth_response_json = oauth_response.json()
            oauth_response_json['expires_in'] += time.time()
            self.token = oauth_response_json
            print("TWITCH: Generated new OAuth token")
            return self.token

    def request_data(self, twitch_handles):
        if self.token is None or self.token['expires_in'] < time.time():
            self.generate_new_oauth()
        data_url = 'https://api.twitch.tv/helix/streams?'
        data_url = data_url + "user_login=" + ("&user_login=".join(twitch_handles))
        data_response = requests.get(
            data_url, headers=self.base_headers(), params=self.params)
        print(data_response.json())
        return data_response.json()['data']

    def request_user(self, twitch_handle):
        if self.token is None or self.token['expires_in'] < time.time():
            self.generate_new_oauth()
        data_url = f'https://api.twitch.tv/helix/users?login={twitch_handle}'
        # data_url = data_url+"user_login="+("&user_login=".join(twitch_handles))
        data_response = requests.get(
            data_url, headers=self.base_headers(), params=self.params)
        print(data_response.json())
        return data_response.json()['data']


def setup(bot):
    bot.add_cog(TwitchIntegrationCog(bot))
