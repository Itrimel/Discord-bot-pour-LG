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
    villageois=("villageois",Clan.village)
    voyante=("voyante",Clan.village)
    sorcière=("sorcière",Clan.village)
    loup_garou=("loup garou",Clan.loup)


class RoleInfo():
    def __init__(self,role):
        self._role=role
        self.clan=role.value[1]
        self.description=role.value[0]
        if role == Roles.voyante:
            self.résultat=''
            self.utilisation=0
        if role == Roles.sorcière:
            self.potion_vie=1
            self.potion_mort=1
        
    def get(self,**kwargs):
        return self._role
    
    
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
        
        if self._role == Roles.sorcière:
            if message[:2]!='re' or message[:4]!="tuer":
                return [False,"Format invalide"]
            if message[:2]=='re':
                revive=True
                message=message[2:]
            else:
                revive=False
                message=message[4:]
            tmp = groupe.avoir_par_nom(message)
            if not (temps== Temps.nuit or temps == Temps.matin) and not revive:
                return [False,"Ce pouvoir s'utilise de nuit"]
            if temps != Temps.matin and revive:
                return [False,"Ce pouvoir s'utilise le matin"]
            elif (self.potion_vie ==0 and revive) or (self.potion_mort==0 and not revive):
                return [False,'Pouvoir déjà utilisé']
            elif tmp == -1:
                return [False,'Joueur inconnu']
            elif tmp.etat == Etat.mort and not revive :
                return [False,'Joueur mort']
            elif tmp.etat == Etat.vivant and revive :
                return [False,'Joueur vivant']
            else :
                return [True]
            
        return [False,"Pouvoir non implémenté"]
    
    def faire_pouvoir(self,texte,groupe):
        
        if self._role == Roles.voyante:
            role_demandé=groupe.avoir_par_nom(texte).role.get(demandeur=Roles.voyante).value[0]
            self.résultat='{} a le rôle {}'.format(texte,role_demandé)
            self.utilisation=1
            return 'Bien enregistré, résultat au matin'
        
        if self._role == Roles.sorcière :
            if texte[:2]=='re':
                revive=True
                texte=texte[2:]
            else:
                revive=False
                texte=texte[4:]
            if revive:
                self.groupe.tués_nuit.remove(texte)
                self.potion_vie-=1
            else:
                if texte not in self.groupe.tués_nuits:
                    self.groupe.tués_nuit+=[texte]
                self.potion_mort-=1
            
    
    def fin_nuit(self,groupe):
        if self._role == Roles.voyante :
            if self.utilisation ==1 :
                self.utilisation = 0
                return  self.résultat
        if self._role == Roles.sorcière:
            if len(groupe.tués_nuit)==0:
                message="Personne de tué cette nuit"
            elif len(groupe.tués_nuit)==1: 
                message="{} a été tué cette nuit".format(groupe.tués_nuit[0])
            else:
                message="{}".format(groupe.tués_nuit[0])
                for i in range(1,len(tués)-1):
                    message+=', {}'.format(tués[i+1])
                " et {} ont été tués.".format(tués[-1])
            return False
        return False
    
    def fin_jour(self,groupe):
        return False