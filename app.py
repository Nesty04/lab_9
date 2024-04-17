from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.name

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        author = request.form['author']
        name = request.form['name']
        new_book = Book(author=author, name=name)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('index'))

    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/delete/<int:id>')
def delete(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
