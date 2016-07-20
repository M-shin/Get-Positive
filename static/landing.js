// Main javascript file for landing.html

function handleSubmit() {
  $('#spinnerArea').load('/spinner');

  var url = $('#inputField').val();
  $.get('/prefetch?url=' + url, function(data) {
    $('#loadingArea').load('/loading2?id=' + data.id)
    window.location.href = '/main?url=' + data.url + '&id=' + data.id;
    //    $.get('/main?url=' + data.url + '&id=' + data.id)
  });
}
