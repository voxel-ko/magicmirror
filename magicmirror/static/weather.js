function getHour() {
    const date = new Date();
    return date.toLocaleTimeString([], {hour: '2-digit', hour12: false});
}


async function updateWeather() {
    // thank you https://stackoverflow.com/a/37664029

    const url = "https://api.open-meteo.com/v1/forecast?latitude=39.609958&longitude=-104.982118&hourly=temperature_2m&timezone=auto&forecast_days=1&timeformat=unixtime&wind_speed_unit=ms&temperature_unit=fahrenheit"

    fetch(url, {method: "GET"})
        .then(function(response) {return response.json()})
        .then(function(json) {
            console.log(json);
            const temperature = json.hourly.temperature_2m[getHour()];
            const temperature_unit = json.hourly_units.temperature_2m;

            document.getElementById("temperature_degrees").innerText = temperature;
            document.getElementById("temperature_unit").innerText = temperature_unit;
        })
}

window.addEventListener('load', function() {
    setInterval(updateWeather, 3600000); // Update every hour, only get 10000 API calls a day
    updateWeather();
})