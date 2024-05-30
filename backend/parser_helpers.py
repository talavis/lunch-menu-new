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
Helper functions for the menu parsers.
"""

import datetime
from datetime import date
import sys

import requests
from bs4 import BeautifulSoup


def restaurant(func):
    """
    Decorator to use for restaurants.
    """

    def helper(res_data):
        map_url = (
            "https://www.openstreetmap.org/#map=19/"
            f"{res_data['coordinate'][0]}/{res_data['coordinate'][1]}"
        )
        data = {
            "title": res_data["name"],
            "location": res_data["region"],
            "url": res_data["homepage"],
            "map_url": map_url,
        }
        try:
            data.update(func(res_data))
        except Exception as err:
            sys.stderr.write(f"Error in {func.__name__}: {err}\n")
            data.update({"menu": []})
            pass
        return data

    helper.__name__ = func.__name__
    helper.__doc__ = func.__doc__

    return helper


def get_parser(url: str) -> BeautifulSoup:
    """
    Request page and create Beautifulsoup object
    """
    page_req = requests.get(url)
    if page_req.status_code != 200:
        raise IOError("Bad HTTP responce code")

    return BeautifulSoup(page_req.text, "html.parser")


def get_day():
    """
    Today as digit
    """
    return date.today().day


def get_monthdigit():
    """
    Month as digit
    """
    return date.today().month


def get_month():
    """
    Month name
    """
    months = {
        1: "januari",
        2: "februari",
        3: "mars",
        4: "april",
        5: "maj",
        6: "juni",
        7: "juli",
        8: "augusti",
        9: "september",
        10: "oktober",
        11: "november",
        12: "december",
    }

    return months[get_monthdigit()]


def get_week():
    """
    Week number
    """
    return date.today().isocalendar()[1]


def get_weekday(lang="sv", tomorrow=False):
    """
    Day name in swedish(sv) or english (en)
    """
    wdigit = get_weekdigit()
    if tomorrow:
        wdigit += 1
    if lang == "sv":
        weekdays = {
            0: "måndag",
            1: "tisdag",
            2: "onsdag",
            3: "torsdag",
            4: "fredag",
            5: "lördag",
            6: "söndag",
            7: "måndag",
        }
    if lang == "en":
        weekdays = {
            0: "monday",
            1: "tuesday",
            2: "wednesday",
            3: "thursday",
            4: "friday",
            5: "saturday",
            6: "sunday",
            7: "monday",
        }
    return weekdays[wdigit]


def get_weekdigit():
    """
    Get digit for week (monday = 0)
    """
    return date.today().weekday()


def get_year():
    """
    Year as number
    """
    return date.today().year
