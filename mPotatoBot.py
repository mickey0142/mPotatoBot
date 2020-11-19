import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from AmongPlayer import AmongPlayer

load_dotenv()

# create a file name .env and put DISCORD_TOKEN=token in there
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord')

players = []
roomCode = '??????'

@bot.command(
    name='ping',
    help='ทดสอบ bot | !ping',
    brief='ทดสอบ bot | !ping'
)
async def ping(ctx):
    await ctx.send('pong')


@bot.command(
    name='listPlayer',
    help='โชว์รายชื่อผู้เล่น | !listPlayer',
    brief='โชว์รายชื่อผู้เล่น | !listPlayer',
)
async def listPlayer(ctx):
    await displayPlayerList(ctx)

@bot.command(
    name='addPlayer',
    help='เพิ่มผู้เล่นลงในรายชื่อ | !addPlayer name',
    brief='เพิ่มผู้เล่น | !addPlayer name'
)
async def addPlayer(ctx, playerName):
    added = False
    voice_channel = bot.get_channel(777150058848190465)
    members = voice_channel.members
    for member in members:
        print(f'member name is {member.name}')
        if member.name == playerName or member.nick == playerName:
            added = True
            amongPlayer = AmongPlayer()
            amongPlayer.member = member
            players.append(amongPlayer)
            break
    if added:
        await ctx.send(f'เพิ่มผู้เล่น {playerName} เรียบร้อยแล้ว')
        print(f'{playerName} added')
    else:
        await ctx.send(f'หาผู้เล่นชื่อ {playerName} ไม่เจอ!')
        print(f'{playerName} not found')

@bot.command(
    name='removePlayer',
    help='ลบผู้เล่นออกจากรายชื่อ | !removePlayer playerName',
    brief='ลบผู้เล่นออกจากรายชื่อ | !removePlayer playerName'
)
async def removePlayer(ctx, playerName):
    try:
        index = int(playerName) - 1
        displayName = players[index].member.name
    except ValueError:
        displayName = playerName
    except IndexError:
        await ctx.send(f'เลขผู้เล่นผิด!')
        return
    removed = False
    for player in players:
        if player.member.name == displayName or player.member.nick == displayName:
            removed = True
            players.remove(player)
    if (removed):
        await ctx.send(f'ลบผู้เล่น {displayName} เรียบร้อยแล้ว')
        print(f'{displayName} removed')
    else:
        await ctx.send(f'หาผู้เล่นชื่อ {displayName} ไม่เจอ!')
        print(f'{displayName} not found')

@bot.command(
    name='clearPlayer',
    help='ลบผู้เล่นทั้งหมดออกจากรายชื่อ | !clearPlayer',
    brief='ลบผู้เล่นทั้งหมดออกจากรายชื่อ | !clearPlayer'
)
async def clearPlayer(ctx):
    players.clear()
    await ctx.send('ลบผู้เล่นออกจากรายชื่อทั้งหมดเรียบร้อยแล้ว')

@bot.command(
    name='addAllPlayer',
    help='เพิ่มผู้เล่นทั้งหมดในห้องลงในรายชื่อผู้เล่น | !addAllPlayer channelName',
    brief='เพิ่มผู้เล่นทั้งหมดในห้องลงในรายชื่อผู้เล่น | !addAllPlayer channelName',
)
async def addAllPlayer(ctx, channelName):
    voice_channel = discord.utils.get(
        ctx.guild.channels,
        name=channelName,
        type=discord.ChannelType.voice
    )
    members = voice_channel.members
    players.clear()
    for member in members:
        amongPlayer = AmongPlayer()
        amongPlayer.member = member
        players.append(amongPlayer)
    await displayPlayerList(ctx)

@bot.command(
    name='mute',
    help='ปิดไมค์ทุกคนที่อยู่ในรายชื่อ | !mute',
    brief='ปิดไมค์ทุกคน | !mute'
)
async def mute(ctx):
    for player in players:
        await player.member.edit(mute=True)
    await ctx.send('ปิดไมค์ทุกคนเรียบร้อยแล้ว')

@bot.command(
    name='unmute',
    help='เปิดไมค์ทุกคนที่อยู่ในรายชื่อ | !unmute',
    brief='เปิดไมค์ทุกคน | !unmute'
)
async def unmute(ctx):
    for player in players:
        if player.alive:
            await player.member.edit(mute=False)
    await ctx.send('เปิดไมค์ทุกคน (ที่ยังรอด) เรียบร้อยแล้ว')

@bot.command(
    name='dead',
    help='เซ็ตว่าผู้เล่นคนนี้ตายแล้ว | !dead playerName',
    brief='เซ็ตว่าผู้เล่นคนนี้ตายแล้ว | !dead playerName'
)
async def dead(ctx, playerName):
    try:
        index = int(playerName) - 1
        displayName = players[index].member.name
    except ValueError:
        displayName = playerName
    except IndexError:
        await ctx.send(f'เลขผู้เล่นผิด!')
        return
    for player in players:
        if player.member.name == displayName or player.member.nick == displayName:
            player.alive = False
            break
    # await ctx.send(f'{displayName} ตาย')
    await displayPlayerList(ctx)

@bot.command(
    name='alive',
    help='เซ็ตว่าผู้เล่นคนนี้ยังไม่ตาย | !alive playerName',
    brief='เซ็ตว่าผู้เล่นคนนี้ยังไม่ตาย | !alive playerName'
)
async def alive(ctx, playerName):
    try:
        index = int(playerName) - 1
        displayName = players[index].member.name
    except ValueError:
        displayName = playerName
    except IndexError:
        await ctx.send(f'เลขผู้เล่นผิด!')
        return
    for player in players:
        if player.member.name == displayName or player.member.nick == displayName:
            player.alive = True
            break
    # await ctx.send(f'{displayName} ยังไม่ตาย!')
    await displayPlayerList(ctx)

@bot.command(
    name='restartGame',
    help='รีเซ็ตสถานะผู้เล่นทุกคน | !restartGame',
    brief='รีเซ็ตสถานะผู้เล่นทุกคน | !restartGame'
)
async def restartGame(ctx):
    for player in players:
        await player.member.edit(mute=False)
        player.alive = True
    # await ctx.send('เริ่มเกมใหม่เรียบร้อย')
    await displayPlayerList(ctx)

@bot.command(
    name='setRoomCode',
    help='เซฟรหัสเข้าห้องเอาไว้ดู | !setRoomCode roomCode',
    brief='เซฟรหัสเข้าห้องเอาไว้ดู | !setRoomCode roomCode'
)
async def setRoomCode(ctx, code):
    global roomCode = code
    await ctx.send(f'รหัสเข้าห้องคือ {roomCode}')

@bot.command(
    name='code',
    help='ดูรหัสเข้าห้อง | !code',
    brief='ดูรหัสเข้าห้อง | !code'
)
async def showRoomCode(ctx):
    await ctx.send(f'รหัสเข้าห้องคือ {roomCode}')

@bot.event
async def on_command_error(ctx, error):
    # catch error here
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('คุณไม่มี Role ที่สามารถใช้คำสั่งนี้ได้')
    elif 'Target user is not connected to voice' in str(error.args[0]):
        await ctx.send('มีผู้เล่นในรายชื่อไม่ได้อยู่ในห้องคุย!')
    else:
        await ctx.send(error.args[0])

async def displayPlayerList(ctx):
    response = f'ตอนนี้มีคนเล่น {len(players)} คน\n'
    print(f'there is {len(players)} players')
    count = 1
    for player in players:
        if player.alive:
            status = 'รอด'
        else:
            status = 'ตาย'
        response += f'{count}. {player.member.name} | สถานะ : {status}\n'
        print(f'player name is {player.member.name}')
        count += 1
    await ctx.send(response)

bot.run(TOKEN)