

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

function medicine_month_stats(id, medicine_name, medicine_quantity, amount_medicine_per_test, colors2, borderColors2){
    const data = {
      labels: medicine_name,
      datasets: [{
        type: 'bar',
        label: 'Số Lượng Thuốc',
        data: medicine_quantity,
        borderColor: borderColors2,
        backgroundColor: colors2
      }, {
        type: 'line',
        label: 'Số Lần kê Đơn',
        data: amount_medicine_per_test,
        fill: false,
        borderColor: borderColors2
      }]
    };
    const config = {
      type: 'scatter',
      data: data,
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    };

    let ctx = document.getElementById(id).getContext("2d")
    new Chart(ctx, config)

}