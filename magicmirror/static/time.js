// Thanks https://www.geeksforgeeks.org/html/how-to-inject-current-day-and-time-into-html/
function updateTime() {
    const date = new Date();

    const time = date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}).replace(/AM|PM/,''); // Removes the AM tag without turning it into 24 hours
    const amPm = date.getHours() >= 12 ? "PM" : "AM";
    const seconds = date.toLocaleTimeString([], {second: '2-digit'});

    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const day = date.toLocaleDateString(undefined, options);

    document.getElementById('day').innerText = day;
    document.getElementById('time').innerText = time;
    document.getElementById('seconds').innerText = seconds;
    document.getElementById('amPm').innerText = amPm;
}

window.addEventListener("load", function() {
    setInterval(updateTime, 1000);
    updateTime();
})
