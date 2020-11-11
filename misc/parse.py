from typing import Dict, Any

import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime


async def fetch(session, url):
    async with session.get(url, params='class=content-middle') as respone:
        return await respone.text()


async def get_station():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://metroalmaty.kz/?q=ru/schedule-list')
        soup = BeautifulSoup(html, 'lxml')
        block = soup.find('tbody')
        schedule = dict()
        identifier = 0
        for i in block.find_all('tr'):
            i = i.get_text('$').split('$')
            identifier += 1
            try:
                schedule.update({identifier: [i[0], i[1], i[2]]})
            except IndexError:
                try:
                    schedule.update({identifier: [i[0], i[1]]})
                except IndexError:
                    schedule.update({identifier: [i[0], 'closed']})
        return schedule


async def info_station(index: str):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, f'http://metroalmaty.kz/?q=ru/schedule-list-view/{index}')
        soup = BeautifulSoup(html, 'lxml')
        block = soup.find('tbody')
        block2 = soup.find('thead')
        schedule = block2.find_all('th')
        if len(schedule) == 2:
            schedule = 'До станций: <u>' + schedule[0].get_text(strip=True) + '</u>  и  <u>' + \
                       schedule[1].get_text(strip=True) + '</u>\n'
        else:
            schedule = 'До станции: <u>' + schedule[0].get_text() + '</u>\n'
        now = datetime.now().time().hour
        # time = str(now.hour) + ':' + str(now.min)
        for i in block.find_all('tr'):
            i = i.get_text('$').split('$')
            if len(i) == 2:
                log = i[0].split(':')[0]
                if log == str(now+1) or log == str(now+2):
                    schedule += 'Время: <b>' + i[0] + '</b>  и  <b>' + i[1] + '</b>\n'
            else:
                log = i[0].split(':')[0]
                if log == str(now+1) or log == str(now+2):
                    schedule += 'Время: <b>' + i[0] + '</b>\n'
        return schedule
