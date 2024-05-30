#!/usr/bin/env python3

# Copyright (c) 2014-2024, Linus Östberg and contributors
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
"""
Menu parsers.
"""

import re

from parser_helpers import *


@restaurant
def parse_bikupan(res_data: dict) -> dict:
    """
    Parse the menu of Restaurang Bikupan
    """

    def fmt_paragraph(p):
        return p.get_text().strip().replace("\n", " ")

    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])
    # check week number
    target = soup.find("div", {"id": "current"})
    if str(get_week()) not in target.find("h2").text:
        return data
    raw_menu = target.find("div", {"class": "menu-item " + get_weekday(lang="en")})
    for entry in raw_menu.find_all("p"):
        # skip rows with english
        if "class" in entry.attrs and "eng-meny" in entry.attrs["class"]:
            continue
        data["menu"].append(entry.text.strip())

    return data


@restaurant
def parse_biomedicum(res_data):
    """
    No homepage for Café Biomedicum.
    """
    return {"menu": []}


@restaurant
def parse_delta(res_data):
    """
    No homepage for Café Delta.
    """
    return {"menu": []}


@restaurant
def parse_dufva(res_data):
    """
    Parse the menu of Sven Dufva
    """
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])

    relevant = soup.find("div", {"id": "post"})
    menu_data = relevant.get_text().split("\n")
    dag = get_weekday()
    started = False
    for line in menu_data:
        if not line:
            continue
        if line.lower() == f"- {dag} -":
            started = True
            continue
        if started:
            if line[0] != "-":
                data["menu"].append(line.strip())
            else:
                break
    return data


@restaurant
def parse_elma(res_data):
    """Parse the menu of Elma."""
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])

    week_text = soup.find("div", {"class": "dishes-wrapper"}).find("h2").text.strip()
    if week_text == f"LUNCH  V.{get_week()}":
        days = soup.find("div", {"class": "dishes-wrapper"}).find_all(
            "div", {"class": "dish--content"}
        )
        ref_weekday = get_weekday()

        for day in days:
            weekday = day.find("h2").text.strip().lower()
            if ref_weekday == "måndag":
                weekday = weekday.replace(f"a{chr(778)}", "å")  # special encoding on the website
            if weekday not in ("lördag", "söndag") and weekday in (
                ref_weekday,
                "veckans vegetariska",
                "veckans pizza",
            ):
                # dish is first title
                main = day.find("h3", {"class": "dish--title"}).text.strip()
                # followed by extras, potentially multiple tags
                extra = " ".join(
                    [part.text.strip() for part in day.find_all("p", {"class": "dish--desc"})]
                ).strip()
                dish = main
                if extra:
                    dish += " " + extra
                data["menu"].append(dish)

    return data


@restaurant
def parse_glada(res_data):
    """
    Parse the menu of Glada restaurangen
    """
    data = {"menu": []}
    # No way I'll parse this one. If anyone actually wants to, I'd be happy to accept a patch.
    return data


@restaurant
def parse_haga(res_data):
    """
    Empty parser for Haga Gatukök.
    """
    return {"menu": []}


@restaurant
def parse_hubben(res_data):
    """
    Parse the menu of Restaurang Hubben
    """
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])

    days = soup.find_all("div", {"class": "day"})
    current = days[get_weekdigit()]
    dishes = current.find_all("div", {"class": "element description col-md-4 col-print-5"})
    for dish in dishes:
        data["menu"].append(dish.get_text().strip().replace("\n", " "))

    return data


@restaurant
def parse_jons(res_data):
    """
    Parse the menu of Jöns Jacob
    """
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])

    days = soup.find("table", {"class": "table lunch_menu animation"})
    day = days.find("tbody", {"class": "lunch-day-content"})
    dishes = day.find_all("td", {"class": "td_title"})
    data["menu"] += [dish.text.strip() for dish in dishes if dish.text.strip()]

    return data


@restaurant
def parse_jorpes(res_data):
    """
    Parse the menu of Resturang Jorpes
    """
    return {"menu": []}


@restaurant
def parse_kraemer(res_data):
    """
    No menu for Hotel von Kraemer.
    """
    return {"menu": []}


@restaurant
def parse_livet(res_data):
    """
    Parse the menu of Livet
    """
    return {"menu": []}


@restaurant
def parse_maethai(res_data):
    """
    Parse the menu of Mai Thai Express
    """
    return {"menu": []}


@restaurant
def parse_nanna(res_data):
    """Parse the menu of Nanna Svartz."""
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])

    weeks = soup.find_all("div", {"class": "menu-container"})
    for week in weeks:
        try:
            header = week.find("h2", {"class": "section-title"}).text
        except AttributeError:
            continue
        if f"Lunch vecka {get_week()}" in header:
            entries = week.find("div", {"class": get_weekday(lang="en")}).find_all("p")
            for entry in entries:
                tmp = entry.get("class")
                if tmp and "small-title" in tmp:
                    continue
                data["menu"].append(entry.text.strip())

    return data


@restaurant
def parse_omni(res_data):
    """
    Parse the menu of Omni.
    """
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])

    days = soup.find_all("thead", {"class": "lunch-day-header"})

    wanted = f"{get_weekday()} {get_day()} {get_month()}"

    for day in days:
        if wanted in day.text.lower():
            next_tag = day
            while next_tag.name != "tbody":
                next_tag = next_tag.nextSibling
            data["menu"] = [
                tag.text.strip() for tag in next_tag.find_all("td", {"class": "td_title"})
            ]
            break

    return data


@restaurant
def parse_rudbeck(res_data):
    """
    Parse the menu of Bistro Rudbeck
    """
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])

    menu_part = soup.find("div", {"class": "menu-item " + get_weekday(lang="en")})

    for entry in menu_part.find_all("p"):
        if "class" not in entry.attrs:
            text = entry.text.strip()
            if text[0] == "-":
                text = text[1:].lstrip()
            data["menu"].append(text)
    return data


@restaurant
def parse_street(res_data):
    """
    Parse the menu of STHLM Street Food.

    Image-based menu, i.e. no parser.
    """
    return {"menu": []}


@restaurant
def parse_svarta(res_data):
    """Parse the menu of Svarta Räfven."""
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])

    weeks = soup.find_all("div", {"class": "menu-container"})
    for week in weeks:
        try:
            header = week.find("h2", {"class": "section-title"}).text
        except AttributeError:
            continue
        if f"Lunch vecka {get_week()}" in header:
            entries = week.find_all("div", {"class": "menu-item"})
            for entry in entries:
                dish = ""
                for row in entry.find_all("p"):
                    p_class = row.get("class")
                    if p_class:
                        if "menu-en" in p_class:
                            continue
                        if "small-title" in p_class:
                            dish += row.text.strip() + ": "
                    else:
                        dish += row.text.strip()
                data["menu"].append(dish)

    return data


# Frösundavik


@restaurant
def parse_bredbar(res_data: dict) -> dict:
    """
    Parse the menu of Food & Co
    """
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])

    menu = soup.find_all("h1")[1].parent
    data["menu"] = [entry.text[1:] for entry in menu if entry.text.startswith("*")]

    return data


@restaurant
def parse_food_co(res_data: dict) -> dict:
    """
    Parse the menu of Food & Co
    """
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])

    hit = soup.find("div", {"class": "day-current"}).parent

    data["menu"] = [
        dish.find("span").text for dish in hit.find_all("section", {"class": "day-alternative"})
    ]

    return data


@restaurant
def parse_kmarkt(res_data: dict) -> dict:
    """
    Parse the menu of K-märkt. No menu available online.
    """
    return {"menu": []}


# Radiohuset
@restaurant
def parse_wkb_gardet(res_data: dict) -> dict:
    """Parse the menu of WKB Gärdet."""
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])
    section = soup.find("div", {"class": "post-content"})
    days = section.find(text=re.compile(get_weekday(), re.IGNORECASE)).parent.parent
    active = False
    for row in days:
        if row.name == "strong" and get_weekday() in row.text.lower():
            active = True
            continue
        if active:
            if row.name == "strong":
                break
            if row.text:
                data["menu"].append(row.text)

    return data


@restaurant
def parse_gourmedia(res_data: dict) -> dict:
    """Parse the menu of Gourmedia."""
    data = {"menu": []}
#    soup = get_parser(res_data["menuUrl"])
#    days = soup.find("fluid-columns-repeater")
#    for day in days.children:
#        if get_weekday() in day.text:
#           pass
    return data


@restaurant
def parse_karavan(res_data: dict) -> dict:
    """Parse the menu of Restaurang Karavan."""
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])
    section = soup.find_all("div", {"class": "menu-content"})
    week = None
    for part in section:
        if str(get_week()) in part.find("div", {"class": "menu-heading"}).text:
            week = part
            break
    if week:
        day = week.find("div", {"class": get_weekday(lang="en")})
        data["menu"] = [dish.text.strip() for dish in day.find_all("p")]

    return data
