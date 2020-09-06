from backend import test
from backend import movies

class TestMovies(test.TestCase):
    def test_create(self):
        obj = movies.Movie.create("Raiders of the Lost Ark")
        self.assertEqual(obj[0], movies.Movie.get(obj[0].id))
        self.assertTrue(obj[0].title == "Raiders of the Lost Ark")
        self.assertRaises(movies.MoviesNotFound, lambda: movies.Movie.create("aaaabbb"))

    def test_initialize(self):
        initialized = movies.initializeDB()
        self.assertEqual(initialized,100)
        initialized = movies.initializeDB()
        self.assertEqual(initialized,0)


