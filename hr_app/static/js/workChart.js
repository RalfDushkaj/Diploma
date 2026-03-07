const workCtx = document.getElementById('workChart');

if (workCtx) {
  new Chart(workCtx, {
    type: 'pie',
    data: {
      labels: ['Onsite', 'Remote'],
      datasets: [{
        data: [onsiteCount, remoteCount],
        backgroundColor: ['#198754', '#0d6efd']
      }]
    }
  });
}