// Main js file for app.html

function replaceQuotes(data) {
    return data.split("'").join('"');
}

function getId() {
  var id = $('#id').attr('content');
  return id;
}

function readMetadata() {
  var score = JSON.parse(replaceQuotes($('#score').attr('content')));
  var reviews = JSON.parse(replaceQuotes($('#reviews').attr('content')));
  var plates = JSON.parse(replaceQuotes($('#plates').attr('content')));
  var stars = JSON.parse(replaceQuotes($('#stars').attr('content')));

  return {score: score, reviews: reviews, plates: plates, stars: stars};
}

function updateSearchResultArea(data) {
  console.log(data);
}

function refine() {
  var keyword = $('#inputField').val();
  console.log('Requesting...')
  $.get('/refine?keyword=' + keyword + '&id=' + getId(), function(data) {
    console.log('Done!')
    updateSearchResultArea(data);
  });
}

function populateReviewArea(stars) {
  console.log(stars);
  var total = 0;
  total += stars.1;
  total += stars.2;
  total += stars.3;
  total += stars.4;
  total += stars.5;
  var ctx = $('#myChart');
}

function populateTopPlates(plates) {
  console.log(plates);
}

$(document).ready(function() {
  data = readMetadata();
  populateReviewArea(data.stars);
  populateTopPlates(data.plates);
});
