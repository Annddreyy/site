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
                const weekendsByDate = {};
                const url = window.location.href;
                const params = new URLSearchParams(url);
                const clientID = Number(params.get('client'));
                const filteredWeekends = weekends.filter(weekend =>
                    weekend.client == clientID
                );
                filteredWeekends.forEach(weekend => {
                    const weekendDateStart = new Date(weekend.date_start);
                    const weekendDateEnd = new Date(weekend.date_end);
                    while (weekendDateStart <= weekendDateEnd) {
                        const dayStart = weekendDateStart.getDate();
                        const monthStart = weekendDateStart.getMonth();
                        const yearStart = weekendDateStart.getFullYear();
                        if (monthStart === currentMonth && yearStart == currentYear) {
                            if (weekendsByDate[dayStart]) {
                                weekendsByDate[dayStart]++;
                            } else {
                                weekendsByDate[dayStart] = 1;
                            }
                        }
                        weekendDateStart.setDate(weekendDateStart.getDate() + 1);
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

                            if (weekendsByDate[date] === 1) {
                                cell.style.backgroundColor = '#0d3b66';
                                cell.style.fontWeight = "bolder";
                            }
                            else if (weekendsByDate[date] >= 2 && weekendsByDate[date] <= 4) {
                                cell.style.backgroundColor = '#faf0ca';
                                cell.style.color = "black";
                                cell.style.fontWeight = "bolder";
                            }
                            else if (weekendsByDate[date] > 4) {
                                cell.style.backgroundColor = '#f4d35e';
                                cell.style.color = "black";
                                cell.style.fontWeight = "bolder";
                            }

                            if (nowMonth === currentMonth && nowYear === currentYear && date === nowDay) {
                                cell.style.backgroundColor = '#86B32D';
                            }

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