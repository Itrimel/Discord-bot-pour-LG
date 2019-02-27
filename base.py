# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 19:03:43 2019

@author: tete5
"""
from bot import *
from token_file import TOKEN
import logging
import event

CHANNEL_ANNONCES='général'

#Mise en place du logging
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot.run(TOKEN)
