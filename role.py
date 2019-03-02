# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 13:25:53 2019

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

class Temps(descrEnum):
    matin='matin'
    jour='jour'
    soir='soir'
    nuit='nuit'
    
class Roles(enum.Enum):
    villageois=("pauvre péon sans intérêt",Clan.village)
    voyante=("voyante",Clan.village)
    loup_garou=("le vrai MVP",Clan.loup)


class RoleInfo():
    def __init__(self,role):
        self._role=role
        self.clan=role.value[1]
        self.description=role.value[0]
        if role == Roles.voyante:
            self.résultat=''
            self.utilisation=0
        
    def get(self,**kwargs):
        return self._role
    
    def est_tué():
        pass
    
    def est_valide(self,message,groupe,temps):
        if self._role == Roles.voyante:
            tmp = groupe.avoir_par_nom(message)
            if temps != Temps.nuit:
                return [False,"Ce pouvoir s'utilise de nuit"]
            elif self.utilisation ==1 :
                return [False,'Pouvoir déjà utilisé']
            elif tmp == -1:
                return [False,'Joueur inconnu']
            elif tmp.etat == Etat.mort :
                return [False,'Joueur mort']
            else:
                return[True]
    
    def faire_pouvoir(self,texte,groupe):
        if self._role == Roles.voyante:
            role_demandé=groupe.avoir_par_nom(texte).role.get(demandeur=Roles.voyante).value[0]
            self.résultat='{} a le rôle {}'.format(texte,role_demandé)
            self.utilisation=1
            return 'Bien enregistré, résultat au matin'
    
    def fin_nuit(self):
        if self._role == Roles.voyante :
            if self.utilisation ==1 :
                self.utilisation = 0
                return  self.résultat
            else :
                return False