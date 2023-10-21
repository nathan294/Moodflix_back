from api.v1.commons.model_commons import Base
from api.v1.models.movie import Movie
from api.v1.models.movie_genre import MovieGenre
from api.v1.models.movie_list import MovieList
from api.v1.models.movie_list_association import MovieListAssociation
from api.v1.models.rating import Rating
from api.v1.models.user import User
from api.v1.models.wish import Wish

__all__ = [Base, User, Movie, MovieGenre, MovieList, MovieListAssociation, Rating, Wish]
