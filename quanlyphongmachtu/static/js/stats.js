

function profit_month_stats(id, total_profit_day=[], profit_day=[], colors, borderColors){
    const labels = profit_day;
    const data = {
      labels: labels,
      datasets: [{
        label: 'Thống Kê Doanh Thu Theo Tháng',
        data: total_profit_day,
        backgroundColor: colors,
        borderColor: borderColors,
        borderWidth: 1
      }]
    };

    const config = {
      type: 'bar',
      data: data,
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      },
    };


    let ctx = document.getElementById(id).getContext("2d")
    new Chart(ctx, config)

}