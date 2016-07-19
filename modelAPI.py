from functions import mongo

# GLOBAL VARIABLES
model = dict()
model['1.0'] = []
model['1.5'] = []
model['2.0'] = []
model['2.5'] = []
model['3.0'] = []
model['3.5'] = []
model['4.0'] = []
model['4.5'] = []
model['5.0'] = []

plates = []

P_1_prior = 0.0
P_1_5_prior = 0.0
P_2_prior = 0.0
P_2_5_prior = 0.0
P_3_prior = 0.0
P_3_5_prior = 0.0
P_4_prior = 0.0
P_4_5_prior = 0.0
P_5_prior = 0.0

P_1_counts = dict()
P_1_5_counts = dict()
P_2_counts = dict()
P_2_5_counts = dict()
P_3_counts = dict()
P_3_5_counts = dict()
P_4_counts = dict()
P_4_5_counts = dict()
P_5_counts = dict()


# -------------------------------------------------------------


# Returns a quality score for a given term
def get_score(rest_id, keyword=None):
    if keyword:
        get_model(rest_id)
        return get_term_score(keyword)


def get_top_reviews(rest_id, max_count, keyword=None):
    return {'creation_date': '1/1/2000', 'review_text': 'good chicken', 'num_stars': 5};


def get_plates():
    plates.append('chicken')


def get_term_score(term):
    if term not in P_1_counts:
        P_1_counts[term] = 0
    if term not in P_1_5_counts:
        P_1_5_counts[term] = 0
    if term not in P_2_counts:
        P_2_counts[term] = 0
    if term not in P_2_5_counts:
        P_2_5_counts[term] = 0
    if term not in P_3_counts:
        P_3_counts[term] = 0
    if term not in P_3_5_counts:
        P_3_5_counts[term] = 0
    if term not in P_4_counts:
        P_4_counts[term] = 0
    if term not in P_4_5_counts:
        P_4_5_counts[term] = 0
    if term not in P_5_counts:
        P_5_counts[term] = 0
    total_count = P_1_counts[term] + P_1_5_counts[term] + P_2_counts[term] + P_2_5_counts[term] + P_3_counts[term] + \
                  P_3_5_counts[term] + P_4_counts[term] + P_4_5_counts[term] + P_5_counts[term]
    score_sum = P_1_counts[term] + 1.5*P_1_5_counts[term] + 2*P_2_counts[term] + 2.5*P_2_5_counts[term] + \
                3*P_3_counts[term] + 3.5*P_3_5_counts[term] + 4*P_4_counts[term] + 4.5*P_4_5_counts[term] + \
                5*P_5_counts[term]
    return score_sum / total_count


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
    return {'1': len(model['1']), '2': len(model['2']), '3': len(model['3']), '4': len(model['4']),
            '5': len(model['5'])}
    # {'1': 3, '2': 13, '3': 27, '4': 293, '5': 36}


# Trains a multinomial event model for restaurants' reviews
def train_general_model():
    model = {}


# Returns total number of reviews for a restaurant
def get_num_reviews():
    num_reviews = 0
    for num_stars in model:
        num_reviews += len(model[num_stars])
    return num_reviews


def train_model():
    num_reviews = get_num_reviews()

    # compute prior probabilities
    P_1_prior = len(model['1.0']) / num_reviews
    P_1_5_prior = len(model['1.5']) / num_reviews
    P_2_prior = len(model['2.0']) / num_reviews
    P_2_5_prior = len(model['2.5']) / num_reviews
    P_3_prior = len(model['3.0']) / num_reviews
    P_3_5_prior = len(model['3.5']) / num_reviews
    P_4_prior = len(model['4.0']) / num_reviews
    P_4_5_prior = len(model['4.5']) / num_reviews
    P_5_prior = len(model['5.0']) / num_reviews

    # compute posterior probabilities
    P_1_counts['total_count'] = 0
    for review in model['1.0']:
        for term in review.split():
            P_1_counts[term] = P_1_counts.get(term, 0) + 1
            P_1_counts['total_count'] += 1
    P_1_5_counts['total_count'] = 0
    for review in model['1.5']:
        for term in review.split():
            P_1_5_counts[term] = P_1_5_counts.get(term, 0) + 1
            P_1_5_counts['total_count'] += 1
    P_2_counts['total_count'] = 0
    for review in model['2.0']:
        for term in review.split():
            P_2_counts[term] = P_2_counts.get(term, 0) + 1
            P_2_counts['total_count'] += 1
    P_2_5_counts['total_count'] = 0
    for review in model['2.5']:
        for term in review.split():
            P_2_5_counts[term] = P_2_5_counts.get(term, 0) + 1
            P_2_5_counts['total_count'] += 1
    P_3_counts['total_count'] = 0
    for review in model['3.0']:
        for term in review.split():
            P_3_counts[term] = P_3_counts.get(term, 0) + 1
            P_3_counts['total_count'] += 1
    P_3_5_counts['total_count'] = 0
    for review in model['3.5']:
        for term in review.split():
            P_3_5_counts[term] = P_3_5_counts.get(term, 0) + 1
            P_3_5_counts['total_count'] += 1
    P_4_counts['total_count'] = 0
    for review in model['4.0']:
        for term in review.split():
            P_4_counts[term] = P_4_counts.get(term, 0) + 1
            P_4_counts['total_count'] += 1
    P_4_5_counts['total_count'] = 0
    for review in model['4.5']:
        for term in review.split():
            P_4_5_counts[term] = P_4_5_counts.get(term, 0) + 1
            P_4_5_counts['total_count'] += 1
    P_5_counts['total_count'] = 0
    for review in model['5.0']:
        for term in review.split():
            P_5_counts[term] = P_5_counts.get(term, 0) + 1
            P_5_counts['total_count'] += 1


# Returns a trained model
def get_model(restaurant):
    # retrieve model from DB
    data = mongo.search_by_restaurant(restaurant)
    for review in data:
        model[review['rating']].append(review['body'])

    # train model
    train_model()

# def main():
#     get_model("Fang")
#     print "Model: ", model
#     train_model()
#     print 'Score: ', get_term_score('amazing')
#
#
# if __name__ == "__main__":
#     main()
