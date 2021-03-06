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

class NotFound(error.Error):
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
            entity = cls.get_or_insert(ndb.Key(cls, movie.get('Title')).id())
            entity.update(
                title = movie.get('Title'),
                year = movie.get('Year'),
                imdbID = movie.get('imdbID'),
                type_ = movie.get('Type'),
                poster = movie.get('Poster')
            )
            entity_list.append(entity)
            cls.get.lru_set(entity, args=[cls, entity.id])
            if(stop_condition(stop_arg1, stop_arg2)):
                break
        return entity_list

    def update(self, **kwargs):
        updates = [setattr(self, key, value) for key, value in kwargs.iteritems() if getattr(self, key) != value]
        if len(updates) > 0:
            self.put()
        return self

    @classmethod
    def initialize(cls, search_key, movies_to_find):
        found = 0
        if(len(Movie.query().fetch()) != 0):
            return 0
        page = 1
        while found < movies_to_find:
            entity_list = cls.create(search_key, page, found, movies_to_find, cls.all_movies_found)
            page += 1
            found += len(entity_list)
        return found

    @staticmethod
    def all_movies_found(found, required):
        if(found >= required):
            return True
        else:
            return False      

    @classmethod
    def search_movies(cls, search, page):
        URL = 'http://www.omdbapi.com/'
        PARAMS = {'apikey':environment.OMDB_KEY, 's':search, "page":page, 'type':'movie'}
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

    @classmethod
    def get_page(cls, page, items_per_page):
        items_per_page = items_per_page if items_per_page else 10
        return cls.query().order(cls.title).fetch(items_per_page, offset=items_per_page*(page-1))
         
    @property
    def id(self):
        return self.key.urlsafe()


def initializeDB(search_key="space", movies_to_find=100):
    return Movie.initialize(search_key, movies_to_find)

def search(title):
    return Movie.get_by_title(title)

def list_movies(page, items_per_page):
    page_list = []
    for movie in Movie.get_page(page, items_per_page):
        page_list.append(movie.to_dict())
    return page_list

def add(title):
    return Movie.create(title)

def delete(id):
    entity_key = ndb.Key(urlsafe=id)
    entity_key.delete()


