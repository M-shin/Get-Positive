// Main javascript file for landing.html

$(document).keypress(function(e) {
  if (e.which == 13) {
    handleSubmit();
  }
});

function handleSubmit() {
  $('#spinnerArea').load('/spinner');

  var url = $('#inputField').val();
  window.location.href='/prefetch?url=' + url;
}
