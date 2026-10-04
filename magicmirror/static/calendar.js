function updateDay(day_id, json) {
    document.getElementById(`${day_id}-day`).innerText = json.Day;
    document.getElementById(`${day_id}-date`).innerText = json.DayDate;
}

function updateCalendar() {
    // TODO: have this take from the config somehow
    const max_events_per_day = 3;

    fetch("/api/week_days", {method: "GET"})
        .then(function(response) {return response.json()})
        .then(function(json) {
            updateDay("today-3", json[0]);
            updateDay("today-2", json[1]);
            updateDay("today-1", json[2]);
            updateDay("today", json[3]);
            updateDay("today+1", json[4]);
            updateDay("today+2", json[5]);
            updateDay("today+3", json[6]);
        });

    // The API returns a JSON dict of day element ids and HTML
    fetch("/api/week_events", {method: "GET"})
        .then(function(response) {return response.json()})
        .then(function(json) {
            Object.entries(json).forEach(function(k) {
                event_id = k[0];
                html = k[1];

                document.getElementById(event_id).innerHTML = html;
            });
        });

    // The API makes the html already
    fetch("/api/upcoming_events", {method: "GET"})
        .then(function(response) {return response.text()})
        .then(function(html) {
            document.getElementById("events-list").innerHTML = html;
        });
}

window.addEventListener("load", function() {
    setInterval(updateCalendar, 3600000);
    updateCalendar();
});