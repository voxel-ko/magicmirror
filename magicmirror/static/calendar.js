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

    fetch("/api/week_events", {method: "GET"})
        .then(function(response) {return response.json()})
        .then(function(json) {
            for (let i = 0; i < Math.min(json.length, 4); i++) {
                const event = json[i];
                const event_name = event.Name;
                const event_days = event.Days;

                event_days.forEach(function(value, index, array) {
                    // value = "today-{day}-event"

                    // `${value}-count` is a hidden <p> element
                    // that each day has that stores the amount of events that day currently has
                    const event_count = Number(document.getElementById(`${value}-count`).innerText);

                    if (event_count <= max_events_per_day) {
                        document.getElementById(`${value}s`).innerHTML += `<p>${event_name}</p>`;
                        document.getElementById(`${value}-count`).innerText = event_count + 1;
                    }
                })
            }
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