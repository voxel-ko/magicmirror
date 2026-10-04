import json
import math
from datetime import date, timedelta
from zoneinfo import ZoneInfo

import arrow
from ics import Calendar

from . import config


def read_calendar(text: str):
    """
    Turns a string representation of a .ics file into a calendar object

    :param text: string representation of a .ics file
    :return: Calendar object from ics library
    """
    cal = Calendar(text)

    assert cal is not None

    return cal


def events_around_date(search_events: Calendar, start_range: int = 1, end_range: int = 1):
    """
    Returns a list of events and the days that those events appear on

    :param search_events: The calendar that events are being pulled from
    :param start_range: The first day that events can appear
    :param end_range: The last day that events can appear
    :return: List of dictionary containing the events name and the days that it should be placed on
    """
    search_events = search_events.events

    week = {}
    week_json = {}

    timezone = ZoneInfo(config.config.timezone)

    today = arrow.now(tz=timezone)
    start_date = today.shift(days=-end_range)
    end_date = today.shift(days=start_range)

    for event in sorted(search_events):
        begin_time = event.begin.to(tz=timezone)
        end_time = event.end.to(tz=timezone)

        if begin_time.is_between(start_date, end_date) or end_time.is_between(start_date, end_date):
            # Get the Unix Epoch of date, convert to days
            # Subtract today in days from start and end in days to get the difference in days without worrying about mouths
            _today = today.timestamp() // 86400

            start = int((begin_time.timestamp() // 86400) - _today)
            end = int((end_time.timestamp() // 86400) - _today)

            # Don't include anything outside the range of -3, 3 as it might mess up javascript looping
            for i in range(max(-3, start), min(3, end + 1)):  # Want to include the end
                sign = "+" if i > 0 else ""
                element_id = f"today{sign}{i}-events"
                week[element_id] = week.get(element_id, [])
                week[element_id].append(event.name)

    max_events_per_day = config.config.max_events_per_day
    for day, events in week.items():
        html = ""
        for i in range(min(max_events_per_day, len(events))):
            event = events[i]
            html += f"<p>{event}</p>\n"

        week_json[day] = html

    print(week_json)

    return week_json


def upcoming_events(search_events: Calendar, end_range: int = 1, max_events: int = 1):
    """
    Creates an HTML representation of events that are going to start/end in the future

    :param search_events: The calendar that events are being pulled from
    :param end_range: The max amount of days to search for events
    :param max_events: The max amount of events to return
    :return: HTML representation of returned events
    """
    search_events = search_events.events

    html = ""

    timezone = ZoneInfo(config.config.timezone)

    today = arrow.now(tz=timezone)
    end_date = today.shift(days=end_range)

    event_count = 0
    for event in sorted(search_events):
        if event_count >= max_events: continue

        begin_time = event.begin.to(tz=timezone)
        end_time = event.end.to(tz=timezone)

        starting = begin_time.is_between(today, end_date)
        ending = end_time.is_between(today, end_date) and not starting
        if starting or ending:
            time_string = f"starts {begin_time.humanize()}" if starting else f"ends {end_time.humanize()}"

            html += f"""
            <div>
                <p class="flex justify-start whitespace-nowrap overflow-hidden">{event.name}</p>
                <p class="flex justify-end">{time_string}</p>
            </div>
            """

            event_count += 1

    return html


def create_day_data(day: date):
    """
    :param day: A date object to format data about
    :return: Dict object of date data
    """
    return {
        "Day": day.strftime("%A"),
        "DayShort": day.strftime("%a"),
        "DayDate": day.day
    }


def get_week_data():
    """
    :return: JSON object of day data for today and the 3 nearest days
    """
    today = date.today()
    return json.dumps([create_day_data(today + timedelta(days=i)) for i in range(-3, 4)])
