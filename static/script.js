// script.js
function updateLastRefresh() {
  var now = new Date();
  var lastRefreshElement = document.getElementById('last-refresh');
  lastRefreshElement.textContent = 'Last Refresh: ' + now.toLocaleString();
}

updateLastRefresh();
