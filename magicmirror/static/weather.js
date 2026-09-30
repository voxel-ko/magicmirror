function getHour() {
    const date = new Date();
    return date.toLocaleTimeString([], {hour: '2-digit', hour12: false});
}

async function updateWeather() {
    // thank you https://stackoverflow.com/a/37664029

    fetch(`/api/weather_data`, {method: "GET"})
        .then(function(response) {return response.json()})
        .then(function(json) {
            console.log(json);
            const temperature = json.temperature;
            const temperature_unit = json.temperature_unit;
            const precipitation = json.precipitation;
            const humidity = json.relative_humidity_2m;
            const wind_speed = json.wind_speed_10m;

            document.getElementById("temperature_degrees").innerText = temperature;
            document.getElementById("temperature_unit").innerText = temperature_unit;
            document.getElementById("precipitation").innerText = precipitation;
            document.getElementById("humidity").innerText = humidity;
            document.getElementById("wind_speed").innerText = wind_speed;
        })
}

window.addEventListener('load', function() {
    setInterval(updateWeather, 900000); // Update every hour, only get 10000 API calls a day
    updateWeather();
})