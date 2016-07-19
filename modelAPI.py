model = dict()
model['1'] = dict()
model['2'] = dict()
model['3'] = dict()
model['4'] = dict()
model['5'] = dict()


def get_score(rest_id, keyword=None):
    return {'score': 0};


def get_top_reviews(rest_id, max_count, keyword=None):
    return {'creation_date': '1/1/2000', 'review_text': 'good chicken', 'num_stars': 5};


def get_top_plates(rest_id, max_count, keyword=None):
    return {'plate': 'chicken', 'score': 4.9}


def get_review_distribution(rest_id, keyword=None):
    return {'1': 3, '2': 13, '3': 27, '4': 293, '5': 36}


# Trains a multinomial event model for restaurants' reviews
def train_model():
    model = {}


# Retrieves model from DB
def get_model():
    model = {};
