function compare_chart_data(a, b) {
    if (a.x < b.x) {
      return -1;
    }
    if (a.x > b.x) {
      return 1;
    }
    return 0;
}

function log_to_data(log) {
  return {
    x: new Date(log.timestamp),
    y: log.duration
  };
}

window.onload = function () {
  var logs = JSON.parse(document.getElementById("logs-json").innerText);
  var ok_defaults = [];
  var ok_quickest = [];
  var ok_quickest_cross = [];
  var ok_quick = [];
  var failed = [];

  logs.forEach(function (log) {
    if (log['exit-code'] == 0) {
      if (log.mode == 'default') {
        ok_defaults.push(log_to_data(log));
      } else if (log.clean == true) {
        if (log.flavour == 'quickest') {
          ok_quickest.push(log_to_data(log));
        } else if (log.flavour == 'quickest-cross') {
          ok_quickest_cross.push(log_to_data(log));
        } else if (log.flavour == 'quick') {
          ok_quick.push(log_to_data(log));
        } else {
          console.log("unknown flavour: " + log.flavour);
        }
      }
    } else { // log.exit_code != 0
      failed.push(log_to_data(log));
    }
  });

  ok_defaults.sort(compare_chart_data);
  ok_quickest.sort(compare_chart_data);
  ok_quickest_cross.sort(compare_chart_data);
  ok_quick.sort(compare_chart_data);
  failed.sort(compare_chart_data);

  console.log(ok_defaults);
  console.log(ok_quickest);
  console.log(failed);

  var ctx = document.getElementById("myChart").getContext('2d');
  var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
      label: "duration chart",
      datasets: [
        { label: "flavour=default exits 0",
          data: ok_defaults,
          fill: false,
          borderColor: '#00cc00',
          pointBackgroundColor: '#00cc00'
        },
        { label: "flavour=quickest exits 0",
          data: ok_quickest,
          fill: false,
          borderColor: '#0080ff',
          pointBackgroundColor: '#0080ff'
        },
        { label: "flavour=quickest-cross exits 0",
          data: ok_quickest_cross,
          fill: false,
          borderColor: '#74a2a2',
          pointBackgroundColor: '#74a2a2'
        },
        { label: "flavour=quick exits 0",
          data: ok_quick,
          fill: false,
          borderColor: '#cc33ff',
          pointBackgroundColor: '#cc33ff'
        },
        { label: "exits non-0",
          data: failed,
          fill: false,
          borderColor: '#ff0000',
          pointBackgroundColor: 'ff0000'
        }
       ]
    },
    options: {
      responsive: false,
       elements: {
            line: {
                tension: 0, // disables bezier curves
            }
        },
      scales: {
        xAxes: [{
          display: true,
          type: 'time',
        }],
        yAxes: [{
          display: true,
        }]
      } 
    }
  });
}
