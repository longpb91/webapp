from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import traceback
# from dotenv import load_dotenv

# load_dotenv()


app = Flask(__name__)

# ENV = 'dev'
ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_DEV')
else:
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_2') 
    print(os.environ.get('DATABASE_URL_2'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/submit", methods=['POST'])
def submit():
    try:
        if request.method == "POST":
            customer = request.form['customer']
            dealer = request.form['dealer']
            rating = request.form['rating']
            comments = request.form['comments']
            # print(customer, dealer, rating, comments)
            if customer == "" or dealer == "":
                return render_template('index.html', message='Please enter required fields')
            
            if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
                # add data to database
                data = Feedback(customer, dealer, rating, comments)
                db.session.add(data)
                db.session.commit()

                return render_template('success.html')
            return render_template('index.html', message='You have already submitted feedback')
    except Exception as e:
        return str(e)
        # return traceback.print_exc()

        
if __name__ == "__main__":
    # app.debug = True
    app.run()

