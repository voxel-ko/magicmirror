# Installation

Clone the repo

```
$ pip install -r requirements.txt
$ flask --app magicmirror run
```

# Configuration

## Calendar Events
place a `.ics` file in the `magicmirror` directory in order to have events show up

## Config File
latitude/longitude:
- auto
- value

`auto` uses https://ip-api.com/ to get latitude and longitude through http for free

timezone:
- auto
- value

`auto` uses https://ip-api.com/ to get latitude and longitude through http for free

speed_unit:
- kmh
- ms

temperature_unit:
- celsius
- fahrenheit

