# UoY Esport Bot Rewrite

## How to set up an instance of this bot

1. Clone this repository:
```console
$ git clone https://github.com/FragSoc/Esports-Bot-Rewrite.git
```

2. Change into the repo directory:
```console
$ cd Esports-Bot-Rewrite
```

3. Create a `secrets.env` file and edit it in your favourite text editor:
```console
$ vim secrets.env
```

4. Edit the below environment variables:
```console
DISCORD_TOKEN=
TWITCH_CLIENT_ID=
TWITCH_CLIENT_SECRET=
```

5. Run docker-compose:
```console
$ docker-compose up
```

## Current commands
<details>
<summary>Voicemaster</summary>

### Voicemaster

##### !setvmmaster {channel_id}
Make the given ID a Voicemaster master

##### !getvmmasters
Get all the Voicemaster masters in the server

##### !removevmmaster {channel_id}
Remove the given ID as a Voicemaster master

##### !removeallmasters
Remove all Voicemaster masters from the server

##### !killallslaves
Kill all the Voicemaster slave channels in the server

##### !lockvm
Locks the Voicemaster slave you're currently in to the number of current members

##### !unlockvm
Unlocks the Voicemaster slave you're currently in
</details>

<details>
<summary>Default Role</summary>

### Default role

##### !setdefaultrole {@role or role_id}
Set the default role to the @'ed role or given role ID

##### !getdefaultrole
Gets the current default role value

##### !removedefaultrole
Removes the current default role
</details>

<details>
<summary>Log Channel</summary>

### Log Channel

##### !setlogchannel {#channel or channel_id}
Set the log channel to the #'ed channel or given role ID

##### !getlogchannel
Gets the current log channel value

##### !removelogchannel
Removes the current log channel value
</details>

<details>
<summary>Administrator Tools</summary>

### Administrator Tools

##### !clear
Clear the specified number of messages from the current text channel

##### !members
List the current number of members in the server
</details>

<details>
<summary>Twitter Integration</summary>

### Twitter Integration

##### !addtwitter {twitter_handle} {#channel or channel_id}
Add a Twitter handle to notify in the specified channel when they tweet or quote retweet

##### !removetwitter {twitter_handle}
Remove the given Twitter handle from notifications

##### !changetwitterchannel {twitter_handle} {#channel or channel_id}
Change the notify channel for the given Twitter handle

##### !getalltwitters
List all the current Twitter handles configured in the server
</details>

<details>
<summary>Twitch Integration</summary>

### Twitch Integration

##### !addtwitch {twitch_handle} {#channel or channel_id}
Add a Twitch handle to notify in the specified channel when they go live

##### !addcustomtwitch {twitch_handle} {#channel or channel_id} "{custom_message}"
Add a Twitch handle to notify in the specified channel when they go live using the placeholders - handle, game, title and link

##### !edittwitch {twitch_handle} {#channel or channel_id}
Edit a configured Twitch handle to use a different channel

##### !editcustomtwitch {twitch_handle} "{custom_message}"
Edit a configured Twitch handle to display a custom message using the placeholders - handle, game, title and link

##### !removetwitch {twitch_handle}
Remove the specified twitch handle from alerting

##### !removealltwitch 
Remove all the Twitch alerts in the guild

##### !getalltwitch
List all the current Twitch handles configured in the server

</details>
