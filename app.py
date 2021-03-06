import time
import json
import pandas as pd
from twitter import Api as tApi
from flask import Flask, request
from flask_restplus import Resource, Api, fields
from flask_cors import CORS
from config import config as c
from words import getWord

app = Flask(__name__)
CORS(app,
     expose_headers=['X-Total-Count',
                     'X-Metrics',
                     'Content-Range']
)
api = Api(app)

twitter = tApi(consumer_key=c['apikey'],
               consumer_secret=c['apisec'],
               access_token_key=c['acctok'],
               access_token_secret=c['accsec'])

search_model = api.model('Tweety', {
    'id': fields.Integer(),
    'lang': fields.String(),
    'text': fields.String(),
    'created_at': fields.String(),
    'location': fields.String(),
    'user': fields.String()
    })

def parse_args(arg, default):
    try:
        return request.args.to_dict()[arg]
    except KeyError:
        return default





@api.route('/search')
class search(Resource):
    @api.marshal_with(search_model)
    def marshled_search(self):
        count = parse_args('count', 10)
        term = parse_args('term', getWord())
        tweets = twitter.GetSearch(term=term, count=count)
        for tweet in tweets:
            tweet.user = tweet.user.name
            tweet.created_at = time.strftime(
                '%Y-%m-%d %H:%M',
                time.strptime(
                    tweet.created_at,'%a %b %d %H:%M:%S +0000 %Y'
                )
            )
        return tweets
        
    def get(self):
        tweets = self.marshled_search()
        df = pd.read_json(json.dumps(tweets))
        tpd = df["created_at"].value_counts() #Tweets per date
        tpl = df["lang"].value_counts() #Tweets per Language
        tpd = tpd.to_json()
        tpl = tpl.to_json()

        return tweets, {
            'X-Total-Count': len(tweets),
            'X-Metrics': {
                'tpd': tpd,
                'tpl': tpl
            }
            }



if __name__ == '__main__':
        app.run(debug=True)
