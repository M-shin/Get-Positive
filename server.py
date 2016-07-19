from flask import Flask, jsonify, render_template, request
import modelAPI
import time

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
  rest_id = scrape(url)

  # Train model
  # train(rest_id)

  # Use model endpoints to access data
  score = modelAPI.get_score(rest_id)
  reviews = modelAPI.get_top_reviews(rest_id, NUM_REVIEWS)
  plates = modelAPI.get_top_plates(rest_id, NUM_REVIEWS)
  stars = modelAPI.get_review_distribution(rest_id)

  return render_template('app.html', score=score, reviews=reviews, plates=plates, stars=stars)

def scrape(url):
  # This is where we would make the scraper scrape stuff
  pass

@app.route('/score', methods=['GET'])
def get_score():
  rest_id = request.args['id']
  keyword = None
  if request.args['keyword'] is not None:
    keyword = request.args['keyword']

  data = modelAPI.get_score(rest_id, keyword)
  return jsonify(**data)

@app.route('/reviews', methods=['GET'])
def get_reviews():
  rest_id = request.args['id']
  keyword = None
  if request.args['keyword'] is not None:
    keyword = request.args['keyword']
  max_count = request.args['count']

  data = modelAPI.get_top_reviews(rest_id, max_count, keyword)
  return jsonify(**data)

@app.route('/plates', methods=['GET'])
def get_plates():
  rest_id = request.args['id']
  keyword = None
  if request.args['keyword'] is not None:
    keyword = request.args['keyword']
  max_count = request.args['count']

  data = modelAPI.get_top_plates(rest_id, max_count, keyword)
  return jsonify(**data)

@app.route('/stars', methods=['GET'])
def get_stars():
  rest_id = request.args['id']
  keyword = None
  if request.args['keyword'] is not None:
    keyword = request.args['keyword']

  data = modelAPI.get_review_distribution(rest_id, keyword)
  return jsonify(**data)
