import os,discord,score,pig_roll,random,image
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

current_games = {}
# set game variables to defaults

@bot.command(name='huckthehogs',help='Initialize the game') # initialize the game
async def init_game(ctx):
    print(ctx.message.guild.id)
    current_games[ctx.message.guild.id] = {'game_init':False,
                                           'game_on':False,
                                           'joinable':False,
                                           'player_list':[],
                                           'current_player':0}
    if not current_games[ctx.message.guild.id]['game_on'] and not current_games[ctx.message.guild.id]['game_init']:
        current_games[ctx.message.guild.id]['game_init'] = True # initialize the game
        current_games[ctx.message.guild.id]['joinable'] = True # start the game's join stage
        current_games[ctx.message.guild.id]['players'] = [] # reset the list of players
        print('Game initialized.')
        embed_var = discord.Embed(title='Welcome to Huck the Hogs!',
                                  description='Use the **!join** command to join the game.\nUse **!quit** at any time to exit the game.\nUse **!help** for a full overview of game commands.')
        await ctx.send(embed=embed_var)

# quit the game
@bot.command(name='quit',help="Abandon the server's current game")
async def quit_game(ctx):
    # reset all game values to the defaults
    current_games[ctx.message.guild.id]['current_player'] = 0 
    current_games[ctx.message.guild.id]['joinable'] = False 
    current_games[ctx.message.guild.id]['game_init'] = False
    current_games[ctx.message.guild.id]['game_on'] = False
    current_games[ctx.message.guild.id]['player_list'] = []
    embed_var = discord.Embed(title='Game exited.',
                              description='Thanks for playing!')
    await ctx.send(embed=embed_var)
   
# allow players to join the game
@bot.command(name='join',help="Join the server's current game (game must have been initialized)")
async def join_game(ctx):
    if current_games[ctx.message.guild.id]['joinable']: # ensure that the game is in the join phase
        user_ID = format(ctx.author.id)
        if not any(player.name == user_ID for player in current_games[ctx.message.guild.id]['player_list']): # check if the player who is trying to join has joined already
            current_games[ctx.message.guild.id]['player_list'].append(Player(user_ID,0,0,False))
            print(f'{ctx.author} has joined the game.')
            if len(current_games[ctx.message.guild.id]['player_list']) > 1: # check if the player is the first to join or not
                embed_var = discord.Embed(description=f"<@{ctx.author.id}> has joined the game.\n{len(current_games[ctx.message.guild.id]['player_list'])} players so far.\n\nUse **!start** to begin when all players have joined.")
            else:
                embed_var = discord.Embed(description=f"<@{ctx.author.id}> has joined the game.\n{len(current_games[ctx.message.guild.id]['player_list'])} player so far.\n\nUse **!start** to begin when all players have joined.")
        else: # 
            embed_var = discord.Embed(description=f'<@{ctx.author.id}> has already joined the game!\n\nUse **!start** to begin when all players have joined.')
        await ctx.send(embed=embed_var)

# start the game once all players have joined
@bot.command(name='start',help="Start the server's game and start rolling (requires at least two players)")
async def start_game(ctx):
    roller_ID = format(ctx.author.id)
    list_of_players = []
    for player in current_games[ctx.message.guild.id]['player_list']:
        list_of_players.append(player.name)
    if roller_ID in list_of_players and not current_games[ctx.message.guild.id]['game_on']: # check that the player who issued the command is actually playing
        if len(current_games[ctx.message.guild.id]['player_list']) < 2:
            embed_var = discord.Embed(description="Huck the Hogs requires at least two players.")
        else:
            current_games[ctx.message.guild.id]['game_on'] = True # start the game
            current_games[ctx.message.guild.id]['joinable'] = False # end the joining stage
            print('Game started')
            embed_var = discord.Embed(title="Let's huck some hogs!",
                                      description=f"<@{current_games[ctx.message.guild.id]['player_list'][0].name}> goes first.\n Use **!roll** to roll the hogs.")
            current_games[ctx.message.guild.id]['player_list'][current_games[ctx.message.guild.id]['current_player']].is_my_turn = True # set the first player to join as the current player
        await ctx.send(embed=embed_var)

# roll the pigs
@bot.command(name='roll',help='On your turn, roll the hogs')
async def player_roll(ctx):
    # determine that the player who !rolled is actually playing
    roller_ID = format(ctx.author.id)
    for player in current_games[ctx.message.guild.id]['player_list']:
        if player.name == roller_ID and player.is_my_turn:
            #set that player as the current player
            print(f"{ctx.author}'s turn.")
            embed_var = discord.Embed(description=f"<@{player.name}>'s turn.")
            roll1 = pig_roll.pig_roll()
            roll2 = pig_roll.pig_roll()
            
            roll = score.scoring(roll1,roll2) # roll two pigs and return a name and a score for the roll
            image.get_image(roll1,roll2)
            file = discord.File('images/rollimage.png', filename='rollimage.png')
            embed_var.set_image(url='attachment://rollimage.png')
            

            # Player rolls a Pig Out
            if roll['name'] == 'Pig Out':
                player.is_my_turn = False # end the player's turn
                player.current_score = 0 # reset the player's score for that turn
                embed_var.add_field(name=f"{roll['name']}",
                                    value=f"Total score: {player.total_score} points")
                # move to the next player
                if current_games[ctx.message.guild.id]['current_player'] == (len(current_games[ctx.message.guild.id]['player_list']) - 1): 
                    current_games[ctx.message.guild.id]['current_player'] = 0
                else:
                    current_games[ctx.message.guild.id]['current_player'] += 1
                current_games[ctx.message.guild.id]['player_list'][current_games[ctx.message.guild.id]['current_player']].is_my_turn = True # set the next player's turn
                embed_var.add_field(name='Next player:',
                                    value=f"<@{current_games[ctx.message.guild.id]['player_list'][current_games[ctx.message.guild.id]['current_player']].name}>",
                                    inline=False)

            # Player rolls an Oinker
            elif roll['name'] == 'Oinker':
                player.is_my_turn = False # end the player's turn
                player.current_score = 0 # reset the player's score for that turn
                player.total_score = 0 # reset the player's score for the entire game
                embed_var.add_field(name=f"{roll['name']}",
                                    value=f"Total score: {player.total_score} points")
                # move to the next player
                if current_games[ctx.message.guild.id]['current_player'] == (len(current_games[ctx.message.guild.id]['player_list']) - 1):
                    current_games[ctx.message.guild.id]['current_player'] = 0
                else:
                    current_games[ctx.message.guild.id]['current_player'] += 1
                current_games[ctx.message.guild.id]['player_list'][current_games[ctx.message.guild.id]['current_player']].is_my_turn = True # set the next player's turn
                embed_var.add_field(name='Next player:',
                                    value=f"<@{current_games[ctx.message.guild.id]['player_list'][current_games[ctx.message.guild.id]['current_player']].name}>",
                                    inline=False)

            # Player rolls anything else
            else:
                player.current_score += roll['score'] # add the score from the roll
                embed_var.add_field(name=f"{roll['name']} [+ {roll['score']} points]",
                                    value=f"Score this turn: {player.current_score} points\nTotal score: {player.total_score + player.current_score} points")
                if player.current_score + player.total_score >= 100: # check if player has won the game
                    embed_var.add_field(name='You win!',
                                        value='Use **!huckthehogs** to play again.',
                                        inline=False)
                    # reset game variables
                    current_games[ctx.message.guild.id]['current_player'] = 0
                    current_games[ctx.message.guild.id]['joinable'] = False
                    current_games[ctx.message.guild.id]['game_init'] = False
                    current_games[ctx.message.guild.id]['game_on'] = False
                    current_games[ctx.message.guild.id]['player_list'] = []
                else:
                    embed_var.add_field(name='\u200b', # prompt the player for their next action
                                        value='Use **!roll** to roll again or **!pass** to move to the next player.',
                                        inline=False)
            
            await ctx.send(file=file,embed=embed_var)

# player ends their turn and keeps their score
@bot.command(name='pass', help='End your turn and keep your score for that turn')
async def player_pass(ctx):
    # determine that the player who !rolled is actually playing
    roller_ID = format(ctx.author.id)
    for player in current_games[ctx.message.guild.id]['player_list']:
        if player.name == roller_ID and player.is_my_turn:
            embed_var = discord.Embed()
            player.is_my_turn = False # end the player's turn
            player.total_score += player.current_score # add their turn's score onto their total score
            embed_var.add_field(name=f"Passed",
                                value=f"Turn score: {player.current_score} points\nTotal score: {player.total_score} points")
            player.current_score = 0 # reset their current score
            # move to the next player
            if current_games[ctx.message.guild.id]['current_player'] == (len(current_games[ctx.message.guild.id]['player_list']) - 1):
                current_games[ctx.message.guild.id]['current_player'] = 0
            else:
                current_games[ctx.message.guild.id]['current_player'] += 1
            current_games[ctx.message.guild.id]['player_list'][current_games[ctx.message.guild.id]['current_player']].is_my_turn = True # set the next player as the current player
            embed_var.add_field(name='Next player:',
                                value=f"<@{current_games[ctx.message.guild.id]['player_list'][current_games[ctx.message.guild.id]['current_player']].name}>",
                                inline=False)
            await ctx.send(embed=embed_var)

# show the game's current score
@bot.command(name='score',help='View all player scores')
async def show_score(ctx):
    if current_games[ctx.message.guild.id]['game_on']: # check that a game is taking place
        score_list = []
        for player in current_games[ctx.message.guild.id]['player_list']:
            score_list.append({'name':player.name,'score':player.total_score}) # create a list of dictionaries with each player's name and total score
        score_list.sort(key=(lambda player_score: player_score.get('score')), # sort the list by score in descending order
                        reverse=True)           
        scoreboard_text = '' # create the string that holds the scoreboard text
        for player_score in score_list:
            scoreboard_text += f"<@{player_score['name']}>: {player_score['score']} points\n"
        embed_var = discord.Embed()
        embed_var.add_field(name='Scores:',value=f'{scoreboard_text}')
        await ctx.send(embed=embed_var)

bot.run(TOKEN)
