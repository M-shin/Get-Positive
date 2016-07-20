from __future__ import division
import csv
from functions import mongo
import math
# from urllib2 import unquote
# from urllib2 import quote

# GLOBAL VARIABLES
plates = []

def get_restaurant_name():
    with open('get_positive/get_positive/reviewCounts.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for row in reader:
            return row[1]

# Returns a quality score for a given term (-1 if term doesn't exist)
def get_score(rest_id, keyword=None):
    model = get_model(rest_id)
    if keyword:
        return get_term_score(keyword, model)
    else:
        return get_general_score(model)


def get_general_score(model):
    total_count = get_num_reviews(model)
    score_sum = len(model['1_0']) + 1.5*len(model['1_5']) + 2*len(model['2_0']) + 2.5*len(model['2_5']) + \
                3*len(model['3_0']) + 3.5*len(model['3_5']) + 4*len(model['4_0']) + 4.5*len(model['4_5']) + \
                5*len(model['5_0'])
    if total_count != 0:
        return score_sum / total_count
    else:
        return -1


def compute_likelihood(num_stars, review, model):
    # compute prior log probability
    update_prior_probabilities(model)
    prior_string = "P_" + num_stars + "_prior"
    # print "prior: ", model[prior_string]
    # print "prior_real: ", len(model['1_0']) / get_num_reviews(model)
    prob = math.log(model[prior_string])

    # add the posterior log probabilities of the review's terms naively
    posterior_string = "P_" + num_stars + "_counts"
    total_count = model[posterior_string]['total_count']
    for term in model[posterior_string]:
        # print "term: ", term
        posterior_prob = math.log((model[posterior_string][term] + 1) / (total_count + model['dictionary_size']))  # uses Laplace smoothing
        prob += posterior_prob

    return prob


def score_term_reviews(term, model):
    result = []
    initial_score = get_term_score(term, model)
    term_score = round(initial_score)
    if term_score == 0.0:
        term_score = 1.0
    reviews = mongo.search_by_keyword(term)
    for review in reviews:
        if review['rating'] == term_score:
            result.append((review['rating'],compute_likelihood(str(review['rating']).replace(".", "_"), \
                   review['body'], model), review['body']))

    if term_score - initial_score >= 0:
        result.sort(key=get_second)
        result.sort(key=get_first)
    else:
        result.sort(key=get_second, reverse=True)
        result.sort(key=get_first, reverse=True)

    return result


def score_reviews(model):
    reviews = []
    for review in model['1_0']:
        reviews.append((1.0, compute_likelihood('1_0', review, model), review))
    for review in model['1_5']:
        reviews.append((1.5, compute_likelihood('1_5', review, model), review))
    for review in model['2_0']:
        reviews.append((2.0, compute_likelihood('2_0', review, model), review))
    for review in model['2_5']:
        reviews.append((2.5, compute_likelihood('2_5', review, model), review))
    for review in model['3_0']:
        reviews.append((3.0, compute_likelihood('3_0', review, model), review))
    for review in model['3_5']:
        reviews.append((3.5, compute_likelihood('3_5', review, model), review))
    for review in model['4_0']:
        reviews.append((4.0, compute_likelihood('4_0', review, model), review))
    for review in model['4_5']:
        reviews.append((4.5, compute_likelihood('4_5', review, model), review))
    for review in model['5_0']:
        reviews.append((5.0, compute_likelihood('5_0', review, model), review))

    # sort reviews from best to worst
    reviews.sort(key=get_second, reverse=True)
    reviews.sort(key=get_first, reverse=True)

    return reviews


def get_first(item):
    return item[0]


def get_second(item):
    return item[1]


def get_top_reviews(rest_id, max_count, keyword=None):
    model = get_model(rest_id)
    # reviews = []
    if not keyword:
        reviews = score_reviews(model)
    else:
        reviews = score_term_reviews(keyword, model)

    count = 0
    result = []
    while count < max_count and count < len(reviews):
        review = dict()
        review['review_text'] = reviews[count][2]
        review['num_stars'] = reviews[count][0]
        result.append(review)
        count += 1
    return result


def get_plates():
    plates.append('chicken')


def get_term_score(term, model):
    if term not in model['P_1_0_counts']:
        model['P_1_0_counts'][term] = 0
    if term not in model['P_1_5_counts']:
        model['P_1_5_counts'][term] = 0
    if term not in model['P_2_0_counts']:
        model['P_2_0_counts'][term] = 0
    if term not in model['P_2_5_counts']:
        model['P_2_5_counts'][term] = 0
    if term not in model['P_3_0_counts']:
        model['P_3_0_counts'][term] = 0
    if term not in model['P_3_5_counts']:
        model['P_3_5_counts'][term] = 0
    if term not in model['P_4_0_counts']:
        model['P_4_0_counts'][term] = 0
    if term not in model['P_4_5_counts']:
        model['P_4_5_counts'][term] = 0
    if term not in model['P_5_0_counts']:
        model['P_5_0_counts'][term] = 0

    total_count = model['P_1_0_counts'][term] + model['P_1_5_counts'][term] + model['P_2_0_counts'][term] + \
                  model['P_2_5_counts'][term] + model['P_3_0_counts'][term] + model['P_3_5_counts'][term] + \
                  model['P_4_0_counts'][term] + model['P_4_5_counts'][term] + model['P_5_0_counts'][term]
    score_sum = model['P_1_0_counts'][term] + 1.5 * model['P_1_5_counts'][term] + 2 * model['P_2_0_counts'][term] + 2.5 * \
                model['P_2_5_counts'][term] + 3 * model['P_3_0_counts'][term] + 3.5 * model['P_3_5_counts'][term] + 4 * \
                model['P_4_0_counts'][term] + 4.5 * model['P_4_5_counts'][term] + 5 * model['P_5_0_counts'][term]
    if total_count != 0:
        return score_sum / total_count
    else:
        return -1


def get_top_plates(rest_id, max_count, keyword=None):
    result = []
    plates.sort(key=get_term_score, reverse=True)
    count = 0
    while count < max_count and count < len(plates):
        plate = dict()
        plate['plate'] = plates[count]
        plate['score'] = get_term_score(plates[count])
        result.append(plate)

    return result  # [{'plate': 'chicken', 'score': 4.9}]


def get_review_distribution(rest_id, keyword=None):
    model = get_model(rest_id)
    if not keyword:
        return {'1': len(model['1_0']), '1.5': len(model['1_5']), '2': len(model['2_0']), '2.5': len(model['2_5']), \
                '3': len(model['3_0']), '3.5': len(model['3_5']), '4': len(model['4_0']), '4.5': len(model['4_5']), \
                '5': len(model['5_0'])}


# Trains a multinomial event model for restaurants' reviews
def train_general_model():
    model = {}


# Returns total number of reviews for a restaurant
def get_num_reviews(retrieved_model):
    # print "retrieved_model['5_0']: ", retrieved_model["5_0"]
    return len(retrieved_model["1_0"]) + len(retrieved_model["1_5"]) + len(retrieved_model["2_0"]) + \
           len(retrieved_model["2_5"]) + len(retrieved_model["3_0"]) + len(retrieved_model["3_5"]) + \
           len(retrieved_model["4_0"]) + len(retrieved_model["4_5"]) + len(retrieved_model["5_0"])


def clean_term(term):
    # print "dirty_term: ", term.encode('utf-8').strip()
    # # print unicode(term, 'utf8')
    # print "term: ", term.encode('utf-8').strip().replace(".", "").replace(",", "").replace("\"", "").replace("(", "").replace(")", ""). \
    #     replace("<br>", "").replace("$", "").lower()
    return term.encode('utf-8').strip().replace(".", "").replace(",", "").replace("\"", "").replace("(", "").replace(")", ""). \
        replace("<br>", "").replace("$", "").replace("!", "").replace(":", "").replace("?", "").lower()


def update_prior_probabilities(retrieved_model):
    # print "model: ", retrieved_model
    num_reviews = get_num_reviews(retrieved_model)
    retrieved_model['P_1_0_prior'] = len(retrieved_model['1_0']) / num_reviews
    retrieved_model['P_1_5_prior'] = len(retrieved_model['1_5']) / num_reviews
    retrieved_model['P_2_0_prior'] = len(retrieved_model['2_0']) / num_reviews
    retrieved_model['P_2_5_prior'] = len(retrieved_model['2_5']) / num_reviews
    retrieved_model['P_3_0_prior'] = len(retrieved_model['3_0']) / num_reviews
    retrieved_model['P_3_5_prior'] = len(retrieved_model['3_5']) / num_reviews
    retrieved_model['P_4_0_prior'] = len(retrieved_model['4_0']) / num_reviews
    retrieved_model['P_4_5_prior'] = len(retrieved_model['4_5']) / num_reviews
    retrieved_model['P_5_0_prior'] = len(retrieved_model['5_0']) / num_reviews


def train_model(retrieved_model):
    # num_reviews = get_num_reviews(retrieved_model)
    #
    # # compute prior probabilities
    # retrieved_model['P_1_0_prior'] = len(retrieved_model['1_0']) / num_reviews
    # retrieved_model['P_1_5_prior'] = len(retrieved_model['1_5']) / num_reviews
    # retrieved_model['P_2_0_prior'] = len(retrieved_model['2_0']) / num_reviews
    # retrieved_model['P_2_5_prior'] = len(retrieved_model['2_5']) / num_reviews
    # retrieved_model['P_3_0_prior'] = len(retrieved_model['3_0']) / num_reviews
    # retrieved_model['P_3_5_prior'] = len(retrieved_model['3_5']) / num_reviews
    # retrieved_model['P_4_0_prior'] = len(retrieved_model['4_0']) / num_reviews
    # retrieved_model['P_4_5_prior'] = len(retrieved_model['4_5']) / num_reviews
    # retrieved_model['P_5_0_prior'] = len(retrieved_model['5_0']) / num_reviews

    update_prior_probabilities(retrieved_model)

    # compute posterior probabilities
    terms = set() # set of unique terms
    retrieved_model['P_1_0_counts']['total_count'] = 0
    for review in retrieved_model['1_0']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_1_0_counts'][term] = retrieved_model['P_1_0_counts'].get(term, 0) + 1
                retrieved_model['P_1_0_counts']['total_count'] += 1
    retrieved_model['P_1_5_counts']['total_count'] = 0
    for review in retrieved_model['1_5']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_1_5_counts'][term] = retrieved_model['P_1_5_counts'].get(term, 0) + 1
                retrieved_model['P_1_5_counts']['total_count'] += 1
    retrieved_model['P_2_0_counts']['total_count'] = 0
    for review in retrieved_model['2_0']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_2_0_counts'][term] = retrieved_model['P_2_0_counts'].get(term, 0) + 1
                retrieved_model['P_2_0_counts']['total_count'] += 1
    retrieved_model['P_2_5_counts']['total_count'] = 0
    for review in retrieved_model['2_5']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_2_5_counts'][term] = retrieved_model['P_2_5_counts'].get(term, 0) + 1
                retrieved_model['P_2_5_counts']['total_count'] += 1
    retrieved_model['P_3_0_counts']['total_count'] = 0
    for review in retrieved_model['3_0']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_3_0_counts'][term] = retrieved_model['P_3_0_counts'].get(term, 0) + 1
                retrieved_model['P_3_0_counts']['total_count'] += 1
    retrieved_model['P_3_5_counts']['total_count'] = 0
    for review in retrieved_model['3_5']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_3_5_counts'][term] = retrieved_model['P_3_5_counts'].get(term, 0) + 1
                retrieved_model['P_3_5_counts']['total_count'] += 1
    retrieved_model['P_4_0_counts']['total_count'] = 0
    for review in retrieved_model['4_0']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_4_0_counts'][term] = retrieved_model['P_4_0_counts'].get(term, 0) + 1
                retrieved_model['P_4_0_counts']['total_count'] += 1
    retrieved_model['P_4_5_counts']['total_count'] = 0
    for review in retrieved_model['4_5']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_4_5_counts'][term] = retrieved_model['P_4_5_counts'].get(term, 0) + 1
                retrieved_model['P_4_5_counts']['total_count'] += 1
    retrieved_model['P_5_0_counts']['total_count'] = 0
    for review in retrieved_model['5_0']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_5_0_counts'][term] = retrieved_model['P_5_0_counts'].get(term, 0) + 1
                retrieved_model['P_5_0_counts']['total_count'] += 1
    retrieved_model['dictionary_size'] = len(terms)
    return retrieved_model


# Returns a trained model
def get_model(restaurant):
    # retrieve model from DB
    data = mongo.search_by_restaurant(restaurant)
    retrieved_model = dict()

    # if a model doesn't exist, it trains one
    if not mongo.get_restaurant_model(restaurant):
        # initialize model
        retrieved_model['1_0'] = []
        retrieved_model['1_5'] = []
        retrieved_model['2_0'] = []
        retrieved_model['2_5'] = []
        retrieved_model['3_0'] = []
        retrieved_model['3_5'] = []
        retrieved_model['4_0'] = []
        retrieved_model['4_5'] = []
        retrieved_model['5_0'] = []
        retrieved_model['P_1_prior'] = 0.0
        retrieved_model['P_1_5_prior'] = 0.0
        retrieved_model['P_2_prior'] = 0.0
        retrieved_model['P_2_5_prior'] = 0.0
        retrieved_model['P_3_prior'] = 0.0
        retrieved_model['P_3_5_prior'] = 0.0
        retrieved_model['P_4_prior'] = 0.0
        retrieved_model['P_4_5_prior'] = 0.0
        retrieved_model['P_5_prior'] = 0.0
        retrieved_model['P_1_0_counts'] = dict()
        retrieved_model['P_1_5_counts'] = dict()
        retrieved_model['P_2_0_counts'] = dict()
        retrieved_model['P_2_5_counts'] = dict()
        retrieved_model['P_3_0_counts'] = dict()
        retrieved_model['P_3_5_counts'] = dict()
        retrieved_model['P_4_0_counts'] = dict()
        retrieved_model['P_4_5_counts'] = dict()
        retrieved_model['P_5_0_counts'] = dict()

        # process reviews
        for review in data:
            rating = str(review['rating']).replace('.', '_')
            retrieved_model[rating].append(review['body'])

        # train model
        trained_model = train_model(retrieved_model)
        # print "trained_model", trained_model
        mongo.save_restaurant_model(restaurant, trained_model)
        return trained_model
    else:
        return mongo.get_restaurant_model(restaurant)


# def main():
#     # model = get_model("Fang")
#     # print "Model: ", model
#     # print "Score: ", get_score("Fang", "fish")
#     # print "review_distribution: ", get_review_distribution("fang")
#     # print "General Score: ", get_score("Fang")
#     print "get_top_reviews: ", get_top_reviews("Fang", 3)
#     print "get_top_term_reviews: ", get_top_reviews("Fang", 3, "fish")
#
# if __name__ == "__main__":
#     main()
