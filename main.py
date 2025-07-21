from flask import Flask, render_template, request, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''





app = Flask(__name__)

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Book.db"
# initialize the app with the extension
db.init_app(app)

class all_book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.args.get('id'):
            book_id = request.args.get('id')
            new_rating= request.form.get('quantity')
            book = db.session.execute(
            db.select(all_book).filter_by(id=book_id)).scalar()
            book.rating = float(new_rating)

        if request.form.get('book_name'):
            with app.app_context():
                book = all_book(name=request.form.get('book_name'),
                                author=request.form.get('author'),
                                rating=request.form.get('rating')
                                )
            db.session.add(book)
            db.session.commit()




    book_data = db.session.execute(db.select(all_book).order_by(all_book.id)).scalars()
    return render_template('index.html', book_data=book_data)


@app.route("/add", methods=['Get', 'POST'])
def add():

    return render_template('add.html')


@app.route('/edit')
def update():
    keyword = request.args.get("id")
    print(keyword)
    with app.app_context():
        book = db.session.execute(
            db.select(all_book).filter_by(id=keyword)
        ).scalar_one_or_none()
    return render_template('edit_rating.html', book=book)


@app.route('/delete')
def delete_book():
    book_id = request.args.get('deleting_id')
    book = db.session.execute(
        db.select(all_book).filter_by(id=int(book_id))
    ).scalar_one_or_none()

    db.session.delete(book)   # delete from session
    db.session.commit()       # commit to DB

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

