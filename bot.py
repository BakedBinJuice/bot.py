#!/usr/bin/env python3

import os
import os.path
from os import path
import discord
import random
from discord.ext import commands
import cryptocompare
import discord.utils
from discord.utils import get



#to handle .env files.

#bot token.
TOKEN = 'TOKEN'
#server name in .env file.

bot = commands.Bot(command_prefix="!")

server_owner = "Bingel"
PARTICIPANT_ROLE = "PARTICIPANT"
RISING_ROLE = "RISING"
GAMBLER_ROLE = "GAMBLER"
BALLER_ROLE = "BALLER"
CRYPTO_ROLE = "CRYPTO-GUY"
KINGPIN_ROLE = "KINGPIN"
GOD_ROLE = "GOD"


#on_ready handles what the bot does after establishing a connection to Discord.
@bot.event
async def on_ready():
	for guild in bot.guilds:
		if guild.name == True:
			break
			
	#iterate over and print out members of a server.
	members = '\n - '.join([member.name for member in guild.members])
	print(f'Guild Members:\n - {members}')
	#make files for users.
	starting_value = "100"
	for guild in bot.guilds:
		for member in guild.members:
			while True:
				if os.path.isfile(member.name + ".txt"):
					member_wallet = open(member.name + ".txt")
					member_balance = member_wallet.read()
					await member.create_dm()
					await member.dm_channel.send(f'Hello {member.name}, I am Crypto-bot (UPDATED). I belong to {guild.name}.\n you currently have ' + str(member_balance) + ' Crypto Coins.')
					break
				else:
					file = open(member.name + ".txt", "w")
					file.write(starting_value)
					file.close()
					await member.create_dm()
					await member.dm_channel.send(f'Hello {member.name}, I am Crypto-bot (UPDATED). I belong to {guild.name}.\n{guild.name} now has a currency, Crypto-Coins.\nWith this currency you can send coins to other members within the server, play gambling games to win or lose your coins and buy rewards if you have enough coins in your wallet.\nTo start you of 100 Crypto-Coins have been added to your personal wallet, go to the {guild.name} and type "!help" to see commands and different games you can play.\nEnjoy - Crypto-bot.')
	
	
#Handles the event of a new member joining.
@bot.event
async def on_member_join(member):
	starting_value = "100"
	file = open(member.name + ".txt", "w")
	file.write(starting_value)
	file.close()
	await member.create_dm()
	#send DM on that channel.
	await member.dm_channel.send(
		f'Hello {member.name}, welcome to {guild.name} I am Crypto-bot. I belong to {guild.name}.\n{guild.name} now has a currency, Crypto-Coins.\nWith this currency you can send coins to other members within the server, play gambling games to win or lose your coins and buy rewards if you have enough coins in your wallet.\nTo start you of 100 Crypto-Coins have been added to your personal wallet, go to the {guild.name} and type "!help" to see commands and different games you can play.\nEnjoy - Crypto-bot.'
	)


#create a text channel with command.
@bot.command(name='create-text-channel', help='type "!create-text-channel name"')
@commands.has_role('admin')
async def create_channel(ctx, channel_name: str):
	guild = ctx.guild
	existing_channel = discord.utils.get(guild.channels, name=channel_name)
	if not existing_channel:
		await ctx.send(f'Creating a new channel: {channel_name}')
		await guild.create_text_channel(channel_name)
	
	
#if user trys to create channel and isnt admin, print this error.	
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.CheckFailure):
		await ctx.send('You do not have the correct role for this command.')
	
#count and print out number of users in a server.	
@bot.command(name='members', help='type "!members" to see amount of members.')
async def check_member_count(ctx):
	guild = ctx.guild
	member_count = 0
	for member in guild.members:
		member_count = member_count + 1
		
	await ctx.send(str(member_count) + ' members.')
	
	
#get price of Bitcoin.
@bot.command(name='bitcoin', help='type "!bitcoin" to see price of Bitcoin.')
async def check_btc_price(ctx):
	guild = ctx.guild
	await ctx.send(str(cryptocompare.get_price('BTC', 'AUD')))
	
	
#get price of Ethereum.
@bot.command(name='ethereum', help='type "!ethereum" to see price of Etherium.')
async def check_eth_price(ctx):
	guild = ctx.guild
	await ctx.send(str(cryptocompare.get_price('ETH', 'AUD')))
	
	
#get price of Monero.
@bot.command(name='monero', help='type "!monero" to see price or Monero.')
async def check_xmr_price(ctx):
	guild = ctx.guild
	await ctx.send(str(cryptocompare.get_price('XMR', 'AUD')))


#get price of crypto's.
@bot.command(name='cryptos', help='type "!cryptos" to see price of cryptos.')
async def check_cryptos_price(ctx):
	guild = ctx.guild
	await ctx.send(str(cryptocompare.get_price(['BTC', 'ETH', 'XMR'], ['AUD', 'AUD', 'AUD'])))


#show users wallet.
@bot.command(name='wallet', help='type "!wallet" to see your balance.')
async def get_balance(ctx):
	user = (str(ctx.message.author.name))
	f = open(user + ".txt", "r")
	balance = f.read()
	await ctx.send(user + ": Crypto-Coins= " + str(balance))
	
	
#send money to other users.
@bot.command(name='send', help='type "!send name value" to transfer funds.')
async def send_funds(ctx, reciever, value):
	guild = ctx.guild
	sender = (str(ctx.message.author.name))
	rwallet = open(sender + ".txt", "r")
	wallet = rwallet.read()
		
	if os.path.isfile(reciever + ".txt"):
		if int(value) < 0:
			await ctx.send("that is not a valid payment.")
		
		elif int(wallet) < int(value):
			await ctx.send("You only have " + wallet + " Crypto-Coins available.\nInsufficient funds!!!")
			
		else:
			rf = open(sender + ".txt", "r")
			og_val = rf.read()
			f = open(sender + ".txt", "w")
			extract = int(og_val) - int(value)
			f.write(str(extract))
			f.close()
			rf.close()
			rec_rfile = open(reciever + ".txt", "r")
			new_val = rec_rfile.read()
			rec_file = open(reciever + ".txt", "w")
			new_bal = int(new_val) + int(value)
			send = rec_file.write(str(new_bal))
			rec_file.close()
			rec_rfile.close()
			await ctx.send("transferred " + value + " Crypto-Coins to " + reciever + " from " + sender + ".")
		
	else:
		await ctx.send(str(reciever) + " is not a member.")
		
		
#coin flip gamble game.
@bot.command(name='flip', help='type "!flip heads 30" to flip a coin and win or lose money') 
async def coin_flip(ctx, choice, bet):
	sender = (str(ctx.message.author.name))
	rwallet = open(sender + ".txt", "r")
	wallet = rwallet.read()
	heads_or_tails = ['heads', 'tails']
	response = random.choice(heads_or_tails)
	
	if int(wallet) < int(bet):
		await ctx.send("insufficient funds!")
		
	elif int(bet) < 0:
		await ctx.send("invalid bet!")
	
	#give user their reward.
	elif str(choice) == str(response):
		reward = int(bet)
		new_bal = int(wallet) + int(reward)
		wf = open(sender + ".txt", "w")
		send_reward = wf.write(str(new_bal))
		wf.close()
		await ctx.send(str(response) + ". You won " + str(bet) + ". Your new balance is " + str(new_bal) + ".")
		
	#take users loses as tax.
	elif str(choice) != str(response):
		rf = open(sender + ".txt", "r")
		og_val = rf.read()
		f = open(sender + ".txt", "w")
		extract = int(og_val) - int(bet)
		f.write(str(extract))
		rf.close()
		f.close()
		rec_rfile = open(server_owner + ".txt", "r")
		new_val = rec_rfile.read()
		rec_file = open(server_owner + ".txt", "w")
		new_bal = int(new_val) + int(bet)
		send = rec_file.write(str(new_bal))
		rec_file.close()
		rec_rfile.close()
		await ctx.send(str(response) + ". You lose " + str(bet) + ". Your new balance is " + str(extract) + ".")
		

#blackjack game.
@bot.command(name='blackjack', help='type "!blackjack bet" to start your round.')
async def blackjack(ctx, bet):
	sender = (str(ctx.message.author.name))
	author = ctx.message.author
	rwallet = open(sender + ".txt", "r")
	wallet = rwallet.read()
	global dealer_cards
	dealer_cards = []
	global player_cards
	player_cards = []
	if int(bet) > int(wallet):
		await ctx.send("INSUFFICIENT FUNDS!!!")
	# Deal the cards
	# Display the cards
	# Dealer Cards
	# Player Cards
	else:
		while len(dealer_cards) != 2:
			dealer_cards.append(random.randint(1, 11))
			player_cards.append(random.randint(1, 11))
			if len(dealer_cards) == 2:
				if len(player_cards) == 2:
					await ctx.send("Dealer has ? & " +  str(dealer_cards[1]) + " You have " + str(player_cards))
					
					# Sum of the Dealer cards
					if sum(dealer_cards) == 21:
						f = open(sender + ".txt", "w")
						extract = int(wallet) - int(bet)
						f.write(str(extract))
						f.close()
						rec_rfile = open(server_owner + ".txt", "r")
						new_val = rec_rfile.read()
						rec_file = open(server_owner + ".txt", "w")
						new_bal = int(new_val) + int(bet)
						send = rec_file.write(str(new_bal))
						rec_rfile.close()
						rec_file.close()
						await ctx.send("You lose, Dealer has 21.\nYou lose " + str(bet) + ". Your new balance is " + str(new_bal) + ".")
								
					elif sum(dealer_cards) > 21:
						reward = int(bet)
						new_bal = int(wallet) + int(reward)
						wf = open(sender + ".txt", "w")
						send_reward = wf.write(str(new_bal))
						wf.close()
						await ctx.send("Dealer has busted!!!\nYou won " + str(bet) + ". Your new balance is " + str(new_bal) + ".")
								
			    		# Sum of the Player cards
					while sum(player_cards) < 21:
						if sum(dealer_cards) == sum(player_cards):
							if sum(dealer_cards) < 11:
								dealer_cards.append(random.randint(1, 11))						
								await ctx.send(str("Do you want to stay or hit? "))
								response = await bot.wait_for('message', check = lambda message: message.author == ctx.author, timeout = 20)
										
								if response.content.lower() == "hit":
									player_cards.append(random.randint(1, 11))
									await ctx.send("You now have a total of " + str(sum(player_cards)) + " from these cards " + str(player_cards))
											
								elif response.content.lower() == "stay":
									await ctx.send("The dealer has a total of " + str(sum(dealer_cards)) + " with " + str(dealer_cards))
									await ctx.send("You have a total of " + str(sum(player_cards)) + " with " + str(player_cards))
											
									if sum(dealer_cards) > sum(player_cards):
										f = open(sender + ".txt", "w")
										extract = int(wallet) - int(bet)
										f.write(str(extract))
										f.close()
										rec_rfile = open(server_owner + ".txt", "r")
										new_val = rec_rfile.read()
										rec_file = open(server_owner + ".txt", "w")
										new_bal = int(new_val) + int(bet)
										send = rec_file.write(str(new_bal))
										rec_rfile.close()
										rec_file.close()
										await ctx.send("Dealer wins! " + str(bet) + ".\nYour new balance is " + str(new_bal) + ".")
										break
											    	
									elif sum(dealer_cards) < sum (player_cards):
										reward = int(bet)
										new_bal = int(wallet) + int(reward)
										wf = open(sender + ".txt", "w")
										send_reward = wf.write(str(new_bal))
										wf.close()
										await ctx.send("You won " + str(bet) + ".\nYour new balance is " + str(new_bal) + ".")
										break
										
							else:
								await ctx.send(str("Do you want to stay or hit? "))
								response = await bot.wait_for('message', check = lambda message: message.author == ctx.author, timeout = 20)
										
								if response.content.lower() == "hit":
									player_cards.append(random.randint(1, 11))
									await ctx.send("You now have a total of " + str(sum(player_cards)) + " from these cards " + str(player_cards))
											
								elif response.content.lower() == "stay":
									await ctx.send("The dealer has a total of " + str(sum(dealer_cards)) + " with " + str(dealer_cards))
									await ctx.send("You have a total of " + str(sum(player_cards)) + " with " + str(player_cards))
											
									if sum(dealer_cards) > sum(player_cards):
										f = open(sender + ".txt", "w")
										extract = int(wallet) - int(bet)
										f.write(str(extract))
										f.close()
										rec_rfile = open(server_owner + ".txt", "r")
										new_val = rec_rfile.read()
										rec_file = open(server_owner + ".txt", "w")
										new_bal = int(new_val) + int(bet)
										send = rec_file.write(str(new_bal))
										rec_rfile.close()
										rec_file.close()
										await ctx.send("Dealer wins! " + str(bet) + ".\nYour new balance is " + str(new_bal) + ".")
										break
											    	
									elif sum(dealer_cards) < sum (player_cards):
										reward = int(bet)
										new_bal = int(wallet) + int(reward)
										wf = open(sender + ".txt", "w")
										send_reward = wf.write(str(new_bal))
										wf.close()
										await ctx.send("You won " + str(bet) + ".\nYour new balance is " + str(new_bal) + ".")
										break
												
						elif sum(dealer_cards) != sum(player_cards):	
							if sum(dealer_cards) < 11:
								dealer_cards.append(random.randint(1, 11))
								await ctx.send(str("Do you want to stay or hit? "))
								response = await bot.wait_for('message', check = lambda message: message.author == ctx.author, timeout = 20)
											
								if response.content.lower() == "hit":
									player_cards.append(random.randint(1, 11))
									await ctx.send("You now have a total of " + str(sum(player_cards)) + " from these cards " + str(player_cards))
												
								elif response.content.lower() == "stay":
									await ctx.send("The dealer has a total of " + str(sum(dealer_cards)) + " with " + str(dealer_cards))
									await ctx.send("You have a total of " + str(sum(player_cards)) + " with " + str(player_cards))
												
									if sum(dealer_cards) > sum(player_cards):
										f = open(sender + ".txt", "w")
										extract = int(wallet) - int(bet)
										f.write(str(extract))
										f.close()
										rec_rfile = open(server_owner + ".txt", "r")
										new_val = rec_rfile.read()
										rec_file = open(server_owner + ".txt", "w")
										new_bal = int(new_val) + int(bet)
										send = rec_file.write(str(new_bal))
										rec_rfile.close()
										rec_file.close()
										await ctx.send("Dealer wins! " + str(bet) + ".\nYour new balance is " + str(new_bal) + ".")
										break
												    	
									elif sum(dealer_cards) < sum (player_cards):
										reward = int(bet)
										new_bal = int(wallet) + int(reward)
										wf = open(sender + ".txt", "w")
										send_reward = wf.write(str(new_bal))
										wf.close()
										await ctx.send("You won " + str(bet) + ".\nYour new balance is " + str(new_bal) + ".")
										break
										
							else:
								await ctx.send(str("Do you want to stay or hit? "))
								response = await bot.wait_for('message', check = lambda message: message.author == ctx.author, timeout = 20)
											
								if response.content.lower() == "hit":
									player_cards.append(random.randint(1, 11))
									await ctx.send("You now have a total of " + str(sum(player_cards)) + " from these cards " + str(player_cards))
												
								elif response.content.lower() == "stay":
									await ctx.send("The dealer has a total of " + str(sum(dealer_cards)) + " with " + str(dealer_cards))
									await ctx.send("You have a total of " + str(sum(player_cards)) + " with " + str(player_cards))
												
									if sum(dealer_cards) > sum(player_cards):
										f = open(sender + ".txt", "w")
										extract = int(wallet) - int(bet)
										f.write(str(extract))
										f.close()
										rec_rfile = open(server_owner + ".txt", "r")
										new_val = rec_rfile.read()
										rec_file = open(server_owner + ".txt", "w")
										new_bal = int(new_val) + int(bet)
										send = rec_file.write(str(new_bal))
										rec_rfile.close()
										rec_file.close()
										await ctx.send("Dealer wins! " + str(bet) + ".\nYour new balance is " + str(new_bal) + ".")
										break
												    	
									elif sum(dealer_cards) < sum (player_cards):
										reward = int(bet)
										new_bal = int(wallet) + int(reward)
										wf = open(sender + ".txt", "w")
										send_reward = wf.write(str(new_bal))
										wf.close()
										await ctx.send("You won " + str(bet) + ".\nYour new balance is " + str(new_bal) + ".")
										break
								    	
						if sum(player_cards) > 21:
							f = open(sender + ".txt", "w")
							extract = int(wallet) - int(bet)
							f.write(str(extract))
							f.close()
							rec_rfile = open(server_owner + ".txt", "r")
							new_val = rec_rfile.read()
							rec_file = open(server_owner + ".txt", "w")
							new_bal = int(new_val) + int(bet)
							send = rec_file.write(str(new_bal))
							rec_rfile.close()
							rec_file.close()
							await ctx.send("You BUSTED! Dealer wins. " + str(bet) + ".\nYour new balance is " + str(new_bal) + ".")
							break
								    	
						elif sum(player_cards) == 21:
							reward = int(bet) * 1.5
							new_bal = int(wallet) + int(reward)
							wf = open(sender + ".txt", "w")
							send_reward = wf.write(str(new_bal))
							wf.close()
							await ctx.send("You have BLACKJACK! You Win!! " + str(reward) + ".\nYour new balance is " + str(new_bal) + ".")
							break
							
						elif sum(dealer_cards) == sum(player_cards):
							await ctx.send("Matching outcome no one wins.")
							break
					

@bot.command(name="buy-role-participant", help='type "!buy-role-participant" for 10,000 Crypto-coins.')
async def add_user_role(ctx):
	cost = 10000
	member = ctx.message.author
	role = discord.utils.get(member.guild.roles, name=str(PARTICIPANT_ROLE))
	sender = str(ctx.message.author.name)
	rwallet = open(sender + ".txt", "r")
	wallet = rwallet.read()
	if int(cost) > int(wallet):
		await ctx.send("INSUFFICIENT FUNDS!!!")
	
	elif int(cost) <= int(wallet):		
		f = open(sender + ".txt", "w")
		extract = int(wallet) - int(cost)
		f.write(str(extract))
		f.close()
		rec_rfile = open(server_owner + ".txt", "r")
		new_val = rec_rfile.read()
		rec_file = open(server_owner + ".txt", "w")
		new_bal = int(new_val) + int(cost)
		send = rec_file.write(str(new_bal))
		rec_rfile.close()
		rec_file.close()
		try:
			await member.add_roles(role)
			await ctx.send(f"{member} was given {PARTICIPANT_ROLE}.\n" + str(cost) + " Crypto-Coins have been transferred your new balance is " + str(new_bal))
		except Exception as e:
			await ctx.send('There was an error running this command ' + str(e))

	
@bot.command(name="buy-role-rising", help='type "!buy-role-rising" for 50,000 Crypto-coins.')
async def add_user_role(ctx):
	cost = 50000
	member = ctx.message.author
	role = discord.utils.get(member.guild.roles, name=str(RISING_ROLE))
	sender = str(ctx.message.author.name)
	rwallet = open(sender + ".txt", "r")
	wallet = rwallet.read()
	if int(cost) > int(wallet):
		await ctx.send("INSUFFICIENT FUNDS!!!")
		
	elif int(cost) <= int(wallet):
		f = open(sender + ".txt", "w")
		extract = int(wallet) - int(cost)
		f.write(str(extract))
		f.close()
		rec_rfile = open(server_owner + ".txt", "r")
		new_val = rec_rfile.read()
		rec_file = open(server_owner + ".txt", "w")
		new_bal = int(new_val) + int(cost)
		send = rec_file.write(str(new_bal))
		rec_rfile.close()
		rec_file.close()
		try:
			await member.add_roles(role)
			await ctx.send(f"{member} was given {RISING_ROLE}.\n" + str(cost) + " Crypto-Coins have been transferred your new balance is " + str(new_bal))
		except Exception as e:
			await ctx.send('There was an error running this command ' + str(e))
		
@bot.command(name="buy-role-gambler", help='type "!buy-role-gambler" for 500,000 Crypto-coins.')
async def add_user_role(ctx):
	cost = 500000
	member = ctx.message.author
	role = discord.utils.get(member.guild.roles, name=str(GAMBLER_ROLE))
	sender = str(ctx.message.author.name)
	rwallet = open(sender + ".txt", "r")
	wallet = rwallet.read()
	if int(cost) > int(wallet):
		await ctx.send("INSUFFICIENT FUNDS!!!")
		
	elif int(cost) <= int(wallet):
		f = open(sender + ".txt", "w")
		extract = int(wallet) - int(cost)
		f.write(str(extract))
		f.close()
		rec_rfile = open(server_owner + ".txt", "r")
		new_val = rec_rfile.read()
		rec_file = open(server_owner + ".txt", "w")
		new_bal = int(new_val) + int(cost)
		send = rec_file.write(str(new_bal))
		rec_rfile.close()
		rec_file.close()
		try:
			await member.add_roles(role)
			await ctx.send(f"{member} was given {GAMBLER_ROLE}.\n" + str(cost) + " Crypto-Coins have been transferred your new balance is " + str(new_bal))
		except Exception as e:
			await ctx.send('There was an error running this command ' + str(e))
		
		
@bot.command(name="buy-role-baller", help='type "!buy-role-baller" for 1,000,000 Crypto-coins.')
async def add_user_role(ctx):
	cost = 1000000
	member = ctx.message.author
	role = discord.utils.get(member.guild.roles, name=str(BALLER_ROLE))
	sender = str(ctx.message.author.name)
	rwallet = open(sender + ".txt", "r")
	wallet = rwallet.read()
	if int(cost) > int(wallet):
		await ctx.send("INSUFFICIENT FUNDS!!!")
		
	elif int(cost) <= int(wallet):
		f = open(sender + ".txt", "w")
		extract = int(wallet) - int(cost)
		f.write(str(extract))
		f.close()
		rec_rfile = open(server_owner + ".txt", "r")
		new_val = rec_rfile.read()
		rec_file = open(server_owner + ".txt", "w")
		new_bal = int(new_val) + int(cost)
		send = rec_file.write(str(new_bal))
		rec_rfile.close()
		rec_file.close()
		try:
			await member.add_roles(role)
			await ctx.send(f"{member} was given {BALLER_ROLE}.\n" + str(cost) + " Crypto-Coins have been transferred your new balance is " + str(new_bal))
		except Exception as e:
			await ctx.send('There was an error running this command ' + str(e))
		
		
@bot.command(name="buy-role-crypto-guy", help='type "!buy-role-crypto-guy" for 50,000,000 Crypto-coins.')
async def add_user_role(ctx):
	cost = 50000000
	member = ctx.message.author
	role = discord.utils.get(member.guild.roles, name=str(CRYPTO_ROLE))
	sender = str(ctx.message.author.name)
	rwallet = open(sender + ".txt", "r")
	wallet = rwallet.read()
	if int(cost) > int(wallet):
		await ctx.send("INSUFFICIENT FUNDS!!!")
		
	elif int(cost) <= int(wallet):
		f = open(sender + ".txt", "w")
		extract = int(wallet) - int(cost)
		f.write(str(extract))
		f.close()
		rec_rfile = open(server_owner + ".txt", "r")
		new_val = rec_rfile.read()
		rec_file = open(server_owner + ".txt", "w")
		new_bal = int(new_val) + int(cost)
		send = rec_file.write(str(new_bal))
		rec_rfile.close()
		rec_file.close()
		try:
			await member.add_roles(role)
			await ctx.send(f"{member} was given {CRYPTO_ROLE}.\n" + str(cost) + " Crypto-Coins have been transferred your new balance is " + str(new_bal))
		except Exception as e:
			await ctx.send('There was an error running this command ' + str(e))
		
		
@bot.command(name="buy-role-kingpin", help='type "!buy-role-kingpin" for 500,000,000 Crypto-coins.')
async def add_user_role(ctx):
	cost = 500000000
	member = ctx.message.author
	role = discord.utils.get(member.guild.roles, name=str(KINGPIN_ROLE))
	sender = str(ctx.message.author.name)
	rwallet = open(sender + ".txt", "r")
	wallet = rwallet.read()
	if int(cost) > int(wallet):
		await ctx.send("INSUFFICIENT FUNDS!!!")
		
	elif int(cost) <= int(wallet):
		f = open(sender + ".txt", "w")
		extract = int(wallet) - int(cost)
		f.write(str(extract))
		f.close()
		rec_rfile = open(server_owner + ".txt", "r")
		new_val = rec_rfile.read()
		rec_file = open(server_owner + ".txt", "w")
		new_bal = int(new_val) + int(cost)
		send = rec_file.write(str(new_bal))
		rec_rfile.close()
		rec_file.close()
		try:
			await member.add_roles(role)
			await ctx.send(f"{member} was given {KINGPIN_ROLE}.\n" + str(cost) + " Crypto-Coins have been transferred your new balance is " + str(new_bal))
		except Exception as e:
			await ctx.send('There was an error running this command ' + str(e))
		
		
@bot.command(name="buy-role-god", help='type "!buy-role-god" for 1,000,000,000 Crypto-coins.')
async def add_user_role(ctx):
	cost = 1000000000000
	member = ctx.message.author
	role = discord.utils.get(member.guild.roles, name=str(GOD_ROLE))
	sender = str(ctx.message.author.name)
	rwallet = open(sender + ".txt", "r")
	wallet = rwallet.read()
	if int(cost) > int(wallet):
		await ctx.send("INSUFFICIENT FUNDS!!!")
		
	elif int(cost) <= int(wallet):
		f = open(sender + ".txt", "w")
		extract = int(wallet) - int(cost)
		f.write(str(extract))
		f.close()
		rec_rfile = open(server_owner + ".txt", "r")
		new_val = rec_rfile.read()
		rec_file = open(server_owner + ".txt", "w")
		new_bal = int(new_val) + int(cost)
		send = rec_file.write(str(new_bal))
		rec_rfile.close()
		rec_file.close()
		try:
			await member.add_roles(role)
			await ctx.send(f"{member} was given {GOD_ROLE}.\n" + str(cost) + " Crypto-Coins have been transferred your new balance is " + str(new_bal))
		except Exception as e:
			await ctx.send('There was an error running this command ' + str(e))
			
			
@bot.command(name="store", help='type= "!store" to see the store.')
async def store(ctx):
	sender = str(ctx.message.author.name)
	rwallet = open(sender + ".txt", "r")
	wallet = rwallet.read()
	await ctx.send('''\t\t\tCrypto-Coin wallet --> ''' + str(wallet) + '\n'''' 
PARTICIPANT: buy for 10,000 Crypto-Coins "!buy-role-participant".
RISING: buy for 50,000 Crypto-Coins with "!buy-role-rising".
GAMBLER: buy for 500,000 Crypto-Coins with "!buy-role-gambler".
BALLER: buy for 1,000,000 Crypto-Coins with "!buy-role-baller".
CRYPTO-GUY: buy for 50,000,000 Crypto-Coins with "!buy-role-crypto-guy".
KINGPIN: buy for 500,000,000 Crypto-Coins with "!buy-role-kingpin".
GOD: buy for 1,000,000,000 Crypto-Coins with "!buy-role-god".''')


bot.run(str(TOKEN))




