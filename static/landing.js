// Main javascript file for landing.html

function handleSubmit() {
  $('#spinnerArea').load('/spinner');

  var url = $('#inputField').val();
  window.location.href='/prefetch?url=' + url
/*  $.get('/prefetch?url=' + url, function(data) {
    $('#loadingArea').load('/loading2?id=' + data.id);
  });*/
}
