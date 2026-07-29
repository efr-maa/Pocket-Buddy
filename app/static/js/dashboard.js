// Refreshes the dashboard's stat tiles and category breakdown via the JSON
// API instead of a full page reload. Currently wired to re-fetch the same
// month on load as a demonstration of the REST layer; extend the `year`/
// `month` query params here if you add month-switching controls later.
(function () {
  const grid = document.getElementById("stat-grid");
  if (!grid) return;

  const year = grid.dataset.year;
  const month = grid.dataset.month;

  fetch(`/api/summary?year=${year}&month=${month}`)
    .then((res) => {
      if (!res.ok) throw new Error(`API returned ${res.status}`);
      return res.json();
    })
    .then((data) => {
      document.getElementById("stat-total").textContent = `$${data.total_spent.toFixed(2)}`;
      document.getElementById("stat-budget").textContent = `$${data.budget.toFixed(2)}`;
      document.getElementById("stat-remaining").textContent = `$${data.remaining_budget.toFixed(2)}`;
      document.getElementById("stat-daily").textContent = `$${data.daily_budget.toFixed(2)}`;
    })
    .catch((err) => console.error("Failed to refresh dashboard summary:", err));
})();
