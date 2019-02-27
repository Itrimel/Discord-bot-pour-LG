# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 18:43:18 2019

@author: tete5
"""

import aiocron

@aiocron.crontab('0 20 * * *')
async def debut_nuit():
    await bot.debut_nuit()

@aiocron.crontab('0 12 * * *')
async def debut_jour():
    await bot.debut_jour()

@aiocron.crontab('0 11 * * *')
async def fin_nuit():
    await bot.fin_nuit()

@aiocron.crontab('0 19 * * *')
async def fin_jour():
    await bot.fin_jour()
    