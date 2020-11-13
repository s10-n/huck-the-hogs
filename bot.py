import os, discord,score,roll,random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
print('Huck the Hogs successfully initiated.')

# initialize the game
@bot.command(name='h')
async def init_game(ctx):
    players = {}
    print('Game initialized.')
    embed_var = discord.Embed(title='Welcome to Huck the Hogs!',description='Use the !join command to join the game.')
    await ctx.send(embed=embed_var)

    # allow players to join the game
    @bot.command(name='join')
    async def join_game(ctx):
        username = format(ctx.author.id)
        if username not in players.keys():
            players[username] = 0
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
        players_list = list(players.keys())
        print('Game started')
        embed_var = discord.Embed(title="Let's huck some hogs!",description=f"<@{players_list[0]}> goes first.")
        await ctx.send(embed=embed_var)
        for player_id in players_list:
            turn_continues = True
            while turn_continues:
                embed_var = discord.Embed(description=f"<@{player_id}>'s turn.")
                initial_roll = score.scoring(roll.pig_roll(random.randint(1,201)),roll.pig_roll(random.randint(1,201)))

                # Player rolls a Pig Out
                if initial_roll['name'] == 'Pig Out':
                    embed_var.add_field(name=f"{initial_roll['name']}",value=f"Total score: {players[player_id]} points")

                # Player rolls an Oinker
                elif initial_roll['name'] == 'Oinker':
                    players[player_id] = 0
                    embed_var.add_field(name=f"{initial_roll['name']}",value=f"Total score: {players[player_id]} points")

                 
                
                else:
                    players[player_id] += initial_roll['score']
                    embed_var.add_field(name=f"{initial_roll['name']} [+ {initial_roll['score']} points!]",value=f"Total score: {players[player_id]} points")
                    embed_var.set_footer(text='Use !roll to roll again or !pass to move to the next player.')
                await ctx.send(embed=embed_var)
        
        
bot.run(TOKEN)

