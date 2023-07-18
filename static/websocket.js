const socket = io();

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
});

socket.on('stock_update', (data) => {
    console.log('Received stock update:', data);
    updateStockData(data);
});

function updateStockData(data) {
    const { price, change, changePercent, high, low, last_updated, ascii_price } = data;

    // Update stock price and change
    const asciiPriceElement = document.querySelector('.rainbow-text');
    const changeElement = document.querySelector('.change');
    const changePercentElement = document.querySelector('.changePercent');
    const highElement = document.querySelector('.high');
    const lowElement = document.querySelector('.low');
    const lastUpdatedElement = document.querySelector('#last-updated');
    

    changeElement.textContent = `Change: ${change}`;
    changePercentElement.innerHTML = `Change Percent: <span style="color: ${changePercent > 0 ? '#90fd58' : '#ff6767'};">${changePercent}%</span>`;
    highElement.innerHTML = `High: <span style="color: #90fd58; font-size: 24px;">&#11014;&#xFE0E</span> ${high}`;
    lowElement.innerHTML = `Low: <span style="color: #ff6767; font-size: 24px;">&#11015;&#xFE0E</span> ${low}`;
    lastUpdatedElement.textContent = `${last_updated}`;
    asciiPriceElement.textContent = ascii_price;
}
