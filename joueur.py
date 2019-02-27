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
    vivant="vivant"
    mort="mort"

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
        self._liste_joueurs=liste_joueurs
        
    def __iter__(self):
        self._iter_pos=0
        return self
    
    def __next__(self):
        if self._iter_pos < len(self._liste_joueurs):
            self._iter_pos+=1
            return(self._liste_joueurs[self._iter_pos-1])
        else:
            raise StopIteration
        
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
        for joueur in self._liste_joueur :
            if joueur.role.clan==clan:
                yield joueur
    
    def ayant_etat(self,etat):
        for joueur in self.liste_joueurs:
            if joueur.etat==etat:
                yield joueur
        
        
        
        
        
        