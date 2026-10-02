from datetime import date, timedelta

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