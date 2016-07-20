// Main js file for app.html

function getId() {
  var id = $('#id').attr('content');
  return id;
}

function hasMenu() {
  var no_menu = $('#no_menu').attr('content');
  return !no_menu;
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
  if (score >= 0) {
    $('#ksa').html('<b>' + $('#inputField').val() + '</b> has a score of: <b>' + (0.0 + score).toFixed(2) + '</b>');
  } else {
    $('#ksa').html('Sorry, <b>' + $('#inputField').val() + '</b> doesn\'t have a score');
  }
}

function updateSearchResultArea(data) {
  if (hasMenu()){
    populateTopPlates(data.plates);
  }
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
        backgroundColor: ['#c00','#0c0','#00c','#cc0','#0cc']
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

function computePre(s, i) {
  var I = [s.lastIndexOf('.', i + 1), s.lastIndexOf('?', i + 1), s.lastIndexOf('!', i + 1)];
  I = I.filter(i => i > -1);
  if (I.length === 0) {
    return 0;
  }
  var max = I[0];
  for (var i = 1; i < I.length; i++) {
    max = Math.max(max, I[i]);
  }
  return max;
}

function computePost(s, i) {
  var I = [s.indexOf('.', i + 1), s.indexOf('?', i + 1), s.indexOf('!', i + 1)];
  I = I.filter(i => i > -1);
  if (I.length === 0) {
    return s.length;
  }
  var min = I[0];
  for (var i = 1; i < I.length; i++) {
    min = Math.min(min, I[i]);
  }
  return min;
}

function bold(s, i, l) {
  var nextSpace = s.indexOf(' ', i);
  return '"...' + s.slice(0, i) + '<b id="kmatch">' + s.slice(i, nextSpace) + '</b>' + s.slice(nextSpace) + '..."';
}

function populateSRA(reviews) {
  var keyword = $('#inputField').val().toLowerCase();
  console.log(keyword);
  if (keyword) {
    reviews.filter(review => review.review_text.toLowerCase().indexOf(keyword) != -1);
    for (var i = 0; i < reviews.length; i++) {
      reviews[i].review_text = reviews[i].review_text.split('<br>').join('');
      var index = reviews[i].review_text.toLowerCase().indexOf(keyword);
      console.log(index);
      var pre = computePre(reviews[i].review_text, index);
      var post = computePost(reviews[i].review_text, index);
      reviews[i].review_text = reviews[i].review_text.slice(pre + 1, post);
      var newIndex = reviews[i].review_text.toLowerCase().indexOf(keyword);
      reviews[i].review_text = bold(reviews[i].review_text, newIndex, keyword.length);
    }
  }
  for (var i = 0; i < 3; i++) {
    $('#sra' + (i + 1)).html('');
  }
  for (var i = 0; i < reviews.length; i++) {
    $('#sra' + (i + 1)).html('- ' + reviews[i].review_text.replace('<br>', ''));
  }
}

function populateTopPlates(plates) {
  for (var i = 0; i < plates.length; i++) {
    $('#plate' + (i + 1)).html('<b>' + plates[i]['plate'] + '</b> with score of: <b>' + (0.0 + plates[i]['score']).toFixed(2) + '</b>');
  }
}

function populateSubHeader(score) {
  $('#subHeaderText').html('Overall Score: <b>' + (0.0 + score).toFixed(2) + '</b>');
}

function renderTopPlateWarning() {
  $('#plate1').html('Sorry, but we can only suggest Top Plates for the customers of <a href="http://locu.com">Locu</a>');
}

$(document).keypress(function(e) {
  if (e.which == 13) {
    refine();
  }
});

$(document).ready(function() {
  data = readMetadata();
  console.log(JSON.stringify(data));
  populateReviewArea(data.stars);
  console.log('Has menu?: ' + hasMenu());
  if (data.plates.length > 0) {
    populateTopPlates(data.plates);
  } else {
    renderTopPlateWarning();
  }
  populateSRA(data.reviews);
  populateSubHeader(data.score);
});
