from flask import Flask, jsonify, render_template, request
from modelAPI import *
import time
#from get_positive.get_positive import BeginScrape, ScrapeReviewCounts
from get_positive.get_positive.BeginScrape import scrapeReviews
from get_positive.get_positive.ScrapeReviewCounts import getReviewCount
NUM_REVIEWS = 5
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('landing.html')

@app.route('/main', methods=['GET'])
def appMain():
  url = request.args['url']

  # Perhaps a step here where we check if the data is already in Mongo

  # Begin by scraping the reviews
  rest_id = ScrapeReviewCounts.getReviewCount(url)
  BeginScrape.scrapeReviews(url)

  # Train model
  # train(rest_id)

  # Use model endpoints to access data
  score = get_score(rest_id)
  reviews = get_top_reviews(rest_id, NUM_REVIEWS)
  plates = get_top_plates(rest_id, NUM_REVIEWS)
  stars = get_review_distribution(rest_id)

  time.sleep(3)

  return render_template('app.html', score=score, reviews=reviews, plates=plates, stars=stars)

@app.route('/loading')
def loading():
  return render_template('loading.html')

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
