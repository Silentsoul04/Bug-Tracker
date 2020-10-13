// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
var ctx = document.getElementById("myPieChartReport");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ["Projects", "Bugs", "Feature"],
    datasets: [{
      data: [total_projects, total_bugs,total_feature ],
      backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
    }],
  },
});

var ctx = document.getElementById("myPieChartReportProjectStatus");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ["Closed", "Open", "In development"],
    datasets: [{
      data: [total_project_close, total_project_open_ ,total_project_dev ],
      backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
    }],
  },
});

var ctx = document.getElementById("myPieChartReportBugsStatus");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ["Closed", "Open", "In development"],
    datasets: [{
      data: [total_bugs_close, total_bugs_open_,total_bugs_dev],
      backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
    }],
  },
});

var ctx = document.getElementById("myPieChartReportFeatureStatus");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels:["Closed", "Open", "In development"],
    datasets: [{
      data: [total_feature_close, total_feature_open_ ,total_feature_dev],
      backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
    }],
  },
});
