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

# initialize the game
@bot.command(name='h')
async def init_game(ctx):
    players = []
    print('Game initialized.')
    embed_var = discord.Embed(title='Welcome to Huck the Hogs!',description='Use the !join command to join the game.')
    await ctx.send(embed=embed_var)

    # allow players to join the game
    @bot.command(name='join')
    async def join_game(ctx):
        user_ID = format(ctx.author.id)
        if not any(player.name == user_ID for player in players):         
            players.append(Player(user_ID,0,0,False))
            if len(players) > 1:
                embed_var = discord.Embed(description=f'<@{ctx.author.id}> has joined the game.\n{len(players)} players so far.')
            else:
                embed_var = discord.Embed(description=f'<@{ctx.author.id}> has joined the game.\n{len(players)} player so far.')
        else:
            embed_var = discord.Embed(description=f'<@{ctx.author.id}> has already joined the game!')
            print(players)
        await ctx.send(embed=embed_var)

        
    @bot.command(name='start')
    async def start_game(ctx):
        print('Game started')
        embed_var = discord.Embed(title="Let's huck some hogs!",description=f"<@{players[0].name}> goes first.\n Use !roll to roll the pigs.")
        await ctx.send(embed=embed_var)

        @bot.command(name='roll')
        async def player_roll(ctx):
            # determine that the player who !rolled is actually playing
            roller_ID = format(ctx.author.id)
            for player in players:
                if player.name == roller_ID:
                    #set that player as the current player
                    print(f"{player.name}'s turn.")
                    embed_var = discord.Embed(description=f"<@{player.name}>'s turn.")
                    initial_roll = score.scoring(pig_roll.pig_roll(),pig_roll.pig_roll())

                    # Player rolls a Pig Out
                    if initial_roll['name'] == 'Pig Out':
                        player.is_my_turn = False
                        player.current_score = 0
                        embed_var.add_field(name=f"{initial_roll['name']}",value=f"Total score: {player.total_score} points")

                    # Player rolls an Oinker
                    elif initial_roll['name'] == 'Oinker':
                        player.is_my_turn = False
                        player.current_score = 0
                        player.total_score = 0
                        embed_var.add_field(name=f"{initial_roll['name']}",value=f"Total score: {player.total_score} points")                 

                    # Player rolls anything else
                    else:
                        player.current_score += initial_roll['score']
                        embed_var.add_field(name=f"{initial_roll['name']} [+ {initial_roll['score']} points!]",value=f"Score this turn: {player.current_score} points.\nTotal score: {player.total_score + player.current_score} points")
                        embed_var.set_footer(text='Use !roll to roll again or !pass to move to the next player.')
                    await ctx.send(embed=embed_var)

              
            
        
bot.run(TOKEN)

