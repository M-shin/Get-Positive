// Main js file for app.html

function readMetadata() {
  var id = $('#id').attr('content');
  var url = $('#url').attr('content');
  return {id: id, url: url};
}

$(document).ready(function() {
  data = readMetadata();
  window.location.href = '/main?url=' + data.url + '&id=' + data.id;
});
