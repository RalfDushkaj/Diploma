const workCtx = document.getElementById('workChart');

if (workCtx) {
  new Chart(workCtx, {
    type: 'pie',
    data: {
      labels: ['Onsite', 'Remote', 'On Leave'],
      datasets: [{
        data: [onsiteCount, remoteCount, on_leaveCount],
        backgroundColor: ['#198754', '#0d6efd', '#ffc107']
      }]
    }
  });
}