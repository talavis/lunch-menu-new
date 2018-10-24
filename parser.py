#!/usr/bin/env python3

# Copyright (c) 2014-2016, Linus Östberg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of kimenu nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
Parsers of the menu pages for the restaurants at Karolinska Institutet
'''

from datetime import date

import requests
from bs4 import BeautifulSoup


def fix_for_html(text):
    '''
    HTML formatting of characters
    '''
    text = text.replace('ö', '&ouml;')
    text = text.replace('Ö', '&Ouml;')
    text = text.replace('å', '&aring;')
    text = text.replace('Å', '&Aring;')
    text = text.replace('ä', '&auml;')
    text = text.replace('Ä', '&Auml;')
    text = text.replace('é', '&eacute;')
    text = text.replace('è', '&egrave;')
    text = text.replace('í', '&iacute;')
    text = text.replace('ì', '&igrave;')
    text = text.replace('à', '&agrave;')
    text = text.replace('á', '&aacute;')
    text = text.replace('ô', '&ocirc;')
    text = text.replace('ü', '&uuml;')
    text = text.replace('Ä', '&Auml;')
    text = text.replace('´', '&#39;')
    text = text.replace('`', '&#39;')
    text = text.replace('ç', '&ccedil;')
    text = text.replace('”', '&quot;')
    text = text.replace('Ã¨', '&egrave;')
    text = text.replace('Ã¤', '&auml;')
    text = text.replace('Ã', '&Auml;')
    text = text.replace('Ã', '&Auml;')
    text = text.replace('Ã¶', '&ouml;')
    text = text.replace('Ã©', '&eacute;')
    text = text.replace('Ã¥', '&aring;')
    text = text.replace(' ', '')
    text = text.replace('Ã', '&Aring')
    # Karolina
    text = text.replace('å', '&aring;')
    text = text.replace('ä', '&auml;')
    text = text.replace('ö', '&ouml;')
    text = text.replace('Ä', '&Auml;')

    text = text.strip()

    return text


### date management start ###
def get_day():
    '''
    Today as digit
    '''
    return date.today().day


def get_monthdigit():
    '''
    Month as digit
    '''
    return date.today().month


def get_month():
    '''
    Month name
    '''
    months = {1: 'januari', 2: 'februari', 3: 'mars', 4: 'april',
              5: 'maj', 6: 'juni', 7: 'juli', 8: 'augusti',
              9: 'september', 10: 'oktober', 11: 'november', 12: 'december'}

    return months[get_monthdigit()]


def get_week():
    return date.today().isocalendar()[1]


def get_weekday(lang='sv', tomorrow=False):
    '''
    Day name in swedish(sv) or english (en)
    '''
    wdigit = get_weekdigit()
    if tomorrow:
        wdigit += 1
    if lang == 'sv':
        weekdays = {0: 'måndag', 1: 'tisdag', 2: 'onsdag', 3: 'torsdag',
                    4: 'fredag', 5: 'lördag', 6: 'söndag', 7: 'måndag'}
    if lang == 'en':
        weekdays = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday',
                    4: 'friday', 5: 'saturday', 6: 'sunday', 7: 'monday'}
    return weekdays[wdigit]


def get_weekdigit():
    return date.today().weekday()


def get_year():
    '''
    Year as number
    '''
    return date.today().year
### date management end ###

### parsers start ###
def parse_bikupan(resdata):
    '''
    Parse the menu of Restaurang Bikupan
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Uppsala',
                              resdata[2], resdata[4])

    page_req = requests.get(resdata[3])
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')

    soup = BeautifulSoup(page_req.text, 'html.parser')
    relevant = soup.find("div", {"class": "col-md-3 hors-menu text-center"})
    rel2 = relevant.find_all("div", {"class": "col-xs-10 text-left"})
    for dish in rel2:
        lines.append(dish.get_text().strip().replace('\n', ' ') + '<br/>')
    lines += restaurant_end()
    return lines


def parse_glada(resdata):
    '''
    Parse the menu of Glada restaurangen
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    # No way I'll parse this one. If anyone actually wants to, I'd be happy to accept a patch.

    lines += restaurant_end()
    return lines


def parse_haga(resdata):
    '''
    Print a link to the menu of Haga gatukök
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])
    lines += restaurant_end()
    return lines


def parse_hjulet(resdata):
    '''
    Parse the menu of Restaurang Hjulet
    '''
    day = get_day()
    month = get_month()
    today = get_weekday()

    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    page_req = requests.get(resdata[3])
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')

    soup = BeautifulSoup(page_req.text, 'html.parser')
    try:
        # find the weekday index
        day_index = None
        i = 0
        for header in soup.find_all('table')[0].find_all('th'):
            if today in str(header).lower() and str(day) in str(header).lower() and month in str(header).lower():
                day_index = i
            i += 1
        # get the menu
        if day_index != None:
            menu = soup.find_all('table')[0].find_all('td')[(day_index)*3:(day_index+1)*3]
            for i in range(len(menu)):
                menu[i] = fix_for_html(remove_html(str(menu[i])))
                menu[i] = menu[i].replace('\n', '<br/>')
                if menu[i].strip():
                    lines.append(menu[i] + '<br/>')
        else:
            pass
    except Exception:
        pass
    lines += restaurant_end()

    return lines


def parse_jons(resdata):
    '''
    Parse the menu of Jöns Jacob
    '''
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow=True)
    day = get_day()
    month = get_month()
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    start = False
    today = '{wday}  {iday} {mon}'.format(wday=weekday, iday=day, mon=month)
    today_alt = '{wday} {iday} {mon}'.format(wday=weekday, iday=day, mon=month)
    current = list()
    page_req = requests.get(resdata[3])
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')
    for line in page_req.text.split('\n'):
        if today in line.lower() or today_alt in line.lower():
            start = True
            continue
        if start and (tomorrow in line.lower() or '<!-- contact -->' in line.lower()):
            break
        if start:
            tmp = fix_for_html(remove_html(line.strip()))
            if tmp.strip():
                current.append(tmp.strip())
            if '</tr>' in line:
                if current:
                    lines.append(' '.join(current) + '<br/>')
                    current = list()

    lines += restaurant_end()
    return lines


def parse_jorpes(resdata):
    '''
    Parse the menu of Resturang Jorpes
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])
    lines += restaurant_end()
    return lines


def parse_karolina(resdata):
    '''
    Parse the menu of Restaurang Karolina
    '''
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow=True)
    day = get_day()
    month = get_month()
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    start = False
    today = '{wday} {iday} {mon}'.format(wday=weekday, iday=day, mon=month)
    today_alt = '{wday}  {iday} {mon}'.format(wday=weekday, iday=day, mon=month)
    current = list()
    page_req = requests.get(resdata[3])
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')
    for line in page_req.text.split('\n'):
        if today in line.lower() or today_alt in line.lower():
            start = True
            continue
        if start and (tomorrow in line.lower() or 'gäller hela veckan' in line.lower()):
            break
        if start:
            tmp = fix_for_html(remove_html(line))
            if tmp.strip():
                current.append(tmp.strip())
            if '</tr>' in line:
                if current:
                    lines.append(' '.join(current) + '<br/>')
                    current = list()

    lines += restaurant_end()
    return lines


def parse_mollan(resdata):
    '''
    Parse the menu of Mollan
    '''
    week = get_week()

    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    page_req = requests.get(resdata[3])
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')
    soup = BeautifulSoup(page_req.text, 'html.parser')

    # get the right div
    relevant = soup.find("div", {"class": "self mobile-leaf text textnormal mobile-undersized-upper"})
    # should be "Vecka " followed by week number
    if str(week) in relevant.find('span').get_text().strip():
#        try:
#            fix_for_html(remove_html(str(relevant.find_all('span')[base + i]))) + '<br/>')
#            wdigit = get_weekdigit()
#            if wdigit < 5:
#                base = 2 + 7*wdigit
#                for i in range(6):
#                    lines.append(
#        except Exception:
        pass # add error logging later

    lines += restaurant_end()

    return lines


def parse_nanna(resdata):
    '''
    Parse the menu of Nanna Svartz
    '''
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow=True)
    week = get_week()

    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    start = False
    page_req = requests.get(resdata[3])
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')
    for line in page_req.text.split('\n'):
        if 'meny' in line.lower() and 'vecka' in line.lower():
            if not str(week) in line:
                break
        # looking for the lines where the menu is listed in bold text
        if weekday in line.lower() and 'h3' in line.lower():
            start = True
            continue
        # alternative formatting
        if weekday in line.lower() and '<strong>' in line.lower():
            start = True
            continue
        # end of day
        if start and (tomorrow in line.lower() or '<div class="span6">' in line):
            break
        if start and len(remove_html(line.strip())) > 1:
            lines.append(fix_for_html(remove_html(line.strip())) + '<br/>')

    lines += restaurant_end()

    return lines


def parse_subway(resdata):
    '''
    Print info about Subway
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])
    lines += restaurant_end()
    return lines


def parse_svarta(resdata):
    '''
    Parse the menu of Svarta Räfven
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    page_req = requests.get(resdata[3])
    soup = BeautifulSoup(page_req.text, 'html.parser')

    try:
        relevant = soup.find("div", {"class": "span6"}).find_all('p')
        # pre
        lines.append(fix_for_html(relevant[0].get_text().split('\n')[0]) + '<br/>')
        # main
        lines.append(fix_for_html(relevant[1].get_text().split('\n')[0]) + '<br/>')
        # dessert
        lines.append(fix_for_html(relevant[2].get_text().split('\n')[0]) + '<br/>')
    except AttributeError:
        # Webpage offline
        pass

    lines += restaurant_end()

    return lines

### parsers end ###

def remove_html(text):
    '''
    Remove HTML tags
    '''
    text = text.replace('&nbsp;', ' ')
    # assumes all < are part of html tags
    try:
        while text.count('<') > 0:
            text = text[:text.index('<')] + text[text.index('>')+1:]
    except:
        pass
    return text


def restaurant_end():
    '''
    Finish the tags after the listing of the menu of a restaurant
    '''
    lines = list()
    lines.append('</p>')
    lines.append('</div>')
    return lines


def restaurant_start(restaurant, location, home_url, mapurl):
    ''''
    Start the listing of the menu of a restaurant
    '''
    lines = list()
    lines.append('<!--{}-->'.format(restaurant))
    lines.append('''<div class="title"><a href="{url}"> {rest}</a> (<a href="{murl}">{loc}</a>)</div>'''.format(rest=restaurant,
                                                                                                                url=home_url,
                                                                                                                loc=location,
                                                                                                                murl=mapurl))
    lines.append('<div class="menu">')
    lines.append('<p>')
    return lines
