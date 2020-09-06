from backend import test
from backend import moviedb
from backend import keyvalue

class TestMovieDBInitialization(test.TestCase):
    def test_initializeDB(self):
        self.assertEqual(len(keyvalue.KeyValue.query().fetch()), 0)
        moviedbinitialization.initializeDB()
        self.assertEqual(len(keyvalue.KeyValue.query().fetch()), 100)

    def test_db_already_initialized(self):
        keyvalue.set("key", "value")
        self.assertEqual(len(keyvalue.KeyValue.query().fetch()), 1)
        moviedbinitialization.initializeDB()
        self.assertEqual(len(keyvalue.KeyValue.query().fetch()), 1)

    def test_not_enougth_movies(self):
        with self.assertRaises(moviedbinitialization.NotEnougthMovies):
            moviedbinitialization.initializeDB("raiders of the lost ark")


