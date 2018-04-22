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


listIssues('https://api.github.com/repos/snowleopard/hadrian/issues?labels=easy', "hadrian-issues");
listIssues('https://api.github.com/repos/izgzhen/hadrians-wall/issues?labels=easy', "hadrians-wall-issues");

window.onload = function () {
  var data = JSON.parse(document.getElementById("durations-json").innerText)
    .map(function(log) {
      return {
        x: new Date(log.timestamp),
        y: log.duration
      };
    });

  data.sort(function (a, b) {
    if (a.x < b.x) {
      return -1;
    }
    if (a.x > b.x) {
      return 1;
    }
    return 0;
  });

  var ctx = document.getElementById("myChart").getContext('2d');
  var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
      label: "label",
      datasets: [
        { label: "ds",
          data: data,
          fill: false,
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
