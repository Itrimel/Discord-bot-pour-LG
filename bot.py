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
        
        for joueur in self.groupe.ayant_etat(pl.Etat.vivant):
            res = joueur.role.fin_nuit(self.groupe)
            if res:
                await self.send_message(await self.get_user_info(joueur.discordID),res)
            if joueur.role.clan==pl.Clan.loup:
                await self.send_message(await self.get_user_info(joueur.discordID),"Le vote des loups-garous est fermé.")

    
    async def debut_jour(self):
        tués=self.groupe.tués_nuit
        for personne in tués:
            joueur = self.groupe.avoir_par_nom(personne)
            message = joueur.tuer()
            await self.send_message(await self.get_user_info(joueur.discordID),message)
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
                await self.send_message(await self.get_user_info(joueur.discordID),res)

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
        
        await self.send_message(self.channel_annonces,message)

        tués=self.groupe.tués_jour
        for personne in tués:
            joueur = self.groupe.avoir_par_nom(personne)
            message = joueur.tuer()
            await self.send_message(await self.get_user_info(joueur.discordID),message)
        
        self.groupe.tués_jour=[]
        self.groupe.égalité=''
        self.groupe.votes={}
        
        await self.send_message(self.channel_annonces,'La nuit se lève, prenez garde !')
        
        #TODO : Mettre ici les messages à envoyer pour les pouvoirs nocturnes
        for joueur in self.groupe.ayant_clan(pl.Clan.loup):
            if joueur.etat==pl.Etat.vivant:
                await self.send_message(await self.get_user_info(joueur.discordID),"Le vote des loups-garous est ouvert.")

        
bot=BotLG(command_prefix='!',command_not_found='Je ne connais pas la commande {} ...')

#TODO : tester vote
@bot.command(pass_context=True)
async def vote(context):
    message=context.message
    if message.channel.is_private==False:
        await bot.delete_message(message)
        await bot.send_message(await bot.get_user_info(message.author.id),'On vote en MP ! :angry:')
    elif not (bot.temps == pl.Temps.jour or (bot.temps == pl.Temps.nuit and bot.groupe.avoir_par_ID(message.author.id).role.clan==pl.Clan.loup)):
        await bot.say("Pourquoi voter ? Ce n'est pas le moment")
    elif bot.groupe.avoir_par_ID(message.author.id).nom in bot.groupe.votes :
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
        await bot.send_message(await bot.get_user_info(message.author.id),"Le pouvoir s'utilise en MP ! :angry:")
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
    
    persos={}
    with open("init.csv",'r') as file:
        for line in file:
            persos[line.split('\t')[0]]=line.split('\t')[1][:-1]
    
    for user in bot.get_all_members():
        if user.name in persos:
            role_user=''
            for role in list(pl.Roles):
                if role.value[0]==persos[user.name]:
                    role_user=role
            if role_user=='':
                raise ValueError('Rôle inconnu : {}'.format(persos[user.name]))
            bot.groupe.ajouter_joueur(pl.Joueur(nom=user.name,discordID=user.id,role=role_user,etat=pl.Etat.vivant))
            persos.pop(user.name, None)
    if len(persos)!=0:
        message='Nom de joueur inconnu :'
        for key in persos:
            message+=' {},'.format(persos[key])
        message=message[:-1]
        raise ValueError(message)