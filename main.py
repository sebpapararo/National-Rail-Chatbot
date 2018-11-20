from nlpu import *
from flask import Flask, render_template

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')





if __name__ == '__main__':
    #app.run(host='127.0.0.1', debug=True)

    y = testingGround()
    #y.testing()

    x = MyClass("Book a train please")
    x.getVerbs()


#https://www.nltk.org/book/ch05.html

