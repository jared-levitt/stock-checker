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

    // Update the stock price on the page
    document.getElementById('stock-price').textContent = data.price;
    document.getElementById('change').textContent = data.change;
    document.getElementById('change-percent').textContent = data.changePercent;
    document.getElementById('high').textContent = data.high;
    document.getElementById('low').textContent = data.low;
});

socket.on('time_update', (data) => {
    // Update the last updated time on the page
    document.getElementById('last-updated').textContent = data.lastUpdated;
});
