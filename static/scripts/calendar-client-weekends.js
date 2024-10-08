let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();

let nowDay = new Date().getDate();
let nowMonth = new Date().getMonth();
let nowYear = new Date().getFullYear();

let updateTimeout;

document.addEventListener("DOMContentLoaded", function() {
    updateCalendar();
});

function updateCalendar() {
    clearTimeout(updateTimeout);

    updateTimeout = setTimeout(() => {
        const monthYear = document.getElementById("monthYear");
        const calendarDays = document.getElementById("calendarDays");

        const firstDay = new Date(currentYear, currentMonth, 1).getDay();
        const lastDate = new Date(currentYear, currentMonth + 1, 0).getDate();
        const monthNames = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"];
        monthYear.innerText = `${monthNames[currentMonth]} ${currentYear}`;
        calendarDays.innerHTML = "";
        let date = 1;

        // Загружаем данные о событиях с API
        fetch('https://roads-of-russia-andrey2211.amvera.io/api/v1/weekends')
            .then(response => response.json())
            .then(weekends => {
                const url = window.location.href;
                const params = new URLSearchParams(url);
                const clientID = Number(params.get('client'));
                const filteredEvents = events.filter(event =>
                    event.clients.includes(clientID) && (
                        document.URL.includes('clients-events') ? event.event_type !== "Обучение" :
                        document.URL.includes('clients-learnings') ? event.event_type === "Обучение" : true
                    )
                );
                filteredEvents.forEach(event => {
                    const eventDateStart = new Date(event.date_start);
                    const eventDateEnd = new Date(event.date_end);
                    while (eventDateStart <= eventDateEnd) {
                        const dayStart = eventDateStart.getDate();
                        const monthStart = eventDateStart.getMonth();
                        const yearStart = eventDateStart.getFullYear();
                        if (monthStart === currentMonth && yearStart == currentYear) {
                            if (eventsByDate[dayStart]) {
                                eventsByDate[dayStart]++;
                                eventsArray[dayStart].push(event);
                            } else {
                                eventsByDate[dayStart] = 1;
                                eventsArray[dayStart] = [event];
                            }
                        }
                        eventDateStart.setDate(eventDateStart.getDate() + 1);
                    }
                });

                for (let i = 0; i < 6; i++) {
                    let row = document.createElement("tr");
                    for (let j = 0; j < 7; j++) {
                        if (i === 0 && j < (firstDay + 6) % 7) {
                            let cell = document.createElement("td");
                            cell.innerText = "";
                            row.appendChild(cell);
                        } else if (date > lastDate) {
                            break;
                        } else {
                            let cell = document.createElement("td");
                            cell.innerText = date;

                            cell.style.borderRadius = "50%";

                            if (eventsByDate[date] === 1) {
                                cell.style.backgroundColor = '#0d3b66';
                                cell.style.fontWeight = "bolder";
                            }
                            else if (eventsByDate[date] >= 2 && eventsByDate[date] <= 4) {
                                cell.style.backgroundColor = '#faf0ca';
                                cell.style.color = "black";
                                cell.style.fontWeight = "bolder";
                            }
                            else if (eventsByDate[date] > 4) {
                                cell.style.backgroundColor = '#f4d35e';
                                cell.style.color = "black";
                                cell.style.fontWeight = "bolder";
                            }

                            if (nowMonth === currentMonth && nowYear === currentYear && date === nowDay) {
                                cell.style.backgroundColor = '#86B32D';
                            }

                            cell.addEventListener('click', () => {
                                displayEventsForDay(cell.innerText, eventsArray);
                            });


                            row.appendChild(cell);
                            date++;
                        }
                    }
                    calendarDays.appendChild(row);
                }
            })
            .catch(error => {
                console.error("Ошибка при получении данных с API:", error);
            });
        }, 300);
}


function prevMonth() {
    currentMonth--;
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    updateCalendar();
}

function nextMonth() {
    currentMonth++;
    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    updateCalendar();
}