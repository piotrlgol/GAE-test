from backend import test
from backend import movies

class TestMovies(test.TestCase):
    def test_create(self):
        obj = movies.add("Raiders of the Lost Ark")
        self.assertEqual(obj[0], movies.Movie.get(obj[0].id))
        self.assertTrue(obj[0].title == "Raiders of the Lost Ark")
        self.assertRaises(movies.MoviesNotFound, lambda: movies.add("aaaabbb"))

    def test_initialize(self):
        initialized = movies.initializeDB()
        self.assertEqual(initialized,100)

    def test_search(self):
        obj = movies.add("Raiders of the Lost Ark")
        self.assertEqual(movies.search("Raiders of the Lost Ark"), obj[0])

    def test_list_movies(self):
        self.assertEqual(len(movies.list_movies(page=1, items_per_page=10)), 10)


