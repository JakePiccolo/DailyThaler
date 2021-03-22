import asyncio
import requests
from bs4 import BeautifulSoup

import discord # Discord API
from discord.ext import commands

TOKEN = 'insert token'
GUILD = 'BoizBoizBoiz'

# Create dice bot and register commands
bot = commands.Bot(command_prefix=':', description="A Discord chat bot to pull the latest Thaler rotation.")


def getthaler(soup, topn):
    lim = 0 
    wlist = []
    for items in soup.find('table', class_='wikitable').find_all('tr'):
        data = items.find_all(['th','td'])
        try:
            what = data[0].a.text
            when = data[0].a.find_next_sibling().text
            #url = data[0].a
            #url = url['href']
            wlist.append(what + ', ' + when)
            lim = lim + 1
            if lim > topn: break 
        except IndexError:pass
    return wlist
   

def getupdate(soup):
    trs = soup.find('table', class_='wikitable').find_all('b')
    return trs[0].text


@bot.command(name = 'qs', description = 'Pulls Daily Thaler quests')
async def quests(ctx):
    author = ctx.message.author
    URL = "https://runescape.wiki/w/Thaler"
    res = requests.get(URL).text
    soup = BeautifulSoup(res,'lxml')
    try:
        await ctx.send('{0}, Here are the last ten Thaler Minigames:'.format(author.mention))
        questlist = []
        for quest in getthaler(soup, topn = 10):
            questlist.append(quest)
        await ctx.send('\n'.join(questlist))
        url = getupdate(soup)
        await ctx.send('Updates in '+ url)
    except Exception as err: 
        await ctx.send('Sorry that did not work {0}. Here is the issue: {1}'.format(author.mention, err))

bot.run(TOKEN)

doit()