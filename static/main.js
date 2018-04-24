function createAnchor(url, text) {
  var a = document.createElement('a');
  a.appendChild(document.createTextNode(text));
  a.href = url;
  return a;
}

function listIssues(url, elementId) {
  var req = new XMLHttpRequest();
  req.onload = function(e) {
    var issues = JSON.parse(this.responseText);
    issues.forEach(function(issue) {
      var a = createAnchor(issues.html_url, "#" + issue.number + " " + issue.title);
      var node = document.createElement("li");
      node.appendChild(a);
      document.getElementById(elementId).appendChild(node);
    });
  };
  req.open('GET', url);
  req.send();
}


// listIssues('https://api.github.com/repos/snowleopard/hadrian/issues?labels=easy', "hadrian-issues");
// listIssues('https://api.github.com/repos/izgzhen/hadrians-wall/issues?labels=easy', "hadrians-wall-issues");

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
  var failed = [];

  logs.forEach(function (log) {
    console.log(log);
    if (log['exit-code'] == 0) {
      if (log.mode == 'default') {
        ok_defaults.push(log_to_data(log));
      } else if (log.flavour == 'quickest' && log.clean == true) {
        ok_quickest.push(log_to_data(log));
      }
    } else { // log.exit_code != 0
      failed.push(log_to_data(log));
    }
  });

  ok_defaults.sort(compare_chart_data);
  ok_quickest.sort(compare_chart_data);
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
          borderColor: '#00cc00'
        },
        { label: "flavour=quickest exits 0",
          data: ok_quickest,
          fill: false,
          borderColor: '#0080ff'
        },
        { label: "exits non-0",
          data: failed,
          fill: false,
          borderColor: '#ff0000'
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
