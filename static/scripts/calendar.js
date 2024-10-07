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
        fetch('https://roads-of-russia-api.vercel.app/api/v1/events') // Замените на реальный URL API
            .then(response => response.json())
            .then(events => {
                const eventsByDate = {};
                const eventsArray = {};
                events.forEach(event => {
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

function displayEventsForDay(day, eventsByDate) {
    const eventsList = document.getElementsByClassName('all-events');
    eventsList[0].innerHTML = "";

    if (eventsByDate[day]) {
        eventsByDate[day].forEach(event => {

            const eventItem = document.createElement('div');
            eventItem.className = 'one-event';
            eventItem.innerHTML = `
                <div class="event-top-part">
                    <div class="event-title">
                        <p>${event.title}</p>
                        <p style="margin-top: 12px;">${event.event_type}</p>
                    </div>
                    <div class="event-text">
                        <p>${event.description}</p>
                    </div>
                </div>
                <div class="event-bottom-part">
                    <div class="event-date">
                        <img src="${window.location.pathname}static/images/calendar.png">
                        <span>с ${event.date_start} до ${event.date_end}</span>
                    </div>
                    <div class="event-author">
                        <img src="${window.location.pathname}static/company_files/${event.photo}" class="user-img">
                        <span>${event.author}</span>
                    </div>
                </div>
            `;

            eventItem.addEventListener('click', () => {
                location.href = `/events/${event.id}`;
            });

            eventsList[0].appendChild(eventItem);
        });
    } else {
        const noEventsItem = document.createElement('li');
        noEventsItem.style.marginTop = "1em";
        noEventsItem.textContent = 'В этот день нет событий';
        eventsList[0].appendChild(noEventsItem);
    }
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