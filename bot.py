# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 14:34:11 2019

@author: tete5
"""

#import aiocron
from discord.ext.commands import Bot
import joueur as pl

class BotLG(Bot):
    def __init__(self,groupe=pl.Groupe(),*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.groupe=groupe
        self.vote_village=False
        self.vote_loup=True

bot=BotLG(command_prefix='!',command_not_found='Je ne connais pas la commande {} ...')

@bot.command(pass_context=True)
async def vote(context):
    message=context.message
    if message.channel.is_private==False:
        await bot.delete_message(message)
        await bot.say('On vote en MP ! 😠')
    elif not (bot.vote_village or (bot.vote_loup and bot.groupe.avoir_par_ID(message.author.id).role.clan==pl.Clan.loup)):
        await bot.say("Pourquoi voter ? Ce n'est pas le moment")
    else:
        vote=message.content[6:]
        joueur=bot.groupe.avoir_par_nom(vote)
        if joueur==-1:
            await bot.say("Joueur inconnu")
        elif joueur.etat==pl.Etat.mort:
            await bot.say("Joueur mort")
        else:
            await bot.say('Tu as voté pour {}'.format(vote))

@bot.command()
async def etat():
    message=''
    for joueur in bot.groupe:
        message+='Nom : {}, état : {}\n'.format(joueur.nom,joueur.etat.description)
    await bot.say(message)
    
    
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
    if len(bot.servers)>1:
        raise NotImplementedError('Juste un serveur à la fois')
    
    for personne in bot.get_all_members():
        if personne.id==bot.user.id:
            continue
        bot.groupe.ajouter_joueur(pl.Joueur(nom=personne.name,discordID=personne.id,role=pl.Roles.loup_garou,etat=pl.Etat.vivant))