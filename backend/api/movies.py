from protorpc import remote, messages

from backend import api, moviedb
from backend.oauth2 import oauth2, Oauth2

@api.endpoint(path="moviedb", title="MovieDB API")
class Movies(remote.Service):
    @remote.method(message_types.VoidMessage, message_types.VoidMessage)
    def search(self, request):
        pass

    @remote.method(message_types.VoidMessage, message_types.VoidMessage)
    def movies(self, request):
        pass

    @remote.method(message_types.VoidMessage, message_types.VoidMessage)
    def add(self, request):
        pass

    @oauth2.required()
    @remote.method(message_types.VoidMessage, message_types.VoidMessage)
    def delete(self, request):
        pass