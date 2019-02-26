# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 12:53:34 2019

@author: tete5
"""
import enum

class descrEnum(str,enum.Enum):
    @property
    def description(self):
        return self.value

class Etat(descrEnum):
    vivant="duh"
    mort="encore duh"

class Clan(descrEnum):
    village="aaa"
    loup="zzzz"

class Roles(enum.Enum):
    villageois=("pauvre péon sans intérêt",Clan.village)
    loup_garou=("le vrai MVP",Clan.loup)
    
    @property
    def description(self):
        return self.value[0]
    
    @property
    def clan(self):
        return self.value[1]

class Joueur():
    def __init__(self,nom='',discordID='',role='',etat=''):
        self.nom=nom
        self.discordID=discordID
        self.role=role
        self.etat=etat

class Groupe():
    def __init__(self,liste_joueurs=[]):
        self.liste_joueurs=liste_joueurs
        
    def ajouter_joueur(self,joueur):
        if type(joueur)!=type(Joueur()):
            raise TypeError('les joueurs doivent être du type Joueur() !')
        self.liste_joueurs+=[joueur]
    
    def ayant_role(self,role,en_vie=False):
        for joueur in self.liste_joueurs :
            if joueur.role==role and ( (not en_vie) or joueur.etat==Etat.vivant):
                yield joueur
    
    def avoir_par_ID(self,discordID):
        for joueur in self.liste_joueurs:
            if joueur.discordID == discordID:
                return joueur
        logger.warning("ID {} inconnu".format(str(discordID)))
        
    def ayant_clan(self,clan):
        for joueur in self.liste_joueur :
            if joueur.role.clan==clan:
                yield joueur
        
        
        
        
        
        