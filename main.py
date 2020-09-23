import discord
from discord.ext import commands, tasks
import asyncio
import random


bot = commands.Bot(command_prefix = "_", description = "Un bot de test.")

randomSentances = ["J'aime les patates", 
					"J'aime les pâtes au pesto", 
					"J'aime les carrotes rapées", 
					"J'aime les boulons", 
					"J'aime les vis", "J'aime la raclette", 
					"J'aime pas le camembert", 
					"Tout le monde aime les patates", 
					"Tu viens de perdre deux secondes de ta vie en lisant ça"]

@bot.event
async def on_ready():
	print("Bonjour")
	changeStatus.start()

@bot.command()
async def test(ctx):
	await ctx.send("Si tu reçois ce message, alors le test a réussi")

@bot.command()
async def patate(ctx):
	await ctx.send("Tu aimes les patates ? Moi aussi.")

@bot.command()
async def rank(ctx):
	await ctx.send("T'as pas de rang et tu sais pourquoi ? Parce que ||tes pa bo/bêle||")

@bot.command()
async def serverinfo(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	numberOfPerson = server.member_count
	serverName = server.name
	message = f"Ce serveur s'appelle __**{serverName}**__, et il compte actuellement **{numberOfPerson} membres**. \n\nIl contient **{numberOfTextChannels} channels textuels** et **{numberOfVoiceChannels} channels vocaux**. "
	await ctx.send(message)

@bot.command()
async def say(ctx, *texte):		
	messages = await ctx.channel.history(limit = 1).flatten()
	for message in messages:
		await message.delete()
	await ctx.send(" ".join(texte))



@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
	messages = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in messages:
		await message.delete()
	
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *, reason = "Aucune raison n'a été donnée"):

	await ctx.guild.kick(user, reason = reason)
		
	embed = discord.Embed(title = "**Expulsation**", description ="(Comment ça ça s'écrit pas comme ça ?)", color = 0xff0000)
	embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url, url = "https://www.youtube.com/channel/UCGfRsT-itPWyntKBvgk7JeA")
	embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/643509670224330772/757228532006125588/unknown.png")
	embed.add_field(name = "Victime du kick", value = user.name, inline = True)
	embed.add_field(name = "Raison", value = reason, inline = True)
	embed.add_field(name = "Modérateur coupable de cet abus de pouvoir", value = ctx.author.name, inline = False)
	embed.set_footer(text = random.choice(randomSentances))
			
	await ctx.send(embed = embed)
	

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *, reason = "Aucune raison n'a été donnée"):
	await ctx.guild.ban(user, reason = reason)
	
	embed = discord.Embed(title = "**Bannissement**", description ="J'aime les patates, pas toi ?", color = 0xff0000)
	embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url, url = "https://www.youtube.com/channel/UCGfRsT-itPWyntKBvgk7JeA")
	embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/643509670224330772/757228532006125588/unknown.png")
	embed.add_field(name = "Victime du banhammer", value = user.name, inline = True)
	embed.add_field(name = "Raison", value = reason, inline = True)
	embed.add_field(name = "Modérateur coupable de cet abus de pouvoir", value = ctx.author.name, inline = False)
	embed.set_footer(text = random.choice(randomSentances))
			
	await ctx.send(embed = embed)
	
async def createMutedRole(ctx):
	mutedRole = await ctx.guild.create_role(name = "Muted", permissions = discord.Permissions(
																send_messages = False,
																speak = False),
															reason = "Création du rôle qui permettra de mute des gens")
	for channel in ctx.guild.channels:
		await channel.set_permissions(mutedRole, send_messages = False, speak = False)
	return mutedRole

async def getMutedRole(ctx):
	roles = ctx.guild.roles
	for role in roles:
		if role.name == "Muted":
			return role
	
	return await createMutedRole(ctx)

@bot.command()
@commands.has_permissions(administrator = True)
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été donnée"):
	mutedRole = await getMutedRole(ctx)
	await member.add_roles(mutedRole, reason = reason)
	await ctx.send(f"{member.mention} ne peut plus parler. Il a perdu sa langue car \"qui joue avec le feu finit par se bruler la langue\". La raison invoquée est : {reason}.")	

@bot.command()
@commands.has_permissions(administrator = True)
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été donnée"):
	mutedRole = await getMutedRole(ctx)
	await member.remove_roles(mutedRole, reason = reason)
	await ctx.send(f"{member.mention} peut à nouveau parler pour la raison : {reason}.")

def isOwner(ctx):
	return ctx.message.author.id == 576062852646043648 

@bot.command()
@commands.check(isOwner)
async def private(ctx):
	await ctx.send("Cette commande n'est utilisable uniquement par le dresseur du bot")

@bot.command()
async def startgame(ctx):
	await ctx.send("A quel jeu voulez vous jouer ? (La commande sera annulée au bout de 10 secondes d'attente).")

	def check(message):
		return message.author == ctx.message.author and ctx.message.channel == message.channel
	
	try:
		game = await bot.wait_for("message", timeout = 10, check = check)
	except:
		await ctx.send("Les 10 secondes sont écoulées. La commande a été annulée.")

	
	message = await ctx.send(f"Le jeu **{game.content}** va commencer. Validez en réagissant avec :white_check_mark: ou annulez en réagissant avec :x:. La commande sera annulée au bout de 10 secondes d'attente).")
	await message.add_reaction("✅")
	await message.add_reaction("❌")

	def checkEmoji(reaction, user):
		return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

	try:
		reaction, user = await bot.wait_for("reaction_add", timeout = 10, check = checkEmoji)
		if reaction.emoji == "✅":
			await ctx.send("Le jeu a démarré.")
		else:
			await ctx.send("Jeu annulé.") 
	except:
		await ctx.send("10 secondes écoulées. La commande a été annulée.")

@bot.command()
async def roulette(ctx):
	await ctx.send("La roulette commencera dans 10 secondes. Envoyez \"**moi**\" dans ce channel pour y participer.")
	
	players = []
	def check(message):
		return message.channel == ctx.message.channel and message.author not in players and message.content == "moi"

	try:
		while True:
			participation = await bot.wait_for('message', timeout = 10, check = check)
			players.append(participation.author)
			print("Nouveau participant : ")
			print(participation)
			await ctx.send(f"**{participation.author.name}** participe au tirage ! Le tirage commence dans 10 secondes.")
	except: #Timeout
		print("Démarrage du tirage...")

	gagner = ["une patate", "une banane", "des pâtes au pesto", "du camembert", "de l'eau minérale mont blanc"]

	await ctx.send("Le tirage va commencer dans 3...")
	await asyncio.sleep(1)
	await ctx.send("2")
	await asyncio.sleep(1)
	await ctx.send("1")
	await asyncio.sleep(1)
	loser = random.choice(players)
	price = random.choice(gagner)
	await ctx.send(f"La personne qui a gagné {price} est...")
	await asyncio.sleep(1)
	await ctx.send("**" + loser.name + "**" + " !")


@bot.event
async def on_member_join(member):
	channel = member.guild.get_channel(701040629324447764)
	await channel.send(f"Bonjour et bienvenue à {member.mention} qui a rejoint le serveur !")

@bot.event
async def on_member_remove(member):
	channel = member.guild.get_channel(701040629324447764)
	await channel.send(f"Ce connard de {member.mention} a quitté le serveur !")	

status = ["_help (commande toujours pas programmée lol)",
		"ta gueule", "J'aime les patates, pas toi ?", 
		"I like trains...", "Spotify Premium c'est la vie",
		"Mad City c'était mieux avant",
		"Ace Attorney les meilleurs jeux du monde",
		"Fortbite c'est d'la merde", "J'aime les pâtes au pesto",
		"J'aime pas le poulet", "Donnez moi quelques vis et boulons svp"
		"Celui qui m'dérange j'le bute",
		"Lol impossible de me déranger je suis en NPD",
		"Il va y avoir du rififi dans mon statut",
		"De la chair à piston"]


@tasks.loop(seconds = 30)
async def changeStatus():
	game = discord.Game(random.choice(status))
	await bot.change_presence(status = discord.Status.dnd, activity = game)

niceSentances = ["Bande de sacs à merde", "Je vous suce tous",
				"Vous m'aimez pas ? Bah moi je vous hais",
				"Je vous dis pas bonjour car je vous aime pas",
				"Vous êtes tous les plus gros connards de l'univers",
				"Les robots sont 1000 fois plus intelligents que vous",
				"Il va y avoir du rififi dans votre bite",
				"Vos gueules ressemblent à des gueules",
				"ta gueule"]

@tasks.loop(hours = 1)
async def compter():
	channel = bot.get_channel(699907052453232692)
	await channel.send(random.choices(niceSentances))


@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("T'as oublié d'entrer un argument dans ta commande petit malin")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("Tu crois que j'vais t'obéir si t'as pas les permissions de faire cette commande connard ?")
	elif isinstance(error, commands.CheckFailure):
		await ctx.send("TU PEUX PAS UTILISER CETTE COMMANDE T'AS COMPRIS ?")
		
bot.run("token")
