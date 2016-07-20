// Main js file for app.html

function getId() {
  var id = $('#id').attr('content');
  return id;
}

function readMetadata() {
  var score = JSON.parse($('#score').attr('content'));
  var reviewString = $('#reviews').attr('content');
  console.log(reviewString);
  var reviews = JSON.parse(reviewString);
  var plates = JSON.parse($('#plates').attr('content'));
  var stars = JSON.parse($('#stars').attr('content'));

  return {score: score, reviews: reviews, plates: plates, stars: stars};
}

function updateKSA(score) {
  $('#ksa').html('<b>' + $('#inputField').val() + '</b> has a score of: <b>' + score + '</b>');
}

function updateSearchResultArea(data) {
  populateTopPlates(data.plates);
  populateSRA(data.reviews);
  updateKSA(data.score);
}

function refine() {
  var keyword = $('#inputField').val();
  $.get('/refine?keyword=' + keyword + '&id=' + getId(), function(data) {
    console.log(JSON.stringify(data));
    updateSearchResultArea(data);
  });
}

function populateReviewArea(stars) {
  var total = 0;
  total += stars['1'];
  total += stars['2'];
  total += stars['3'];
  total += stars['4'];
  total += stars['5'];
  var ctx = $('#myChart');
  var data = {
    labels: ['1', '2', '3', '4', '5'],
    datasets: [
      {
        data: [stars['1'], stars['2'], stars['3'], stars['4'], stars['5']],
        backgroundColor: ['#f00','#0f0','#00f','#ff0','#0ff']
      }
    ]
  };
  var options = {};
  var doughnut = new Chart(ctx, {
    type: 'doughnut',
    data: data,
    options: options
  });
}

function populateSRA(reviews) {
  console.log('R: ' + reviews);
  $('#sra1').html(reviews[0].review_text);
  $('#sra2').html(reviews[1].review_text);
  $('#sra3').html(reviews[2].review_text);
}

function populateTopPlates(plates) {
  for (var i = 0; i < 3; i++) {
    $('#plate' + (i + 1)).html('<b>' + plates[i]['plate'] + '</b> with score of: <b>' + plates[i]['score'] + '</b>');
  }
}

function populateSubHeader(score) {
  $('#subHeaderText').html('Overall Score: <b>' + score + '</b>');
}

$(document).ready(function() {
  data = readMetadata();
  console.log(JSON.stringify(data));
  populateReviewArea(data.stars);
  populateTopPlates(data.plates);
  populateSRA(data.reviews);
  populateSubHeader(data.score);
});
