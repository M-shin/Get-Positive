from flask import Flask, jsonify, render_template, request
import modelAPI

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('landing.html')

@app.route('/app')
def app():
  return render_template('layout.html')

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
