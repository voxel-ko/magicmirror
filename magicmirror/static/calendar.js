function updateCalendar() {
    fetch("/api/week_data", {method: "GET"})
        .then(function(response) {return response.json()})
        .then(function(json) {
            json[1].DayShort = undefined;
            console.log(json);

            document.getElementById("today-3-day").innerText = `${json[0].DayShort}`;
            document.getElementById("today-2-day").innerText = `${json[1].DayShort}`;
            document.getElementById("today-1-day").innerText = `${json[2].DayShort}`;
            document.getElementById("today-day").innerText = `${json[3].DayShort}`;
            document.getElementById("today+1-day").innerText = `${json[4].DayShort}`;
            document.getElementById("today+2-day").innerText = `${json[5].DayShort}`;
            document.getElementById("today+3-day").innerText = `${json[6].DayShort}`;
        });
}

window.addEventListener("load", function() {
    //setInterval(updateCalendar, 3600000);
    //updateCalendar();
});