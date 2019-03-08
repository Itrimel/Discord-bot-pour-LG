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
        self.channel_annonces='annonces'
        self.message_vote=''
        
    async def fin_nuit(self):
        self.temps=pl.Temps.matin
        
        decompte={}
        for vote in self.groupe.votes.values() :
            if vote not in decompte :
                decompte[vote]=1
            else :
                decompte[vote]+=1
        if len(decompte)!=0:
            tué_loups=max(decompte, key=lambda key: decompte[key])
            if tué_loups not in self.groupe.tués_nuit:
                self.groupe.tués_nuit+=[tué_loups]
        
        for joueur in self.groupe.ayant_clan(pl.Clan.loup):
            await self.send_message(await self.get_user_info(joueur.discordID),"Le vote des loups-garous est fermé.")

        
        for joueur in self.groupe.ayant_etat(pl.Etat.vivant):
            res = joueur.role.fin_nuit(self.groupe)
            if res:
                await self.send_message(self.get_user_info(joueur.id),res)
    
    async def debut_jour(self):
        tués=self.groupe.tués_nuit
        for personne in tués:
            joueur = self.groupe.avoir_par_nom(personne)
            message = joueur.tuer()
            await self.send_message(self.get_user_info(joueur.id),message)
        self.groupe.tués_nuit=[]
        
        if len(tués)==0:
             message="Le jour se lève.\nCette nuit, personne n'a été tué."
        elif len(tués)==1: 
            message="Le jour se lève.\nCette nuit, {} a été tué.".format(tués[0])
        else:
            message="Le jour se lève.\nCette nuit"
            for i in range(len(tués)-1):
                message+=', {}'.format(tués[i])
            " et {} ont été tués.".format(tués[-1])
        await self.send_message(self.channel_annonces,message)
        
        self.groupe.votes={}
        self.temps=pl.Temps.jour
        await self.send_message(self.channel_annonces,"Le vote du jour est ouvert.")

    async def fin_jour(self):
        self.temps=pl.Temps.soir
        message='Le vote est fermé.'
        
        for joueur in self.groupe.ayant_etat(pl.Etat.vivant):
            res = joueur.role.fin_jour(self.groupe)
            if res:
                await self.send_message(self.get_user_info(joueur.id),res)

        await self.send_message(self.channel_annonces,message)

    async def debut_nuit(self):
        self.temps=pl.Temps.nuit
        
        decompte={}
        for (votant,vote) in self.groupe.votes.items():
            if vote not in decompte :
                decompte[vote]=[votant]
            else:
                decompte[vote]+=1
        if len(decompte)==0:
            message="Pas de votes reçus aujourd'hui"
        else:
            tué=max(decompte, key=lambda key: len(decompte[key]))
            message="Le résultat du vote du village est le suivant :\n"
            for voté in decompte:
                message+="{} :".format(voté)
                for votant in decompte[voté]:
                    message+=" {},".format(votant)
                    message=message[:-1]+"\n"
                    if sum(len(nb_votes)==len(decompte[tué]) for nb_votes in decompte.values())>1 :
                        if len (self.groupe.égalité)!=0:
                            message+="Le tué est {} avec {} voix contres".format(self.groupe.égalité,len(decompte[self.groupe.égalité]))
                            if self.groupe.égalité not in self.groupe.tués_jour:
                                self.groupe.tués_jour+=[self.groupe.égalité]
                        else:
                            message+="Il n'y a pas de tué par vote du village aujourd'hui"
                    else:
                        message+="Le tué est {} avec {} voix contres".format(tué,len(decompte[tué]))
                        self.groupe.tués_jour+=[tué]

        tués=self.groupe.tués_jour
        for personne in tués:
            joueur = self.groupe.avoir_par_nom(personne)
            message = joueur.tuer()
            await self.send_message(self.get_user_info(joueur.id),message)
        
        self.groupe.tués_jour=[]
        self.groupe.égalité=''
        
        await self.send_message(self.channel_annonces,message)
        await self.send_message(self.channel_annonces,'La nuit se lève, prenez garde !')
        
        #TODO : Mettre ici les messages à envoyer pour les pouvoirs nocturnes
        for joueur in self.groupe.ayant_clan(pl.Clan.loup):
            await self.send_message(await self.get_user_info(joueur.discordID),"Le vote des loups-garous est ouvert.")

        
bot=BotLG(command_prefix='!',command_not_found='Je ne connais pas la commande {} ...')

#TODO : tester vote
@bot.command(pass_context=True)
async def vote(context):
    message=context.message
    if message.channel.is_private==False:
        gen = await bot.get_user_info(message.author.id) #besoin de faire ça pour que l'envoi de message marche ...
        await bot.delete_message(message)
        await bot.send_message(gen,'On vote en MP ! :angry:')
    elif not (bot.temps == pl.Temps.jour or (bot.temps == pl.Temps.nuit and bot.groupe.avoir_par_ID(message.author.id).role.clan==pl.Clan.loup)):
        await bot.say("Pourquoi voter ? Ce n'est pas le moment")
    elif message.author.id in bot.groupe.votes :
        await bot.say("Tu as déjà voté petit coquin")
    else:
        vote=message.content[6:]
        joueur=bot.groupe.avoir_par_nom(vote)
        if joueur==-1:
            await bot.say("Joueur inconnu")
        elif joueur.etat==pl.Etat.mort:
            await bot.say("Joueur mort")
        else:
            bot.groupe.votes[bot.groupe.avoir_par_ID(message.author.id).nom]=vote
            await bot.say('Tu as voté pour {}'.format(vote))
            

@bot.command()
async def etat():
    message=''
    for joueur in bot.groupe:
        message+='Nom : {}, état : {}\n'.format(joueur.nom,joueur.etat.description)
    await bot.say(message)
    
@bot.command()
async def suivant():
    if bot.temps==pl.Temps.nuit:
        await bot.fin_nuit()
    elif bot.temps==pl.Temps.matin:
        await bot.debut_jour()
    elif bot.temps==pl.Temps.jour:
        await bot.fin_jour()
    elif bot.temps==pl.Temps.soir:
        await bot.debut_nuit()
        
    
    
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
        if channel.name==bot.channel_annonces:
            bot.channel_annonces=channel
            break
    
    for personne in bot.get_all_members():
        if personne.id==bot.user.id:
            continue
        bot.groupe.ajouter_joueur(pl.Joueur(nom=personne.name,discordID=personne.id,role=pl.Roles.loup_garou,etat=pl.Etat.vivant))