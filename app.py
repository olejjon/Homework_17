# app.py

from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('director')
genre_ns = api.namespace('genre')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Int()
    genre_id = fields.Int()
    genre = fields.Str()
    director_id = fields.Int()
    director = fields.Str()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        # all_books = db.session.query(Movie).all()
        qf = Movie.query
        if director_id:
            qf = qf.filter(Movie.director_id == director_id)
        if genre_id:
            qf = qf.filter(Movie.genre_id == genre_id)
        movies = qf.all()
        return movies_schema.dump(movies), 200

    def post(self):
        movie_data = request.json
        new_data = Movie(**movie_data)
        db.session.add()
        db.session.commit()
        return '', 201, {'movie_id': new_data.id}



@movie_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id: int):
        movie = Movie.query.get(id)
        # movie = db.session.query(Movie).filter(Movie.id == id).one()
        if not movie:
            return '', 404
        return movie_schema.dump(movie), 200

    def put(self, id:int):
        movie = Movie.query.get(id)
        if not movie:
            return '', 404
        movie_data = request.json
        movie.title = movie_data.get('title')
        movie.description = movie_data.get('description')
        movie.trailer = movie_data.get('trailer')
        movie.year = movie_data.get('year')
        movie.rating = movie_data.get('rating')
        movie.genre_id = movie_data.get('genre_id')
        movie.genre = movie_data.get('genre')
        movie.director_id = movie_data.get('director_id')
        movie.director = movie_data.get('director')

        db.session.add(movie)
        db.session.commit()
        return '', 204

    def delete(self, id: int):
        movie = Movie.query.get(id)
        # movie = db.session.query(Movie).filter(Movie.id == id).one()
        if not movie:
            return '', 404
        db.session.delete(movie)
        return '', 204




# @director_ns.route('/')
# class DirectorsView(Resource):
#     def get(self):
#         all_directors = db.session.query(Director).all()
#         return directors_schema.dump(all_directors), 200
#
#
# @director_ns.route('/<int:id>')
# class DirectorView(Resource):
#     def get(self, id):
#         try:
#             director = db.session.query(Director).filter(Director.id == id).one()
#             return directors_schema.dump(director), 200
#         except Exception as e:
#             return str(e), 404
#
#
# @genre_ns.route('/')
# class GenresView(Resource):
#     def get(self):
#         all_genres = db.session.query(Genre).all()
#         return genres_schema.dump(all_genres), 200
#
#
# @genre_ns.route('/<int:id>')
# class GenreView(Resource):
#     def get(self, id):
#         try:
#             genre = db.session.query(Genre).filter(Movie.id == id).one()
#             return genre_schema.dump(genre), 200
#         except Exception as e:
#             return str(e), 404


if __name__ == '__main__':
    app.run(debug=True)
