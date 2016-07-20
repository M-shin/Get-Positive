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

function updateSearchResultArea(data) {
  populateReviewArea(data.stars);
  populateTopPlates(data.plates);
  populateSRA(data.reviews)
}

function refine() {
  var keyword = $('#inputField').val();
  $.get('/refine?keyword=' + keyword + '&id=' + getId(), function(data) {
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
  $('#sra1').html(reviews[0].review_text);
  $('#sra2').html(reviews[1].review_text);
  $('#sra3').html(reviews[2].review_text);
}

function populateTopPlates(plates) {
  $('#plate1').html(plates[0]);
  $('#plate2').html(plates[1]);
  $('#plate3').html(plates[2]);
}

$(document).ready(function() {
  data = readMetadata();
  populateReviewArea(data.stars);
  populateTopPlates(data.plates);
  populateSRA(reviews);
});
