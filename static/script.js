// Get the current date and time
var currentDate = new Date();

// Format the date as yyyy/mm/dd
var formattedDate = currentDate.getFullYear() + '/' + (currentDate.getMonth() + 1) + '/' + currentDate.getDate();

// Format the time as military time in hours and minutes
var formattedTime = currentDate.getHours().toString().padStart(2, '0') + ':' + currentDate.getMinutes().toString().padStart(2, '0');

// Display the formatted date and time
document.getElementById('last-updated').textContent = formattedDate + ' ' + formattedTime;
