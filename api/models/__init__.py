from api.models.commons import Base
from api.models.movie import Movie
from api.models.movie_genre import MovieGenre
from api.models.movie_list import MovieList
from api.models.movie_list_association import MovieListAssociation
from api.models.user import User

__all__ = [Base, User, Movie, MovieGenre, MovieList, MovieListAssociation]
