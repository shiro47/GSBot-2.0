
# Discord Bot

This project is a Python-based Discord bot that is specifically designed to cater to Apex Legends players. The bot offers a range of features that include building a leaderboard for server users, displaying the current map rotation, and providing information about the current Apex Predator threshold.

Additionally, the bot can register Twitch streamers and monitor their streaming status. It then sends this information to a designated text channel, ensuring that the server's members stay informed and up-to-date on their favorite streamers' activities.

## Tech Stack

- Python 3.11 
- Discord.py
- REST APIs (Twitch and Apex)
- MongoDB



## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

- `TOKEN`: This is a Discord token that you can obtain by creating your own Discord bot.

- `APEX_TOKEN`: You can obtain this token by visiting https://apexlegendsapi.com/.

- `TWITCH_CLIENT_ID`: You can obtain this ID by visiting https://dev.twitch.tv/docs/api/.

- `TWITCH_CLIENT_SECRET`: You can obtain this secret by visiting https://dev.twitch.tv/docs/api/.

- `MONGODB_PASSWORD`: This is the password for your MongoDB Atlas database.
## Features

This Python-based Discord bot offers a range of features designed to enhance the Apex Legends gaming experience for server members, including:

- This Discord bot has the ability to function on multiple servers concurrently.
- Registering and unregistering users to a leaderboard with validation.
- Generating a leaderboard and automatically updating it every hour.
- Creating a map rotation embed and regularly updating it every 10 minutes.
- Generating an embed with Apex Predator threshold and the total number of Masters and Predator players.
- Registering and unregistering Twitch streamers to a database with validation.
- Creating a list of currently live streaming Twitch streamers on a designated text channel and updating it every 7 minutes.
- These features help to create a more engaging and interactive server environment for Apex Legends enthusiasts, making it easy for members to stay connected and informed about the game and its community.

These features help to create a more engaging and interactive server environment for Apex Legends enthusiasts, making it easy for members to stay connected and informed about the game and its community.
## Demo

There are two ways you can try out this Discord bot:

- Create your own Discord bot and clone this repository to use the bot's code.

- Contact me and request an invite link to add the bot to your server.

You can reach me on discord: 

Shiro#1406
## Screenshots
**Leaderboard:**

![App Screenshot](https://i.postimg.cc/3xgXPNBM/leaderboard.png)
##
**Map rotation:**

![App Screenshot](https://i.postimg.cc/k5sxgHzf/map-rotation.png)
##
**Predator threshold:**

![App Screenshot](https://i.postimg.cc/d0w2vFHh/predator-treshold.png)
##
**Streamers list:**

![App Screenshot](https://i.postimg.cc/gJ03XDPd/streamers-list.png)
