from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

class Edit(FlaskForm):
    rating = StringField('Your rating out of 10, e.g. 7.5', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    submit = SubmitField('Done')


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-10-movies.db"
db.init_app(app)

class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True)
    year: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)
    rating: Mapped[float] = mapped_column(Float)
    ranking: Mapped[int] = mapped_column(Integer)
    review: Mapped[str] = mapped_column(String)
    img_url: Mapped[str] = mapped_column(String)


with app.app_context():
    db.create_all()

# with app.app_context():
#     second_movie = Movie(
#         title="Avatar The Way of Water",
#         year=2022,
#         description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#         rating=7.3,
#         ranking=9,
#         review="I liked the water.",
#         img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
#     )
#     db.session.add(second_movie)
#     db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():  # put application's code here
    result = db.session.execute(db.select(Movie))
    all_movies = result.scalars().all()
    return render_template("index.html", movies=all_movies)


@app.route('/edit', methods=['GET', 'POST'])
def rate_movie():
    form = Edit()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("edit.html", movie=movie, form=form)

@app.route('/delete')
def delete_entry():
    # Fetch the entry to delete
    movie_id = request.args.get("id")
    movie = db.session.get(Movie, movie_id)
    if movie:
        db.session.delete(movie)  # Mark the entry for deletion
        db.session.commit()       # Commit changes to the database
    return redirect(url_for("index"))


@app.route("/add")


if __name__ == '__main__':
    app.run(debug=True)
