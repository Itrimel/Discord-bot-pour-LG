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
        self.temps=pl.Temps.matin
        self.votes={}
        self.channel_annonces=0
    
    async def debut_nuit(self):
        self.votes={}
        self.temps=pl.Temps.matin
        await self.send_message(self.channel_annonces,'La nuit se lève, prenez garde !')
        #TODO : Mettre ici les messages à envoyer pour les pouvoirs nocturnes
        for joueur in self.groupe.ayant_clan(pl.Clan.loup):
            await self.send_message(self.get_user_info(joueur.id),"Le vote des loups-garous est ouvert.")
    
    async def fin_nuit(self):
        
        for joueur in self.groupe.ayant_etat(pl.Etat.vivant):
            res = joueur.role.fin_nuit()
            if res:
                await self.send_message(self.get_user_info(joueur.id),res)
        
        self.temps=pl.Temps.matin
        decompte={}
        for vote in self.votes.values() :
            if vote not in decompte :
                decompte[vote]=1
            else :
                decompte[vote]+=1
        tué=max(decompte, key=lambda key: decompte[key])
        if sum(nb_votes==decompte[tué] for nb_votes in decompte.values())>1 :
            message="Le jour se lève.\n Cette nuit, personne n'a été tué."
        else:
            self.groupe.avoir_par_nom(tué).changer_etat(pl.Etat.mort)
            message="Le jour se lève.\n Cette nuit, {} a été tué.".format(tué)
        await self.send_message(self.channel_annonces,message)
    
    async def debut_jour(self):
        self.votes={}
        self.temps=pl.Temps.jour
        await self.send_message(self.channel_annonces,"Le vote du jour est ouvert.")

    async def fin_jour(self):
        self.temps=pl.Temps.soir
        decompte={}
        for (votant,vote) in self.votes.items():
            if vote not in decompte :
                decompte[vote]=[votant]
            else:
                decompte[vote]+=1
        tué=max(decompte, key=lambda key: len(decompte[key]))
        message="Le vote est fini. Le décompte est le suivant :\n"
        for voté in decompte:
            message+="{} :".format(voté)
            for votant in decompte[voté]:
                message+=" {},".format(votant)
            message=message[:-1]+"\n"
        if sum(len(nb_votes)==len(decompte[tué]) for nb_votes in decompte.values())>1 :
            #TODO : demander l'avis de l'ancien
            #Sinon
            message+="Il n'y a pas de tué aujourd'hui"
        else:
            message+="Le tué est {} avec {} voix contres".format(tué,len(decompte[tué]))
            self.groupe.avoir_par_nom(tué).changer_etat(pl.Etat.mort)
        await self.send_message(self.channel_annonces,message)


bot=BotLG(command_prefix='!',command_not_found='Je ne connais pas la commande {} ...')

#TODO : tester vote
@bot.command(pass_context=True)
async def vote(context):
    message=context.message
    if message.channel.is_private==False:
        await bot.delete_message(message)
        await bot.send_message(bot.get_user_info(message.author.id),'On vote en MP ! :angry:')
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
            bot.votes[bot.groupe.avoir_par_ID(message.author.id).nom]=vote
            await bot.say('Tu as voté pour {}'.format(vote))
            

@bot.command()
async def etat():
    message=''
    for joueur in bot.groupe:
        message+='Nom : {}, état : {}\n'.format(joueur.nom,joueur.etat.description)
    await bot.say(message)
    
    
#TODO : rajouter les pouvoirs un par un, tester voyante
@bot.command(pass_context=True)
async def pouvoir(context):
    message=context.message
    joueur=bot.groupe.avoir_par_ID(message.author.id)
    if message.channel.is_private==False:
        await bot.delete_message(message)
        await bot.send_message(bot.get_user_info(message.author.id),"Le pouvoir s'utilise en MP ! :angry:")
    else:
        texte=message.content[6:]
        validité=joueur.role.est_valide(texte,bot.groupe,bot.temps)
        if validité[0]==False:
            await bot.say(validité[1])
        else:
            réponse =joueur.role.faire_pouvoir(texte,bot.groupe)
            await bot.say(réponse)
    
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