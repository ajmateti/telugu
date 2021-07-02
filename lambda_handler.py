import json
from random import randint
import re
import base64
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("TeluguMovies")

def get_movie():
    rand_year = randint(2000, 2021)
    resp = table.scan(FilterExpression = Attr('year').eq(rand_year) & Attr('popularity').lte(2000))['Items']

    N = len(resp)

    rand_index = randint(1, N)-1
    
    movie_obj = resp[rand_index]
    title, year, director, actors = None, None, None, []
    year = int(movie_obj['year'])
    movie =re.sub(r'[^A-Za-z ]+', '',  movie_obj['title']).upper()
    director = movie_obj['director'] if movie_obj['director'] and movie_obj['director']!='nan' else ''
    actor = movie_obj['actors'][0] if movie_obj['actors'] else ''
    return movie, [year, director, actor]

def get_encoded(s):
    if s:
        return base64.b64encode(s.encode())
    else:
        return None

def get_str_or_null(s):
    if not s:
        return "null"
    else:
        return "'%s'" % s.decode("utf-8")

def lambda_handler(event, context):
    content = ""
    with open('index.html', 'r') as f:
        content = f.read()
    movie, details =get_movie()
    print(movie,details)
    movie = get_str_or_null(get_encoded(movie))
    year = get_str_or_null(get_encoded(str(details[0])))
    director = get_str_or_null(get_encoded(details[1]))
    actor = get_str_or_null(get_encoded(details[2]))
    
    
    content = content.replace("$MOVIE", movie)
    content = content.replace("$YEAR", year)
    content = content.replace("$DIRECTOR", director)
    content = content.replace("$ACTOR",actor )
    response = {
    "statusCode": 200,
    "body": content,
    "headers": {
        'Content-Type': 'text/html'
        }
    }
    return response