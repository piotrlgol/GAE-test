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
        initialized = movies.initializeDB()
        self.assertEqual(initialized,0)

    def test_search(self):
        obj = movies.add("Raiders of the Lost Ark")
        self.assertEqual(movies.search("Raiders of the Lost Ark"), obj[0])

    def test_list_movies(self):
        movies.initializeDB()
        self.assertEqual(len(movies.list_movies(page=1, items_per_page=10)), 10)

    def test_delete(self):
        obj = movies.add("Raiders of the Lost Ark")
        movies.delete(obj[0].id)
        self.assertEqual(movies.search("Raiders of the Lost Ark"), None)

class TestMovieApi(test.TestCase):
    def test_add(self):
        resp = self.api_mock.post("/api/movies.add", dict(title="Raiders of the Lost Ark"))
        self.assertEqual(resp.get("error"), None)
        self.assertEqual(movies.search("Raiders of the Lost Ark").title, "Raiders of the Lost Ark")

    def test_search(self):
        obj = movies.add("Raiders of the Lost Ark")
        resp = self.api_mock.post("/api/movies.search", dict(title="Raiders of the Lost Ark"))
        self.assertEqual(resp.get("error"), None)
        self.assertEqual(resp.get("title"), obj[0].title)

    def test_movies(self):
        movies.initializeDB()
        resp = self.api_mock.post("/api/movies.movies", dict(page=1))
        self.assertEqual(resp.get("error"), None)
        self.assertEqual(resp.movies, movies.list_movies(page=1, items_per_page=10))

    def test_delete(self):
        resp = self.api_mock.post("/api/user.create", dict(email="test@gmail.com", password="test"))
        self.assertEqual(resp.get("error"), None)
        resp = self.api_mock.post("/api/user.me")
        self.assertEqual(resp.get("email"), "test@gmail.com")

        obj = movies.add("Raiders of the Lost Ark")
        resp = self.api_mock.post("/api/movies.delete", dict(id=obj[0].id))
        self.assertEqual(resp.get("error"), None)
        self.assertEqual(movies.search("Raiders of the Lost Ark"), None)
