from flask import Flask, jsonify, render_template, request
from modelAPI import *
from get_positive.get_positive.GetMenu import getMenuItems
import subprocess
import json

NUM_REVIEWS = 5
app = Flask(__name__)

@app.route('/')
def _index():
  return render_template('landing.html')

@app.route('/prefetch', methods=['GET'])
def _prefetch():
  url = request.args['url']
  subprocess.call(['python', 'get_positive/get_positive/ScrapeReviewCounts.py', '-u', url])

  rest_id = get_restaurant_name()
  return render_template('loading2.html', id=rest_id, url=url)

@app.route('/main', methods=['GET'])
def _appMain():
  url = request.args['url']
  rest_id = request.args['id']

  # Begin by scraping the reviews
  subprocess.call(['python', 'get_positive/get_positive/BeginScrape.py', '-u', url, '-n', rest_id])

  # Populate database with menu items
  response = getMenuItems()

  # Use model endpoints to access data
  score = get_score(rest_id)
  reviews = get_top_reviews(rest_id, NUM_REVIEWS)

  plates = get_top_plates(rest_id, NUM_REVIEWS)
  stars = get_review_distribution(rest_id)

  return render_template('app.html', score=score, reviews=reviews, plates=plates, stars=stars, id=rest_id, no_menu=response)

@app.route('/testmain')
def _testMain():
  # Use model endpoints to access data
  score = 5.0
  reviews = ['Wow you guys are good', 'Like, real good', 'JK you suck hahahaha'];
  plates = ['Fish Soup', 'Fish Bowl', 'Fishy'];
  stars = {'1': 5, '2': 2, '3': 10, '4': 16, '5': 40}

  return render_template('app.html', score=score, reviews=reviews, plates=plates, stars=stars, id='In-N-Out Burger')

@app.route('/loading1')
def _loading1():
  return render_template('loading1.html')

@app.route('/spinner')
def _spinner():
  return render_template('spinner.html')

@app.route('/loading2')
def _loading2():
  return render_template('loading2.html', id=request.args['id'])

@app.route('/refine', methods=['GET'])
def _refine():
  rest_id = request.args['id']
  keyword = request.args['keyword']
  data = {
    'score': get_score(rest_id, keyword),
    'reviews': get_reviews(rest_id, 3, keyword),
    'plates': get_plates(rest_id, 3, keyword),
    'stars': get_review_distribution(rest_id, keyword)
  }
  return jsonify(**data)
