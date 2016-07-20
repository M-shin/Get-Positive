import csv
from functions import mongo

# GLOBAL VARIABLES
plates = []

def get_restaurant_name():
    with open('get_positive/get_positive/reviewCounts.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for row in reader:
            return row[1]

# Returns a quality score for a given term (-1 if term doesn't exist)
def get_score(rest_id, keyword=None):
    if keyword:
        model = get_model(rest_id)
        return get_term_score(keyword, model)


def score_reviews(model):
    return 0


def get_top_reviews(rest_id, max_count, keyword=None):
    model = get_model(rest_id)
    reviews = []
    # for review in model[]

    return {'creation_date': '1/1/2000', 'review_text': 'good chicken', 'num_stars': 5}



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


def train_model(retrieved_model):
    num_reviews = get_num_reviews(retrieved_model)

    # compute prior probabilities
    retrieved_model['P_1_prior'] = len(retrieved_model['1_0']) / num_reviews
    retrieved_model['P_1_5_prior'] = len(retrieved_model['1_5']) / num_reviews
    retrieved_model['P_2_prior'] = len(retrieved_model['2_0']) / num_reviews
    retrieved_model['P_2_5_prior'] = len(retrieved_model['2_5']) / num_reviews
    retrieved_model['P_3_prior'] = len(retrieved_model['3_0']) / num_reviews
    retrieved_model['P_3_5_prior'] = len(retrieved_model['3_5']) / num_reviews
    retrieved_model['P_4_prior'] = len(retrieved_model['4_0']) / num_reviews
    retrieved_model['P_4_5_prior'] = len(retrieved_model['4_5']) / num_reviews
    retrieved_model['P_5_prior'] = len(retrieved_model['5_0']) / num_reviews

    # compute posterior probabilities
    retrieved_model['P_1_counts']['total_count'] = 0
    for review in retrieved_model['1_0']:
        for term in review.split():
            term = str(term).replace(".", "")
            retrieved_model['P_1_counts'][term] = retrieved_model['P_1_counts'].get(term, 0) + 1
            retrieved_model['P_1_counts']['total_count'] += 1
        retrieved_model['P_1_5_counts']['total_count'] = 0
    for review in retrieved_model['1_5']:
        for term in review.split():
            term = str(term).replace(".", "")
            retrieved_model['P_1_5_counts'][term] = retrieved_model['P_1_5_counts'].get(term, 0) + 1
            retrieved_model['P_1_5_counts']['total_count'] += 1
    retrieved_model['P_2_counts']['total_count'] = 0
    for review in retrieved_model['2_0']:
        for term in review.split():
            term = str(term).replace(".", "")
            retrieved_model['P_2_counts'][term] = retrieved_model['P_2_counts'].get(term, 0) + 1
            retrieved_model['P_2_counts']['total_count'] += 1
    retrieved_model['P_2_5_counts']['total_count'] = 0
    for review in retrieved_model['2_5']:
        for term in review.split():
            term = str(term).replace(".", "")
            retrieved_model['P_2_5_counts'][term] = retrieved_model['P_2_5_counts'].get(term, 0) + 1
            retrieved_model['P_2_5_counts']['total_count'] += 1
    retrieved_model['P_3_counts']['total_count'] = 0
    for review in retrieved_model['3_0']:
        for term in review.split():
            term = str(term).replace(".", "")
            retrieved_model['P_3_counts'][term] = retrieved_model['P_3_counts'].get(term, 0) + 1
            retrieved_model['P_3_counts']['total_count'] += 1
    retrieved_model['P_3_5_counts']['total_count'] = 0
    for review in retrieved_model['3_5']:
        for term in review.split():
            term = str(term).replace(".", "")
            retrieved_model['P_3_5_counts'][term] = retrieved_model['P_3_5_counts'].get(term, 0) + 1
            retrieved_model['P_3_5_counts']['total_count'] += 1
    retrieved_model['P_4_counts']['total_count'] = 0
    for review in retrieved_model['4_0']:
        for term in review.split():
            term = str(term).replace(".", "")
            retrieved_model['P_4_counts'][term] = retrieved_model['P_4_counts'].get(term, 0) + 1
            retrieved_model['P_4_counts']['total_count'] += 1
    retrieved_model['P_4_5_counts']['total_count'] = 0
    for review in retrieved_model['4_5']:
        for term in review.split():
            term = str(term).replace(".", "")
            retrieved_model['P_4_5_counts'][term] = retrieved_model['P_4_5_counts'].get(term, 0) + 1
            retrieved_model['P_4_5_counts']['total_count'] += 1
    retrieved_model['P_5_counts']['total_count'] = 0
    for review in retrieved_model['5_0']:
        for term in review.split():
            term = str(term).replace(".", "")
            retrieved_model['P_5_counts'][term] = retrieved_model['P_5_counts'].get(term, 0) + 1
            retrieved_model['P_5_counts']['total_count'] += 1
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


# def main():
#     model = get_model("Fang")
#     print "Model: ", model
#     print "Score: ", get_score("Fang", "guy")
#     print "review_distribution: ", get_review_distribution("fang")
#
# if __name__ == "__main__":
#     main()
