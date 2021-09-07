import os
import discord
import keep_alive

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# keep_alive.keep_alive()

TOKEN = 'ODgzMzgyODc2OTQ1NjUzODUx.YTJIag.p2mk9WNxIXLh5fdiQDpW2boaaxI'

create = ["!new trial"]
addRoles = ["!trial roles"]
addInfo = ["!trial info"]
help = ["!trial help"]

event = {"name": "",
          "info": "",
          "numbTanks": "",
          "tanks": "",
          "numbHealers": "",
          "healers": "",
          "numbDDs": "",
          "DDs": ""}

show = 0
botMessage = ""
trialCreated = False

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_reaction_add(reaction, user):
  channel = client.get_channel(884019211746283530)
  if reaction.message.author.name == "ESOraiding":
    if user.name == "ESOraiding":
      pass
    else:
      if (reaction.emoji == "🛡️"): 
        event["tanks"] += user.name + " "
        await channel.send(f'{user.mention} is now participating in the '+event["name"]+'trial as tank!')
      if (reaction.emoji == "❤️"): 
        event["healers"] += user.name + " "
        await channel.send(f'{user.mention} is now participating in the '+event["name"]+'trial as healer!')
      if (reaction.emoji == "⚔️"): 
        event["DDs"] += user.name + " "
        await channel.send(f'{user.mention} is now participating in the '+event["name"]+'trial as damage dealer!')


@client.event
async def on_raw_reaction_remove(payload):
  channel = client.get_channel(884019211746283530)
  member = str(await client.fetch_user(payload.user_id))
  emoji = payload.emoji.name

  if emoji == "🛡️":
    tanks = event["tanks"].split(' ')
    user = member.split("#")[0]
    for x in tanks:
      if x == user:
        tanks.remove(x)
        tanks = ''.join(tanks)
        event["tanks"] = tanks
    await channel.send(f'<@{payload.user_id}> is quiting '+event["name"]+'trial!')
  if emoji == "❤️":
    healers = event["healers"].split(' ')
    user = member.split("#")[0]
    for y in healers:
      if y == user:
        healers.remove(y)
        healers = ''.join(healers)
        event["healers"] = healers
    await channel.send(f'<@{payload.user_id}> is quiting '+event["name"]+'trial!')
  if emoji == "⚔️":
    DDs = event["DDs"].split(' ')
    user = member.split("#")[0]
    for z in DDs:
      if z == user:
        DDs.remove(z)
        DDs = ''.join(DDs)
        event["DDs"] = DDs
    await channel.send(f'<@{payload.user_id}> is quiting '+event["name"]+'trial!')


@client.event
async def on_message(message):
  global event, show, trialCreated

  channel = client.get_channel(781421884209627166)
  helpChannel = client.get_channel(884017785435471872)
  usermessage = str(message.content)
  if message.author.name == "ESOraiding":
    pass
  else:
    # Trial help
    if "!trial help" in usermessage:
      await helpChannel.send(">>> ```Bot commands: \n\n▶Creating a new trial: \n!new trial <trial name> \n\n▶After creating a new trial, you have to specify the number of roles: \n!trial roles <Tank count> <Healer> <DD count>\n\n▶You can also add info about the trial: \n!trial info <info> \n\n▶When you have filled in at least the name and number of roles the event will finally be created and people will be bale to join by reacting \n\n▶After creating the trial, you can check it: \n!trial show```")


    # Creating trial
    if "!new trial" in usermessage:
      trialCreated = True
      #Reset the variables
      event["name"] = ""
      event["info"] = ""
      event["numbTanks"] = ""
      event["tanks"] = ""
      event["numbHealers"] = ""
      event["healers"] = ""
      event["numbDDs"] = ""
      event["DDs"] = ""
      show = 0

      splitmessage = usermessage.split(' ')
      if len(splitmessage) > 2: 
        for y in splitmessage:
          if y == "!new" or y == "trial":
            pass
          else:
            event["name"] += y + " "
        await message.add_reaction("👍")
      else:
        await channel.send("Please enter the name/info of the trial!")


    # Adding info to the trial
    if "!trial info" in usermessage:
      if trialCreated == True:
        splitmessage = usermessage.split(' ')
        if len(splitmessage) > 2:
          for y in splitmessage:
            if y == "!trial" or y == "info":
              pass
            else:
              event["info"] += y + " "
          await message.add_reaction("👍")
        else:
          await channel.send("Enter the info of the trial!")
      else:
        await channel.send("Please create a trial!")

    # Adding roles to the trial
    if "!trial roles" in usermessage:
      if trialCreated == True:
        splitmessage = usermessage.split(' ')
        if len(splitmessage) > 2:
          if len(splitmessage) == 5:
            try:
              if type(int(splitmessage[2])) == int:
                event["numbTanks"] = splitmessage[2]

              if type(int(splitmessage[3])) == int:
                event["numbHealers"] = splitmessage[3]

              if type(int(splitmessage[4])) == int:
                event["numbDDs"] = splitmessage[4]

              await message.add_reaction("👍")
            except:
              await channel.send("Please enter numbers for the roles!")
          elif len(splitmessage) > 5:
            await channel.send("Too many roles!")
          else:
            await channel.send("Please enter all the roles")
        else:
          await channel.send("Please enter the roles")
      else:
        await channel.send("Please create a trial!")


    # Showing the trial after finishing it
    if event["name"] != "" and event["numbTanks"] != "" and event["numbHealers"] != "" and event["numbDDs"] != "" and show != 1:
      show = 1
      if event["info"] != "":
        trialInfo = ">>> ```Trial created: "+event["name"]+"\n\n"+event["info"]+"\n\nPlease react with the right emoji to be able to participate in the trial! \n\n 🛡️ Tank (Needed: "+event["numbTanks"]+") \n\n ❤️ Healer (Needed: "+event["numbHealers"]+") \n\n ⚔️ Damage Dealer (Needed: "+event["numbDDs"]+")```"
      else:
        trialInfo = ">>> ```Trial created: "+event["name"]+"\n\nPlease react with the right emoji to be able to participate in the trial! \n\n 🛡️ Tank (Needed: "+event["numbTanks"]+") \n\n ❤️ Healer (Needed: "+event["numbHealers"]+") \n\n ⚔️ Damage Dealer (Needed: "+event["numbDDs"]+")```"
      botMessage = await channel.send(trialInfo)
      await botMessage.add_reaction("🛡️")
      await botMessage.add_reaction("❤️")
      await botMessage.add_reaction("⚔️")
      
    
    # Check trial
    if ("!trial show") == usermessage:
      if show == 1:
        if event["info"] != "":
          await channel.send(">>> ```Trial: "+event["name"]+"\n\n"+event["info"]+" \n\n 🛡️ Tanks - "+event["tanks"]+"\n\n ❤️ Healers - "+event["healers"]+"\n\n ⚔️ DDs - "+event["DDs"]+"```")
        else:
          await channel.send(">>> ```Trial: "+event["name"]+" \n\n 🛡️ Tanks - "+event["tanks"]+"\n\n ❤️ Healers - "+event["healers"]+"\n\n ⚔️ DDs - "+event["DDs"]+"```")
      else:
        await channel.send("Please create a new trial or fill in the required info!")


@client.event
async def on_guild_join(guild):
    joinchannel = guild.system_channel
    await joinchannel.send('*Ahoy to all the fishermen and hello to everyone else, I was invited here today to try to make your lifes easier during trials!\n So till your next trial!* \n\n I\'m a Custom Discord Bot, created by TimeSauce')
    
client.run(TOKEN)