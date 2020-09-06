from backend import test
from backend import movies

class TestMovieDB(test.TestCase):
    def test_create(self):
        obj = movies.Movie.create("Raiders of the Lost Ark")
        self.assertEqual(obj[0], movies.Movie.get(obj[0].id))

    # def test_initializeDB(self):
    #     self.assertEqual(len(moviedb.Movie.query().fetch()), 0)
    #     moviedb.initializeDB()
    #     self.assertEqual(len(moviedb.Movie.query().fetch()), 100)

    # def test_db_already_initialized(self):
    #     moviedb.Movie.create("raiders of the lost ark")
    #     self.assertEqual(len(moviedb.Movie.query().fetch()), 1)
    #     moviedb.initializeDB()
    #     self.assertEqual(len(moviedb.Movie.query().fetch()), 1)

    # def test_not_enougth_movies(self):
    #     with self.assertRaises(moviedb.MoviesNotFound):
    #         moviedb.initializeDB("raiders of the lost ark")


