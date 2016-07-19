// Main js file for app.html

function readMetadata() {

  function replaceQuotes(data) {
    return data.split("'").join('"');
  }

  var score = JSON.parse(replaceQuotes($('#score').attr('content')));
  var reviews = JSON.parse(replaceQuotes($('#reviews').attr('content')));
  var plates = JSON.parse(replaceQuotes($('#plates').attr('content')));
  var stars = JSON.parse(replaceQuotes($('#stars').attr('content')));

  return {score: score, reviews: reviews, plates: plates, stars: stars};
}

$(document).ready(function() {
  data = readMetadata();
  $('#displayScore').html(JSON.stringify(data.score));
  $('#displayReviews').html(JSON.stringify(data.reviews));
  $('#displayPlates').html(JSON.stringify(data.plates));
  $('#displayStars').html(JSON.stringify(data.stars));
});
