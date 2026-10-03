from datetime import date, timedelta
from ics import Calendar, Event
import arrow

def read_calendar(text):
    cal = Calendar(text)

    assert cal is not None

    return cal

def events_around_date(search_events: Calendar, start_range: int = 1, end_range: int = 1):
    search_events = search_events.events

    events = []

    today = arrow.utcnow()
    start_date = today.shift(days=-end_range)
    end_date = today.shift(days=start_range)

    for event in sorted(search_events):
        begin_time = event.begin.to("UTC")
        end_time = event.end.to("UTC")

        if begin_time.is_between(start_date, end_date) or end_time.is_between(start_date, end_date):
            # Get the Unix Epoch of date, convert to days
            # Subtract today in days from start and end in days to get the difference in days without worrying about mouths
            _today = today.timestamp() // 86400

            start = int((begin_time.timestamp() // 86400) - _today)
            end = int((end_time.timestamp() // 86400) - _today)

            days = []
            # Don't include anything outside the range of -3, 3 as it might mess up javascript looping
            for i in range(max(-3, start), min(3, end + 1)): # Want to include the end
                if i < 0:
                    element_id = f"today-{i}-event"
                elif i == 0:
                    element_id = f"today-{i}-event"
                else:
                    element_id = f"today+{i}-event"
                days.append(element_id)

            events.append({
                "Name": event.name,
                "Days": days
            })

    return events

def upcoming_events(search_events: Calendar, end_range: int = 1, max_events: int = 1):
    search_events = search_events.events

    html = ""

    today = arrow.utcnow()
    end_date = today.shift(days=end_range)

    event_count = 0
    for event in sorted(search_events):
        if event_count >= max_events: continue

        begin_time = event.begin.to("UTC")
        end_time = event.end.to("UTC")

        starting = begin_time.is_between(today, end_date)
        ending = end_time.is_between(today, end_date) and not starting
        if starting or ending:
            # Get the Unix Epoch of date, convert to days
            # Subtract today in days from start and end in days to get the difference in days without worrying about mouths
            _today = today.timestamp() // 86400

            start = int((begin_time.timestamp() // 86400) - _today)
            end = int((end_time.timestamp() // 86400) - _today)

            time_string = f"starts {begin_time.humanize()}" if starting else f"ends {end_time.humanize()}"

            html += f"""
            <div>
                <p class="flex justify-start whitespace-nowrap overflow-hidden">{event.name}</p>
                <p class="flex justify-end">{time_string}</p>
            </div>
            """

            event_count += 1

    return html

def create_day_data(date: date):
    return {
        "Day": date.strftime("%A"),
        "DayShort": date.strftime("%A")[0:3],
        "DayDate": date.day
    }

def get_week():
    today = date.today()
    return [
        create_day_data(today - timedelta(days=3)),
        create_day_data(today - timedelta(days=2)),
        create_day_data(today - timedelta(days=1)),
        create_day_data(today),
        create_day_data(today + timedelta(days=1)),
        create_day_data(today + timedelta(days=2)),
        create_day_data(today + timedelta(days=3)),
    ]

if __name__ == "__main__":
    from pprint import pprint as print

    print(get_week())