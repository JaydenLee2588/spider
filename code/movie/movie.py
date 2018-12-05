class Movie:
    def __init__(self):
        self.name = ''
        self.image = ''
        self.mtrcbRating = ''
        self.genre = ''
        self.running_time = ''
        self.directors = []

    def __str__(self):
        director_str = ''
        for director in self.directors:
            director_str = director_str + director + ", "
        return "name: " + self.name + " genre: " + self.genre + " \ndirectors: " + director_str
