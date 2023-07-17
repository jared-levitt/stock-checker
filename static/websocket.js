const socket = io();

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
});

socket.on('stock_update', (data) => {
    // Handle the received stock update data
    console.log('Received stock update:', data);
    updateStockData(data);
});

function updateStockData(data) {
    const priceElement = document.getElementById('price');
    const changeElement = document.getElementById('change');
    const highElement = document.getElementById('high');
    const lowElement = document.getElementById('low');
    const arrowElement = document.getElementById('arrow');
    const lastUpdatedElement = document.getElementById('last-updated');

    priceElement.textContent = data.price;
    changeElement.textContent = `(${data.change}%)`;
    highElement.textContent = `High: ${data.high}`;
    lowElement.textContent = `Low: ${data.low}`;

    if (data.changePercent > 0) {
        arrowElement.innerHTML = '<span class="arrow-up-right">&#8599;&#xFE0E;</span>';
        arrowElement.style.color = '#90fd58';
    } else {
        arrowElement.innerHTML = '<span class="arrow-down-right">&#8600;&#xFE0E;</span>';
        arrowElement.style.color = '#ff6767';
    }

    const timestamp = new Date(data.timestamp);
    const formattedTimestamp = formatTimestamp(timestamp);
    lastUpdatedElement.textContent = `Last Updated: ${formattedTimestamp}`;
}

function formatTimestamp(timestamp) {
    const year = timestamp.getFullYear();
    const month = timestamp.getMonth() + 1;
    const day = timestamp.getDate();
    const hours = timestamp.getHours();
    const minutes = timestamp.getMinutes();

    const formattedDate = `${padZero(day)}/${padZero(month)}/${year}`;
    const formattedTime = `${padZero(hours)}:${padZero(minutes)}`;

    return `${formattedDate} ${formattedTime}`;
}

function padZero(number) {
    return number.toString().padStart(2, '0');
}
