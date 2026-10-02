function updateDay(day_id, json) {
    document.getElementById(`${day_id}-day`).innerText = json.Day;
    document.getElementById(`${day_id}-date`).innerText = json.DayDate;
}

function updateCalendar() {
    fetch("/api/week_data", {method: "GET"})
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
}

window.addEventListener("load", function() {
    setInterval(updateCalendar, 3600000);
    updateCalendar();
});