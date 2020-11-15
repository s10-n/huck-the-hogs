import os,discord,score,pig_roll,random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class Player:
    def __init__(self, name, total_score, current_score, is_my_turn):
        self.name = name
        self.total_score = total_score
        self.current_score = current_score
        self.is_my_turn = is_my_turn

bot = commands.Bot(command_prefix='!')
print('Huck the Hogs successfully initiated.')

current_player = 0
players_can_join = False
game_initialized = False
game_on = False
players = []

# initialize the game
@bot.command(name='h') # adjust to !huckthehogs when complete
async def init_game(ctx):
    global game_on
    global game_initialized
    if not game_on and not game_initialized:
        global players
        global players_can_join
        game_initialized = True
        players_can_join = True
        players = []
        print('Game initialized.')
        embed_var = discord.Embed(title='Welcome to Huck the Hogs!',description='Use the **!join** command to join the game.\nUse **!quit** at any time to exit the game.')
        await ctx.send(embed=embed_var)

@bot.command(name='quit')
async def quit_game(ctx):
    global current_player
    global players_can_join
    global game_initialized
    global game_on
    global players
    current_player = 0
    players_can_join = False
    game_initialized = False
    game_on = False
    players = []
    embed_var = discord.Embed(title='Game exited.',description='Thanks for playing!')
    await ctx.send(embed=embed_var)
    
        # allow players to join the game
@bot.command(name='join')
async def join_game(ctx):
    global players_can_join
    global players
    if players_can_join:
        user_ID = format(ctx.author.id)
        if not any(player.name == user_ID for player in players):         
            players.append(Player(user_ID,0,0,False))
            if len(players) > 1:
                embed_var = discord.Embed(description=f'<@{ctx.author.id}> has joined the game.\n{len(players)} players so far.\n\nUse **!start** to begin when all players have joined.')
            else:
                embed_var = discord.Embed(description=f'<@{ctx.author.id}> has joined the game.\n{len(players)} player so far.\n\nUse **!start** to begin when all players have joined.')
        else:
            embed_var = discord.Embed(description=f'<@{ctx.author.id}> has already joined the game!\n\nUse **!start** to begin when all players have joined.')
            print(players)
        await ctx.send(embed=embed_var)


@bot.command(name='start')
async def start_game(ctx):
    global players_can_join
    global game_on
    global players
    roller_ID = format(ctx.author.id)
    list_of_players = []
    for player in players:
        list_of_players.append(player.name)
    if roller_ID in list_of_players and not game_on:
        game_on = True
        players_can_join = False
        print('Game started')
        embed_var = discord.Embed(title="Let's huck some hogs!",description=f"<@{players[0].name}> goes first.\n Use **!roll** to roll the pigs.")
        global current_player
        players[current_player].is_my_turn = True
        await ctx.send(embed=embed_var)


@bot.command(name='roll')
async def player_roll(ctx):
    global current_player
    global players
    # determine that the player who !rolled is actually playing
    roller_ID = format(ctx.author.id)
    for player in players:
        if player.name == roller_ID and player.is_my_turn:
            #set that player as the current player
            print(f"{player.name}'s turn.")
            embed_var = discord.Embed(description=f"<@{player.name}>'s turn.")
            initial_roll = score.scoring(pig_roll.pig_roll(),pig_roll.pig_roll())

            # Player rolls a Pig Out
            if initial_roll['name'] == 'Pig Out':
                player.is_my_turn = False
                player.current_score = 0
                embed_var.add_field(name=f"{initial_roll['name']}",value=f"Total score: {player.total_score} points")
                if current_player == (len(players) - 1):
                    current_player = 0
                else:
                    current_player += 1
                players[current_player].is_my_turn = True
                embed_var.add_field(name='Next player:',value=f"<@{players[current_player].name}>",inline=False)

            # Player rolls an Oinker
            elif initial_roll['name'] == 'Oinker':
                player.is_my_turn = False
                player.current_score = 0
                player.total_score = 0
                embed_var.add_field(name=f"{initial_roll['name']}",value=f"Total score: {player.total_score} points")
                if current_player == (len(players) - 1):
                    current_player = 0
                else:
                    current_player += 1
                players[current_player].is_my_turn = True
                embed_var.add_field(name='Next player:',value=f"<@{players[current_player].name}>",inline=False)

            # Player rolls anything else
            else:
                player.current_score += initial_roll['score']
                print(player.current_score)
                embed_var.add_field(name=f"{initial_roll['name']} [+ {initial_roll['score']} points]",value=f"Score this turn: {player.current_score} points\nTotal score: {player.total_score + player.current_score} points")
                if player.current_score + player.total_score >= 100:
                    embed_var.add_field(name='You win!',value='Use **!huckthehogs** to play again.',inline=False)
                    global players_can_join
                    global game_initialized
                    global game_on
                    current_player = 0
                    players_can_join = False
                    game_initialized = False
                    game_on = False
                    players = []
                else:
                    embed_var.add_field(name='\u200b',value='Use **!roll** to roll again or **!pass** to move to the next player.',inline=False)
            await ctx.send(embed=embed_var)

@bot.command(name='pass')
async def player_pass(ctx):
    global current_player
    global players
    # determine that the player who !rolled is actually playing
    roller_ID = format(ctx.author.id)
    for player in players:
        if player.name == roller_ID and player.is_my_turn:
            embed_var = discord.Embed()
            player.is_my_turn = False
            player.total_score += player.current_score
            embed_var.add_field(name=f"Passed",value=f"Turn score: {player.current_score} points\nTotal score: {player.total_score} points")
            player.current_score = 0
            if current_player == (len(players) - 1):
                current_player = 0
            else:
                current_player += 1
            players[current_player].is_my_turn = True
            embed_var.add_field(name='Next player:',value=f"<@{players[current_player].name}>",inline=False)
            await ctx.send(embed=embed_var)

@bot.command(name='score')
async def show_score(ctx):
    if game_on:
        global players
        score_list = []
        for player in players:
            score_list.append({'name':player.name,'score':player.total_score})

        def get_score(player_score):
            return player_score.get('score')
        score_list.sort(key=get_score,reverse=True)           

        scoreboard_text = ''      
        for player_score in score_list:
            scoreboard_text += f"<@{player_score['name']}>: {player_score['score']} points\n"
        embed_var = discord.Embed()
        embed_var.add_field(name='Scores:',value=f'{scoreboard_text}')
        await ctx.send(embed=embed_var)

bot.run(TOKEN)
