import asyncio
import requests
from bs4 import BeautifulSoup

import discord # Discord API
from discord.ext import commands

TOKEN = 'insert token here'
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
            url = data[0].a
            url = url['href']
            wlist.append(what + ', ' + when + ', ' + 'https://runescape.wiki' + url)
            lim = lim + 1
            if lim > topn: break 
        except IndexError:pass
    return wlist
   

def getupdate(soup):
    trs = soup.find('table', class_='wikitable').find_all('b')
    return trs[0].text


@bot.command(name = 'dt', description = 'Pulls Daily Thaler quests')
async def quests(ctx):
    author = ctx.message.author
    URL = "https://runescape.wiki/w/Thaler"
    res = requests.get(URL).text
    soup = BeautifulSoup(res,'lxml')
    try:
        embed = discord.Embed(title = "Thaler Minigames", 
        description = "These are the next ten Minigames:", 
        color = discord.Color.red(),
        icon_url = 'https://static.wikia.nocookie.net/runescape2/images/b/b1/Minigame_Spotlight_update_post_header.jpg/revision/latest/scale-to-width-down/629?cb=20150518110749'
        )
        #await ctx.send('{0}, Here are the next ten Thaler Minigames:'.format(author.mention))
        questlist = []
        for quest in getthaler(soup, topn = 10):
            questlist.append(quest)
        #await ctx.send('\n'.join(questlist))
        embed.add_field(name = "Minigame List", value = '\n'.join(questlist), inline = False )

        upd = getupdate(soup)
        embed.add_field(name = "Updates in ", value = upd, inline = True)
        #await ctx.send('Updates in '+ upd)
        await ctx.send(embed = embed)
    except Exception as err: 
        await ctx.send('Sorry that did not work {0}. Here is the issue: {1}'.format(author.mention, err))

bot.run(TOKEN)
