# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 12:53:34 2019

@author: tete5
"""

from role import Clan,Roles,RoleInfo,Etat,Temps

class Joueur():
    def __init__(self,nom='',discordID='',role=Roles.villageois,etat=''):
        self.nom=nom
        self.discordID=discordID
        self.role=RoleInfo(role)
        self.etat=etat
    
    def recharger(self):
        pass
    
    def tuer(self):
        #TODO:Rajouter les pouvoirs à la mort ici, et tester !
        self.etat=Etat.mort
        return "Tu es mort !"

class Groupe():
    def __init__(self,liste_joueurs=[]):
        self._liste_joueurs=liste_joueurs
        self._iterable=0
        self.tués_nuit=[]
        self.tués_jour=[]
        self.égalité=''
        self.votes={}
        
    def __iter__(self):
        #TODO : à tester !!!
        self._iterable=iter(self._liste_joueurs)
        return self
    
    def __next__(self):
        return next(self._iterable)
        
    def ajouter_joueur(self,joueur):
        if type(joueur)!=type(Joueur()):
            raise TypeError('les joueurs doivent être du type Joueur() !')
        self._liste_joueurs+=[joueur]
    
    def ayant_role(self,role,en_vie=False):
        for joueur in self._liste_joueurs :
            if joueur.role==role and ( (not en_vie) or joueur.etat==Etat.vivant):
                yield joueur
    
    def avoir_par_ID(self,discordID):
        for joueur in self._liste_joueurs:
            if joueur.discordID == discordID:
                return joueur
        logger.warning("ID {} inconnu".format(str(discordID)))
    
    def avoir_par_nom(self,nom):
        for joueur in self._liste_joueurs:
            if joueur.nom == nom:
                return joueur
        return -1
        
    def ayant_clan(self,clan):
        for joueur in self._liste_joueurs:
            if joueur.role.clan==clan:
                yield joueur
    
    def ayant_etat(self,etat):
        for joueur in self._liste_joueurs:
            if joueur.etat==etat:
                yield joueur
        
        
        
        
        
        