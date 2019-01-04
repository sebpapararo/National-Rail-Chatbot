from flask import Flask, render_template
from nlpu import *

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')





if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)

    # x = input("Hi there, what would you like to do?")
    # y = processInput(x)
    # print(y)





    # x = input("Hi there, what would you like to do?")

    y = MyClass(x)
    # print(y)







    # x = input("Hi there, what would you like to do?")

    # y = processInput(x)





#https://www.nltk.org/book/ch05.html

