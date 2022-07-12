# from replit import db
# keys = db.keys()
# for row in keys:
#   del db[row]

import os
from os import system
from time import sleep
import discord
from keepAlive import keep_alive
from discord.ext import commands
from replit import db
from discord.ext.commands import has_permissions, MissingPermissions

my_secret = os.environ['Token']

listA = []
listB = []
listC = []

Admin = ['627139164537749505', '952814969097957377']


client = commands.Bot(command_prefix='+')

@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user}')

@client.command()
async def hello(ctx):
  async for message in ctx.channel.history(limit=1):
    await message.delete()
  await ctx.send("❈────────•✦•❅•✦•────────❈\n"
                   ":rotating_light: ★กระดานคำสั่งจากนายทะเบียนบ้านหูยาว★ :rotating_light:\n\n"

                  "+add <@name> 1   → เพิ่ม point (เฉพาะแอดมิน)\n"
                  "+cut <@name> 1   → ลด point (เฉพาะแอดมิน)\n\n"

                  ":bulb: CHECK POINT★ (ลูกบ้านสามารถใช้ได้ทุกคน) :bulb:\n\n"

                  "+show   → เช็ค point ตัวเอง\n"
                  "+s <@name>   → เช็ค point คนอื่น\n"
                  "+board   → เปิด LeaderBoard 25 อันดับแรก\n\n"

                  "❈────────•✦•❅•✦•────────❈\n")

def sort_list(list1, list2):
 
    zipped_pairs = zip(list2, list1)
 
    z = [x for _, x in sorted(zipped_pairs)]
     
    return z
def cal_board():
  global listA
  global listB
  global listC

  listA = []
  listB = []
  listC = []
  
  keys = db.keys()
  for row in keys:
    value = db[row]
    ch = isinstance(value,int)
    if ch == True:
      listA.append(row)
      listB.append(value)
  # print(listA)
  # print(listB)
  listC = sort_list(listA, listB)
  listC.reverse()

@client.command(pass_context = True)
@has_permissions(administrator = True)
async def whoami(ctx):
  await ctx.send('คุณเป็น administrator')

@whoami.error
async def whoami_error(ctx, error):
  if isinstance(error, MissingPermissions):
    text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
    await ctx.send(text)
  
@client.command()
@has_permissions(administrator = True)
async def add(ctx, player: discord.Member, input: int):
  sPlayer = str(player.id)
  np = 'n' + str(player.id)
  nPlayer = str(player.name)
  check = False
  keys = db.keys()
  for row in keys:
    if row == sPlayer:
      check = True
      break
  if check == True:
    value = db[sPlayer]
    cal = value + input
    db[sPlayer] = cal
    db[np] = nPlayer
  else:
    db[np] = nPlayer
    db[sPlayer] = input
  await ctx.channel.send('<@'+ sPlayer +'> add '+ str(input) +'★Star')

@add.error
async def add_error(ctx, error):
  if isinstance(error, MissingPermissions):
    text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
    await ctx.send(text)
  

@client.command()
@has_permissions(administrator = True)
async def cut(ctx, player: discord.Member, input: int): 
  sPlayer = str(player.id)
  np = 'n' + str(player.id)
  nPlayer = str(player.name)
  check = False
  keys = db.keys()
  for row in keys:
    if row == sPlayer:
      check = True
      break
  if check == True:
    value = db[sPlayer]
    cal = value - input
    if cal < 0:
      await ctx.channel.send('Error คะแนนติดลบ')
    else:
      db[sPlayer] = cal
      db[np] = nPlayer
      await ctx.channel.send('<@'+ sPlayer +'> del '+ str(input) +'★Star')
  else:
    await ctx.channel.send('<@'+ sPlayer +'> Not Found')
  
    
# @client.command()
# async def show(ctx):
#   sPlayer = str(ctx.author.id)
#   check = False
#   keys = db.keys()
#   for row in keys:
#     if row == sPlayer:
#       check = True
#       break
#   if check == True:
#     value = db[sPlayer]
#     print(sPlayer)
#     await ctx.channel.send('<@'+ sPlayer +'> have '+ str(value) +'★point')
#   else:
#     await ctx.channel.send('Not Found')
@client.command()
async def show(ctx):
  sPlayer = str(ctx.author.id)
  np = 'n' + str(ctx.author.id)
  nPlayer = str(ctx.author.name)
  check = False
  keys = db.keys()
  for row in keys:
    if row == sPlayer:
      check = True
      break
  if check == True:
    value = db[sPlayer]
    db[np] = nPlayer
    print(sPlayer)
    await ctx.channel.send('<@'+ sPlayer +'> have '+ str(value) +'★Star')
  else:
    await ctx.channel.send('Not Found')

# @client.command()
# async def s(ctx, player: discord.Member):
#   sPlayer = str(player.id)
#   check = False
#   keys = db.keys()
#   for row in keys:
#     if row == sPlayer:
#       check = True
#       break
#   if check == True:
#     value = db[sPlayer]
#     await ctx.channel.send('<@'+ sPlayer +'> have '+ str(value) +'★point')
#   else:
#     await ctx.channel.send('Not Found')
    
@client.command()
async def s(ctx, player: discord.Member):
  sPlayer = str(player.id)
  np = 'n' + str(player.id)
  nPlayer = str(player.name)
  check = False
  keys = db.keys()
  for row in keys:
    if row == sPlayer:
      check = True
      break
  if check == True:
    value = db[sPlayer]
    db[np] = nPlayer
    await ctx.channel.send(nPlayer +' have '+ str(value) +'★Star')
  else:
    await ctx.channel.send('Not Found')

@client.command()
async def board(ctx):
   cal_board()
   print(listC)
   embed = discord.Embed(title=f"{'----------<Leader Board>----------'}", description=('แสดง Top25'),color=discord.Color.red())
   num = 0
   while num < len(listC):
     value = db[listC[num]]
     nameDis = str(listC[num])
     embed.add_field(name='★Star' + str(value), value=f"{'<@'+nameDis+'>'}")
     num += 1
   await ctx.send(embed=embed)

@client.command()
async def b(ctx):
  await ctx.channel.send('ขอเวลาบอทคิดแปปนึง')
  cal_board()
  #print(listC)
  output = " ----------<Leader Board>---------- \n"
  output = output + " ถ้าชื่อใครไม่ขึ้นให้ใช้คำสั่ง +show ก่อนแล้วมาลองใหม่ \n"
  num = 0
  while num < len(listC):
    value = db[listC[num]]
    nameDis = str(listC[num])
    np = 'n' + nameDis
    #print(np)
    keys = db.keys()
    #print(keys)
    check = False
    for row in keys:
      if row == np:
        check = True
        break
    if check == True:
      nameDis = db[np]
      output = output + ''+ str(value) + '★Star ของ ' +nameDis + ' \n'
    else:
      output = output + ''+str(value) + '★Star ของ ' + '<@'+nameDis+'> \n'
    num += 1
    if num%25 == 0:
      await ctx.send('```' + output + '```' )
      output = " ----------<Leader Board>---------- \n"
      output = output + " ถ้าชื่อใครไม่ขึ้นให้ใช้คำสั่ง +show ก่อนแล้วมาลองใหม่ \n"
    elif num == len(listC):
      await ctx.send('```' + output + '```' )
      output = " ----------<Leader Board>---------- \n"
      output = output + " ถ้าชื่อใครไม่ขึ้นให้ใช้คำสั่ง +show ก่อนแล้วมาลองใหม่ \n"
  
@client.command()
async def restart(ctx): 
  await ctx.channel.send('Test Restart')
  print("\n\nRESTARTING NOW\n\n\n")
  await ctx.channel.send('kill process')
  print('kill')
  system('kill 1')
  await ctx.channel.send('sleep')
  print('sleep')
  sleep(7)
  await ctx.channel.send('restart')
  print('restart')
  system("python main.py")

keep_alive()
try:
    client.run(my_secret)
except discord.errors.HTTPException:
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  system("python restarter.py")
  
  
  