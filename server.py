from flask import Flask, jsonify, render_template, request
from modelAPI import *
import subprocess
import time
#from get_positive.get_positive.BeginScrape import scrapeReviews
#from get_positive.get_positive.ScrapeReviewCounts import getReviewCount

NUM_REVIEWS = 5
app = Flask(__name__)

@app.route('/')
def _index():
  return render_template('landing.html')

@app.route('/prefetch', methods=['GET'])
def _prefetch():
  url = request.args['url']
  rest_id = getReviewCount(url)
#  return rest_id
  return jsonify(**{'id': 'FANG', 'url': url})

@app.route('/main', methods=['GET'])
def _appMain():
#  url = request.args['url']
#  rest_id = request.args['id']

  # Perhaps a step here where we check if the data is already in Mongo

  # Begin by scraping the reviews
#  scrapeReviews(url, rest_id)
  sup = subprocess.call(['python', 'get_positive/get_positive/BeginScrape.py', '-u', 'http://www.yelp.com/biz/fang-san-francisco-2', '-n', 'Fang'])
  # Use model endpoints to access data
#  score = get_score(rest_id)
#  reviews = get_top_reviews(rest_id, NUM_REVIEWS)
#  plates = get_top_plates(rest_id, NUM_REVIEWS)
#  stars = get_review_distribution(rest_id)

#  time.sleep(3)
  return 'Done!' + str(sup)
 # return render_template('app.html', score=score, reviews=reviews, plates=plates, stars=stars)

@app.route('/loading1')
def _loading1():
  return render_template('loading1.html')

@app.route('/loading2')
def _loading2():
  return render_template('loading2.html', id=request.args['id'])

@app.route('/score', methods=['GET'])
def _get_score():
  rest_id = request.args['id']
  keyword = None
  if request.args['keyword'] is not None:
    keyword = request.args['keyword']

  data = get_score(rest_id, keyword)
  return jsonify(**data)

@app.route('/reviews', methods=['GET'])
def _get_reviews():
  rest_id = request.args['id']
  keyword = None
  if request.args['keyword'] is not None:
    keyword = request.args['keyword']
  max_count = request.args['count']

  data = get_top_reviews(rest_id, max_count, keyword)
  return jsonify(**data)

@app.route('/plates', methods=['GET'])
def _get_plates():
  rest_id = request.args['id']
  keyword = None
  if request.args['keyword'] is not None:
    keyword = request.args['keyword']
  max_count = request.args['count']

  data = get_top_plates(rest_id, max_count, keyword)
  return jsonify(**data)

@app.route('/stars', methods=['GET'])
def _get_stars():
  rest_id = request.args['id']
  keyword = None
  if request.args['keyword'] is not None:
    keyword = request.args['keyword']

  data = get_review_distribution(rest_id, keyword)
  return jsonify(**data)
