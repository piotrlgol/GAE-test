import json

from protorpc import remote, messages, message_types

from backend import api, movies
from backend.oauth2 import oauth2, Oauth2

class TitleRequest(messages.Message):
    title = messages.StringField(1)

class MovieResponse(messages.Message):
    title = messages.StringField(1)
    Year = messages.StringField(2)
    imdbID = messages.StringField(3)
    Type = messages.StringField(4)
    Poster = messages.StringField(5)

class MoviePageRequest(messages.Message):
    page = messages.IntegerField(1)
    items_per_page = messages.IntegerField(2)

class MoviePageResponse(messages.Message):
    movies = messages.StringField(1)

class MovieIDRequest(messages.Message):
    id= messages.StringField(1)


@api.endpoint(path="movies", title="Movies API")
class Movies(remote.Service):
    @remote.method(TitleRequest, MovieResponse)
    def search(self, request):
        movie = movies.searchDB(request.title)
        if movie is not None:
            return MovieResponse(
                title = movie.title,
                Year = movie.year,
                imdbID = movie.imdbID,
                Type = movie.type_,
                Poster = movie.poster
                )
        else:
            return MovieResponse()

    @remote.method(MoviePageRequest, MoviePageResponse)
    def movies(self, request):
        movies_page = movies.list_movies(request.page, request.items_per_page)
        return MoviePageResponse(movies=json.dumps(movies_page, ensure_ascii=True))

    @remote.method(TitleRequest, message_types.VoidMessage)
    def add(self, request):
        movies.add(request.title)
        return message_types.VoidMessage()

    @remote.method(message_types.VoidMessage, message_types.VoidMessage)
    def init(self, request):
        movies.initializeDB()
        return message_types.VoidMessage()

    @oauth2.required()
    @remote.method(MovieIDRequest, message_types.VoidMessage)
    def delete(self, request):
        movies.delete(request.id)
        return message_types.VoidMessage()