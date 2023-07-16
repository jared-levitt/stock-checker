// script.js
document.addEventListener('DOMContentLoaded', function() {
    var button = document.getElementById('submitButton');
    button.addEventListener('click', function() {
        var ticker = document.getElementById('ticker').value;
        window.location.href = '/stock-price/' + ticker;
    });
});
