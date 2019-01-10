import sqlite3

from flask import Flask, render_template, request, g, redirect
from pyknow import *

from KB_main import *

app = Flask(__name__)
DATABASE = 'database.db'
engine = trainBot()


# Database Methods
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))

    db.row_factory = make_dicts
    return db


def query_db(query, args=(), one=False):
    cur = None
    rv = None
    try:

        cur = get_db().execute(query, args)
        rv = cur.fetchall()
    except sqlite3.Error as e:
        app.logger.info('Database error: %s' % e)
    except Exception as e:
        app.logger.info('Exception in query_db: %s' % e)
    finally:
        if cur:
            cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    global engine
    # engine.reset()
    # engine.run()

    query = "SELECT itemid, item FROM chatHist"
    result = query_db(query)

    return render_template('index.html', data=result)


@app.route('/userUpdate', methods=['GET', 'POST'])
def userUpdate():
    global engine
    userInput = request.form.get('inputBox')

    query = 'INSERT INTO chatHist (item) VALUES("%s");' % (userInput)
    result = query_db(query)
    get_db().commit()

    trainBot.passReply(userInput, engine)
    # engine.declare(Fact(receivedInput='true'))
    # engine.facts.duplication = True
    # engine.duplicate(engine.facts[2], receivedInput='true')
    engine.run()
    # engine.duplicate(engine.facts[2], receivedInput='false')

    query = "SELECT itemid, item FROM chatHist"
    result = query_db(query)

    return redirect('/')

    # return render_template('index.html', data=result)


@app.route('/botUpdate', methods=['GET', 'POST'])
def botUpdate(botReply):

    query = 'INSERT INTO chatHist (item) VALUES("%s");' % (botReply)
    result = query_db(query)
    get_db().commit()

    query = "SELECT itemid, item FROM chatHist"
    result = query_db(query)

    return render_template('index.html', data=result)


@app.route('/restartChat', methods=['GET', 'POST'])
def restartChat():
    global engine
    query = 'DELETE FROM chatHist;'
    result = query_db(query)
    get_db().commit()

    query = 'DELETE FROM sqlite_sequence WHERE name = "chatHist";'
    result = query_db(query)
    get_db().commit()

    # engine = trainBot()
    engine.reset()
    # engine.run()

    return redirect('/')


if __name__ == '__main__':

    with app.app_context():
        restartChat()
        engine.reset()
        engine.run()

    app.run(host='127.0.0.1', debug=True)
