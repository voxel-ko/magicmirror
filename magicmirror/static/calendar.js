function updateDay(day_id, json) {
    document.getElementById(`${day_id}-day`).innerText = json.Day;
    document.getElementById(`${day_id}-date`).innerText = json.DayDate;
}

function updateCalendar() {
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
                console.log(event);
                const event_name = event.Name;
                const event_days = event.Days;

                // The code below is so terrible, I know that if I ever change how many events there can be I'll have to improve this
                event_days.forEach(function(value, index, array) {
                    if (document.getElementById(`${value}-0`).innerText.trim() == "") {
                        document.getElementById(`${value}-0`).innerText = event_name;
                    } else  if (document.getElementById(`${value}-1`).innerText == "") {
                        document.getElementById(`${value}-1`).innerText = event_name;
                    } else if (document.getElementById(`${value}-2`).innerText == "") {
                        document.getElementById(`${value}-2`).innerText = event_name
                    }
                })
            }
        });
}

window.addEventListener("load", function() {
    setInterval(updateCalendar, 3600000);
    updateCalendar();
});