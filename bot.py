# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 14:34:11 2019

@author: tete5
"""

from discord.ext.commands import Bot
import joueur as pl

class BotLG(Bot):
    def __init__(self,groupe=pl.Groupe(),*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.groupe=groupe
        self.jour=True
        self.nuit=False
        self.votes={}
        self.channel_annonces=0
    
    async def debut_nuit(self):
        self.votes={}
        self.nuit=True
        await self.send_message(self.channel_annonces,'La nuit se lève, prenez garde !')
        #TODO : Mettre ici les messages à envoyer pour les pouvoirs nocturnes
        for joueur in self.groupe.ayant_clan(pl.Clan.loup):
            await self.send_message(self.get_user_info(joueur.id),"Le vote des loups-garous est ouvert.")
    
    async def fin_nuit(self):
        self.nuit=False
        decompte={}
        for vote in self.votes.values() :
            if vote not in decompte :
                decompte[vote]=1
            else :
                decompte[vote]+=1
        #TODO : que faire en cas d'égalité ?
        tué=max(decompte, key=lambda key: decompte[key])
        self.groupe.changer_etat(tué,pl.Etat.mort)
        message="Le jour se lève.\n Cette nuit, {} a été tué.".format(tué)
        await self.send_message(self.channel_annonces,message)
    
    async def debut_jour(self):
        self.votes={}
        self.jour=True
        await self.send_message(self.channel_annonces,"Le vote du jour est ouvert.")

    async def fin_jour(self):
        self.jour=False
        decompte={}
        for (votant,vote) in self.votes.items():
            if vote not in decompte :
                decompte[vote]=[votant]
            else:
                decompte[vote]+=1
        #TODO : penser à rajouter l'ancien en cas d'égalité
        tué=max(decompte, key=lambda key: len(decompte[key]))
        
        message="Le vote est fini. Le décompte est le suivant :\n"
        for voté in decompte:
            message+="{} :".format(voté)
            for votant in decompte[voté]:
                message+=" {},".format(votant)
            message=message[:-1]+"\n"
        message+="Le tué est {} avec {} voix contres".format(tué,len(decompte[tué]))
        await self.send_message(self.channel_annonces,message)
        
        self.groupe.changer_etat(tué,pl.Etat.mort)


bot=BotLG(command_prefix='!',command_not_found='Je ne connais pas la commande {} ...')

@bot.command(pass_context=True)
async def vote(context):
    message=context.message
    if message.channel.is_private==False:
        await bot.delete_message(message)
        await bot.say('On vote en MP ! 😠')
    elif not (bot.jour or (bot.nuit and bot.groupe.avoir_par_ID(message.author.id).role.clan==pl.Clan.loup)):
        await bot.say("Pourquoi voter ? Ce n'est pas le moment")
    elif message.author.id in bot.votes :
        await bot.say("Tu as déjà voté petit coquin")
    else:
        vote=message.content[6:]
        joueur=bot.groupe.avoir_par_nom(vote)
        if joueur==-1:
            await bot.say("Joueur inconnu")
        elif joueur.etat==pl.Etat.mort:
            await bot.say("Joueur mort")
        else:
            bot.votes[message.author.id]=vote
            await bot.say('Tu as voté pour {}'.format(vote))
            

@bot.command()
async def etat():
    message=''
    for joueur in bot.groupe:
        message+='Nom : {}, état : {}\n'.format(joueur.nom,joueur.etat.description)
    await bot.say(message)
    
    
#TODO:implémenter une commande pouvoir qui permet d'utiliser son pouvoir, et les rajouter un par un
    
    
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
    if len(bot.servers)>1:
        raise NotImplementedError('Juste un serveur à la fois')
    for channel in bot.get_all_channels():
        if channel.name==CHANNEL_ANNONCES:
            bot.channel_annonces=channel
            break
    
    for personne in bot.get_all_members():
        if personne.id==bot.user.id:
            continue
        bot.groupe.ajouter_joueur(pl.Joueur(nom=personne.name,discordID=personne.id,role=pl.Roles.loup_garou,etat=pl.Etat.vivant))