from functions import mongo
import math
from urllib2 import unquote
from urllib2 import quote

# GLOBAL VARIABLES
plates = []


# Returns a quality score for a given term (-1 if term doesn't exist)
def get_score(rest_id, keyword=None):
    if keyword:
        model = get_model(rest_id)
        return get_term_score(keyword, model)


def compute_likelihood(num_stars, review, model):
    # compute prior log probability
    prior_string = "P_" + num_stars + "_prior"
    prob = math.log(model[prior_string])

    # add the posterior log probabilities of the review's terms naively
    posterior_string = "P_" + num_stars + "_counts"
    total_count = model[posterior_string]['total_count']
    for term in model[posterior_string]:
        posterior_prob = math.log((term + 1) / (total_count + model['dictionary_size']))  # uses Laplace smoothing
        prob += posterior_prob

    return prob


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
    return reviews


def get_first(item):
    return item.first


def get_second(item):
    return item.second


def get_top_reviews(rest_id, max_count, keyword=None):
    model = get_model(rest_id)
    reviews = score_reviews(model)
    reviews.sort(key=get_second, reverse=True)
    reviews.sort(key=get_first, reverse=True)
    count = 0
    result = []
    while count < max_count and count < len(reviews):
        review = dict()
        review['review_text'] = reviews[count].third
        review['num_stars'] = reviews[count].first
        result.append(review)
        count += 1
    return result
    # return [{'creation_date': '1/1/2000', 'review_text': 'good chicken', 'num_stars': 5}]


def get_plates():
    plates.append('chicken')


def get_term_score(term, model):
    if term not in model['P_1_counts']:
        model['P_1_counts'][term] = 0
    if term not in model['P_1_5_counts']:
        model['P_1_5_counts'][term] = 0
    if term not in model['P_2_counts']:
        model['P_2_counts'][term] = 0
    if term not in model['P_2_5_counts']:
        model['P_2_5_counts'][term] = 0
    if term not in model['P_3_counts']:
        model['P_3_counts'][term] = 0
    if term not in model['P_3_5_counts']:
        model['P_3_5_counts'][term] = 0
    if term not in model['P_4_counts']:
        model['P_4_counts'][term] = 0
    if term not in model['P_4_5_counts']:
        model['P_4_5_counts'][term] = 0
    if term not in model['P_5_counts']:
        model['P_5_counts'][term] = 0

    total_count = model['P_1_counts'][term] + model['P_1_5_counts'][term] + model['P_2_counts'][term] + \
                  model['P_2_5_counts'][term] + model['P_3_counts'][term] + model['P_3_5_counts'][term] + \
                  model['P_4_counts'][term] + model['P_4_5_counts'][term] + model['P_5_counts'][term]
    score_sum = model['P_1_counts'][term] + 1.5 * model['P_1_5_counts'][term] + 2 * model['P_2_counts'][term] + 2.5 * \
                model['P_2_5_counts'][term] + 3 * model['P_3_counts'][term] + 3.5 * model['P_3_5_counts'][term] + 4 * \
                model['P_4_counts'][term] + 4.5 * model['P_4_5_counts'][term] + 5 * model['P_5_counts'][term]
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
        return {'1': len(model['1_0']), '2': len(model['2_0']), '3': len(model['3_0']), '4': len(model['4_0']),
                '5': len(model['5_0'])}


# Trains a multinomial event model for restaurants' reviews
def train_general_model():
    model = {}


# Returns total number of reviews for a restaurant
def get_num_reviews(retrieved_model):
    return len(retrieved_model["1_0"]) + len(retrieved_model["1_5"]) + len(retrieved_model["2_0"]) + \
           len(retrieved_model["2_5"]) + len(retrieved_model["3_0"]) + len(retrieved_model["3_5"]) + \
           len(retrieved_model["4_0"]) + len(retrieved_model["4_5"]) + len(retrieved_model["5_0"])


def clean_term(term):
    # print "dirty_term: ", term.encode('utf-8').strip()
    # # print unicode(term, 'utf8')
    # print "term: ", term.encode('utf-8').strip().replace(".", "").replace(",", "").replace("\"", "").replace("(", "").replace(")", ""). \
    #     replace("<br>", "").replace("$", "").lower()
    return term.encode('utf-8').strip().replace(".", "").replace(",", "").replace("\"", "").replace("(", "").replace(")", ""). \
        replace("<br>", "").replace("$", "").lower()


def train_model(retrieved_model):
    num_reviews = get_num_reviews(retrieved_model)

    # compute prior probabilities
    retrieved_model['P_1_0_prior'] = len(retrieved_model['1_0']) / num_reviews
    retrieved_model['P_1_5_prior'] = len(retrieved_model['1_5']) / num_reviews
    retrieved_model['P_2_0_prior'] = len(retrieved_model['2_0']) / num_reviews
    retrieved_model['P_2_5_prior'] = len(retrieved_model['2_5']) / num_reviews
    retrieved_model['P_3_0_prior'] = len(retrieved_model['3_0']) / num_reviews
    retrieved_model['P_3_5_prior'] = len(retrieved_model['3_5']) / num_reviews
    retrieved_model['P_4_0_prior'] = len(retrieved_model['4_0']) / num_reviews
    retrieved_model['P_4_5_prior'] = len(retrieved_model['4_5']) / num_reviews
    retrieved_model['P_5_0_prior'] = len(retrieved_model['5_0']) / num_reviews

    # compute posterior probabilities
    terms = set() # set of unique terms
    retrieved_model['P_1_counts']['total_count'] = 0
    for review in retrieved_model['1_0']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_1_counts'][term] = retrieved_model['P_1_counts'].get(term, 0) + 1
                retrieved_model['P_1_counts']['total_count'] += 1
    retrieved_model['P_1_5_counts']['total_count'] = 0
    for review in retrieved_model['1_5']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_1_5_counts'][term] = retrieved_model['P_1_5_counts'].get(term, 0) + 1
                retrieved_model['P_1_5_counts']['total_count'] += 1
    retrieved_model['P_2_counts']['total_count'] = 0
    for review in retrieved_model['2_0']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_2_counts'][term] = retrieved_model['P_2_counts'].get(term, 0) + 1
                retrieved_model['P_2_counts']['total_count'] += 1
    retrieved_model['P_2_5_counts']['total_count'] = 0
    for review in retrieved_model['2_5']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_2_5_counts'][term] = retrieved_model['P_2_5_counts'].get(term, 0) + 1
                retrieved_model['P_2_5_counts']['total_count'] += 1
    retrieved_model['P_3_counts']['total_count'] = 0
    for review in retrieved_model['3_0']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_3_counts'][term] = retrieved_model['P_3_counts'].get(term, 0) + 1
                retrieved_model['P_3_counts']['total_count'] += 1
    retrieved_model['P_3_5_counts']['total_count'] = 0
    for review in retrieved_model['3_5']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_3_5_counts'][term] = retrieved_model['P_3_5_counts'].get(term, 0) + 1
                retrieved_model['P_3_5_counts']['total_count'] += 1
    retrieved_model['P_4_counts']['total_count'] = 0
    for review in retrieved_model['4_0']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_4_counts'][term] = retrieved_model['P_4_counts'].get(term, 0) + 1
                retrieved_model['P_4_counts']['total_count'] += 1
    retrieved_model['P_4_5_counts']['total_count'] = 0
    for review in retrieved_model['4_5']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_4_5_counts'][term] = retrieved_model['P_4_5_counts'].get(term, 0) + 1
                retrieved_model['P_4_5_counts']['total_count'] += 1
    retrieved_model['P_5_counts']['total_count'] = 0
    for review in retrieved_model['5_0']:
        for term in review.split():
            term = clean_term(term)
            if term:
                terms.add(term)
                retrieved_model['P_5_counts'][term] = retrieved_model['P_5_counts'].get(term, 0) + 1
                retrieved_model['P_5_counts']['total_count'] += 1
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
        retrieved_model['P_1_counts'] = dict()
        retrieved_model['P_1_5_counts'] = dict()
        retrieved_model['P_2_counts'] = dict()
        retrieved_model['P_2_5_counts'] = dict()
        retrieved_model['P_3_counts'] = dict()
        retrieved_model['P_3_5_counts'] = dict()
        retrieved_model['P_4_counts'] = dict()
        retrieved_model['P_4_5_counts'] = dict()
        retrieved_model['P_5_counts'] = dict()

        # process reviews
        for review in data:
            rating = str(review['rating']).replace('.', '_')
            retrieved_model[rating].append(review['body'])

        # train model
        trained_model = train_model(retrieved_model)
        print "trained_model", trained_model
        mongo.save_restaurant_model(restaurant, trained_model)
        return trained_model
    else:
        return mongo.get_restaurant_model(restaurant)


def main():
    model = get_model("Fang")
    print "Model: ", model
    print "Score: ", get_score("Fang", "fish")
    print "review_distribution: ", get_review_distribution("fang")
    print "get_top_reviews: ", get_top_reviews("Fang", 3)

if __name__ == "__main__":
    main()
