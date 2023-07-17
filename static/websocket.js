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
});
