# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 18:43:18 2019

@author: tete5
"""

import aiocron

@aiocron.crontab('0 20 * * *')
async def debut_nuit():
    bot.debut_nuit()

@aiocron.crontab('0 12 * * *')
async def debut_jour():
    bot.debut_jour()

@aiocron.crontab('0 11 * * *')
async def fin_nuit():
    bot.fin_nuit()

@aiocron.crontab('0 19 * * *')
async def fin_jour():
    bot.fin_jour()
    