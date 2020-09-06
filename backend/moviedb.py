import requests

from backend import keyvalue, environment

class NotEnougthMovies(Exception):
    def __init__(self, message="There is not enougth movies for given search key"):
        self.message = message
    def __str__(self):
        return repr(self.message)

class MovieDBInitialization():
    @classmethod
    def insertmovies(cls, search_key, movies_to_find):
        if(len(keyvalue.KeyValue.query().fetch()) != 0):
            return
        page = 1
        while len(keyvalue.KeyValue.query().fetch()) < movies_to_find:
            request = cls.request_movies(search_key, page)
            if(request['Response'] == 'False'):
                raise NotEnougthMovies()
            for movie in request['Search']:
                keyvalue.set(movie['Title'], movie)
                if(len(keyvalue.KeyValue.query().fetch()) >= movies_to_find):
                    break
            page += 1      

    @classmethod
    def request_movies(cls, search, page):
        URL = 'http://www.omdbapi.com/'
        PARAMS = {'apikey':environment.OMDB_KEY, 's':search, "page":page}
        try:
            response = requests.get(url = URL, params = PARAMS) 
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        return response.json()


def initializeDB(search_key="space", movies_to_find=100):
    MovieDBInitialization.insertmovies(search_key, movies_to_find)

def searchDB():
    pass

def list_movies():
    pass

def add():
    pass

def delete():
    pass