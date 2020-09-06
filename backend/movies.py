import urllib
import urllib2
import json

from google.appengine.ext import ndb

from backend.cache import lru_cache
from backend import error, environment

class MoviesNotFound(error.Error):
    pass

class OMDBNotResponding(error.Error):
    pass

class Movie(ndb.Model):
    title = ndb.StringProperty(indexed=True)
    year = ndb.StringProperty(indexed=False)
    imdbID = ndb.StringProperty(indexed=False)
    type_ = ndb.StringProperty(indexed=False)
    poster = ndb.StringProperty(indexed=False)

    @classmethod
    def create(cls, title, page=1, stop_arg1=None, stop_arg2=None, stop_condition = lambda stop_arg1, stop_arg2: True):
        entity_list = []
        request = cls.search_movies(title, page)
        if(request['Response'] == 'False'):
            raise MoviesNotFound()
        for movie in request.get('Search'):
            entity = cls(
                title = movie.get('Title'),
                year = movie.get('Year'),
                imdbID = movie.get('imdbID'),
                type_ = movie.get('Type'),
                poster = movie.get('Poster')
            )
            entity.put()
            cls.get.lru_set(entity, args=[cls, entity.id])
            entity_list.append(entity)
            if(stop_condition(stop_arg1, stop_arg2)):
                break
        return entity_list

    @classmethod
    def initialize(cls, search_key, movies_to_find):
        if(len(Movie.query().fetch()) != 0):
            return
        page = 1
        found = 0
        while found < movies_to_find:
            entity_list = cls.create(search_key, page, found, movies_to_find, cls.all_movies_found)
            found += len(entity_list)
            page += 1

    @staticmethod
    def all_movies_found(found, required):
        if(found >= required):
            return True
        else:
            return False      

    @classmethod
    def search_movies(cls, search, page):
        URL = 'http://www.omdbapi.com/'
        PARAMS = {'apikey':environment.OMDB_KEY, 's':search, "page":page}
        data = urllib.urlencode(PARAMS)
        data = data.encode('ascii')
        full_url = URL + '?' + data
        try:
            response = urllib2.urlopen(full_url)
        except urllib2.URLError:
            raise OMDBNotResponding()
        return json.load(response)

    @classmethod
    @lru_cache()
    def get(cls, id):
        entity = None

        try:
            entity = ndb.Key(urlsafe=id).get()
        except:
            pass

        if entity is None or not isinstance(entity, cls):
            raise NotFound("No movie found with id: %s" % id)
        return entity

    @classmethod
    def get_by_title(cls, title):
        entities = cls.query(cls.title == title).fetch(1)
        return entities[0] if entities else None

    @property
    def id(self):
        return self.key.urlsafe()


def initializeDB(search_key="space", movies_to_find=100):
    Movie.initialize(search_key, movies_to_find)

def searchDB(title):
    return Movie.get_by_title(title)

def list_movies(page, items_per_page):
    pass

def add(title):
    Movie.create(title)

def delete(id):
    pass