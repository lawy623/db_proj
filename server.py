#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.18.7/w4111"
#
DATABASEURI = "postgresql://yl4003:4758@34.73.21.127/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
    """
    This function is run at the beginning of every web request
    (every time you enter an address in the web browser).
    We use it to setup a database connection that can be used throughout the request.

    The variable g is globally accessible.
    """
    try:
        g.conn = engine.connect()
    except:
        print "uh oh, problem connecting to database"
        import traceback; traceback.print_exc()
        g.conn = None

@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't, the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception as e:
        pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
class News:
    def __init__(self, result):
        self.nid = result['nid']
        self.title = result['title']
        self.author = result['author']
        self.date = result['date']
        self.content = result['content']
        self.mid = result['mid']
        self.cid = result['cid']
        self.cname = result['cname']
        self.nation = result['nation']
        self.level = result['level']

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/home')
def home():
    news = []
    cursor = g.conn.execute("SELECT * FROM news ORDER BY date DESC")
    for result in cursor:
        news.append(News(result))

    context = dict(data = news)

    return render_template("home.html", **context)

@app.route('/home_match')
def home_match():
    pass

@app.route('/home_team')
def home_team():
    pass

@app.route('/home_score')
def home_score():
    pass

@app.route('/news') # This gets nid from '/home'
def news():
    nid = request.args.get('nid')
    cursor = g.conn.execute("SELECT * FROM news WHERE nid = (%s)", nid)
    result = cursor.fetchone()
    if not result.nid:
        return render_template("notfound.html")

    match = ""
    coach = ""
    team = ""
    if result.mid:
        matches = g.conn.execute("SELECT * FROM match WHERE mid = (%s)", result.mid)
        match = matches.fetchone()
    if result.cid:
        coaches = g.conn.execute("SELECT * FROM coach WHERE cid = (%s)", result.cid)
        coach = coaches.fetchone()
    if result.cname:
        teames = g.conn.execute("SELECT * FROM club WHERE cname = (%s) AND nation = (%s) AND level = (%s)", result.cname, result.nation, result.level)
        team = teames.fetchone()
    return render_template("news.html", news = result, match = match, coach = coach, team = team)

class Coach:
    def __init__(self, result):
        self.cid = result['cid']
        self.name = result['name']
        self.age = result['age']
        self.nationality = result['nationality']

@app.route('/coach')
def coach():
    cid = request.args.get('cid')
    coaches = g.conn.execute("SELECT * FROM coach WHERE cid = (%s)", cid)
    coach = coaches.fetchone()

    return render_template("coach.html", coach = coach)


@app.route('/match')
def match():
    mid = request.args.get('mid')
    if mid :
        return redirect('/home')
    else:
        return redirect('/')

class Team:
    def __init__(self, result):
        self.rank = result['rank']
        self.stadium = result['stadium']
        self.city = result['city']
        self.year = result['year']
        self.sponsor = result['sponsor']
        self.cid = result['cid']
        self.cname = result['cname']
        self.nation = result['nation']
        self.level = result['level']


@app.route('/team')
def team():
    cname = request.args.get('cname')
    nation = request.args.get('nation')
    level = request.args.get('level')
    pass


@app.route('/player')
def player():
    pass


# Example of adding new data to the database
# The add from index page will directly it to here.
# And it will also redirect back to the home page.
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
    return redirect('/')





if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        """

        HOST, PORT = host, port
        print "running on %s:%d" % (HOST, PORT)
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


    run()
