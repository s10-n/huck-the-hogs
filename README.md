# Huck the Hogs
A non-commercial Discord bot version of the dice game Pig, inspired by Pass the Pigs.

[Add to your Discord server](https://discord.com/api/oauth2/authorize?client_id=776352589088292874&permissions=0&scope=bot)

## How to play

Each turn involves the player rolling two hogs, each of which has a dot on one side. 
The player scores or loses points based on the way the hogs land (see [Scoring](#scoring) below).
The player's turn ends when they either roll a Pig Out (wiping their score for the turn) or an Oinker (wiping their score for the game) or when they pass the hogs to the next player.
The first player to reach 100 or more points wins.

## Commands

**!huckthehogs** - Initialize the game

**!join** - Join the server's current game (game must have been initialized)

**!start** - Start the server's game and start rolling (requires at least two players)

**!roll** - On your turn, roll the hogs

**!pass** - End your turn and keep your score for that turn

**!score** - View all player scores

**!quit** - Abandon the server's current game

## Scoring

### Single pig
Roll | Score
-----|------
![Single sider](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Sider%20(dot).png)Single sider (the hog is lying on its side)|0 points
![Razorback](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Razorback.png)Razorback (the hog is lying on its back)|5 points
![Trotter](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Trotter.png)Trotter (the hog is standing upright)|5 points
![Snouter](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Snouter.png)Snouter (the hog is leaning on its snout)|10 points
![Jowler](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Jowler.png)Jowler (the hog is resting on its snout and ear)|15 points

### Both pigs

Roll | Score
-----|------
![Dot sider](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Sider%20(dot).png)![Dot sider](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Sider%20(dot).png)Sider (both hogs are on the same side)|1 point
![Razorback](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Razorback.png)![Razorback](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Razorback.png)Double Razorback (both hogs are lying on their backs)|20 points
![Trotter](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Trotter.png)![Trotter](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Trotter.png)Double Trotter (both hogs are standing upright)|20 points
![Snouter](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Snouter.png)![Snouter](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Snouter.png)Double Snouter (both hogs are leaning on their snouts)|40 points
![Jowler](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Jowler.png)![Jowler](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Jowler.png)Double Jowler (both hogs are resting on their snout and ear)|60 points
![Razorback](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Razorback.png)![Dot sider](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Sider%20(dot).png)Mixed Combo (not listed above)|Combine single hogs' scores
![Dot sider](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Sider%20(dot).png)![No dot sider](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Sider%20(no%20dot).png)Pig Out (hogs are lying on opposite sides)|Turn score resets to zero and turn ends
![Oinker](https://raw.githubusercontent.com/s10-n/huck-the-hogs/main/images/Oinker.png)Oinker (hogs are touching)|Total score resets to zero and turn ends


