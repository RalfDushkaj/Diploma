const deptCtx = document.getElementById('deptChart');

if (deptCtx) {
  new Chart(deptCtx, {
    type: 'bar',
    data: {
      labels: deptLabels,
      datasets: [{
        label: 'Employees',
        data: deptCounts,
        backgroundColor: '#0d6efd'
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}