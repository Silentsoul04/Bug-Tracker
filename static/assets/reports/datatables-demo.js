// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable();
});

$(document).ready(function() {
  $('#dataTableProject').DataTable({
    "order": [ 2, 'desc' ],
    dom: 'Bfrtip',
    buttons: [
        'csv', 'excel', 'pdf', 'print'
    ]
  });
});

$(document).ready(function() {
  $('#dataTableBugs').DataTable({
    "order": [ 3, 'desc' ],
    dom: 'Bfrtip',
    buttons: [
        'csv', 'excel', 'pdf', 'print'
    ]
  });
});

$(document).ready(function() {
  $('#dataTableFeatures').DataTable({
    "order": [ 3, 'desc' ],
    dom: 'Bfrtip',
    buttons: [
        'csv', 'excel', 'pdf', 'print'
    ]
  });
});

$(document).ready(function() {
  $('#dataTableUser').DataTable({
    "order": [ 5, 'desc' ],
    dom: 'Bfrtip',
    buttons: [
        'csv', 'excel', 'pdf', 'print'
    ]
  });
});

$(document).ready(function() {
  $('#dataTableTotal').DataTable({
    "order": [ 5, 'desc' ]
  });
});

$(document).ready(function() {
  $('#dataTableOpen').DataTable({
    "order": [ 0, 'desc' ],
    dom: 'Bfrtip',
    buttons: [
        'csv', 'excel', 'pdf', 'print'
    ]
  });
});


$(document).ready(function() {
  $('#dataTableClosed').DataTable({
    "order": [ 0, 'desc' ],
    dom: 'Bfrtip',
    buttons: [
        'csv', 'excel', 'pdf', 'print'
    ]
  });
});

$(document).ready(function() {
  $('#dataTableExpired').DataTable({
    "order": [ 0, 'desc' ],
    dom: 'Bfrtip',
    buttons: [
        'csv', 'excel', 'pdf', 'print'
    ]
  });
});
$(document).ready(function() {
  $('#dataTableTopBugs').DataTable({
    "order": [ 2, 'desc' ],
    dom: 'Bfrtip',
    buttons: [
        'csv', 'excel', 'pdf', 'print'
    ]
  });
});

$(document).ready(function() {
  $('#dataTableTopFeature').DataTable({
    "order": [ 2, 'desc' ],
    dom: 'Bfrtip',
    buttons: [
        'csv', 'excel', 'pdf', 'print'
    ]
  });
});

$(document).ready(function() {
  $('#dataTableTopProjects').DataTable({
    "order": [ 2, 'desc' ],
    dom: 'Bfrtip',
    buttons: [
        'csv', 'excel', 'pdf', 'print'
    ]
  });
});

$(document).ready(function() {
  $('#dataTableTopProjectBugs').DataTable({
    "order": [ 1, 'desc' ],
    dom: 'Bfrtip',
    buttons: [
        'csv', 'excel', 'pdf', 'print'
    ]
  });
});












