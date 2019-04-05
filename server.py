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
from flask import Flask, request, render_template, g, redirect, Response, url_for

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

class League:
    def __init__(self, result):
        self.name = result['name']
        self.nation = result['nation']
        self.level = result['level']

class Coach:
    def __init__(self, result):
        self.cid = result['cid']
        self.name = result['name']
        self.age = result['age']
        self.nationality = result['nationality']

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

class Player:
    def cast_NULL(self, value):
        if value == '':
            return "NULL"
        return value

    def __init__(self, result):
        self.number = self.cast_NULL(result['number'])
        self.age = self.cast_NULL(result['age'])
        self.position = self.cast_NULL(result['position'])
        self.price = self.cast_NULL(result['price'])
        self.height = self.cast_NULL(result['height'])
        self.nationality = self.cast_NULL(result['nationality'])
        self.name = self.cast_NULL(result['name'])
        self.since = self.cast_NULL(result['since'])
        self.cname = self.cast_NULL(result['cname'])
        self.nation = self.cast_NULL(result['nation'])
        self.level = self.cast_NULL(result['level'])
        self.foot = self.cast_NULL(result['foot'])

class Match:
    def __init__(self, result):
        self.mid = result['mid']
        self.date = result['date']
        self.time = result['time']
        self.host = result['host']
        self.guest = result['guest']
        self.nation = result['nation']
        self.level = result['level']

class Score:
    def __init__(self, result):
        self.mid = result['mid']
        self.date = result['date']
        self.time = result['time']
        self.host = result['host']
        self.guest = result['guest']
        self.goal_num = result['goal_num']
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
    nation = request.args.get('nation')
    level = request.args.get('level')

    leagues = [] # All the leagues that contains team infomation.
    cursor_leagues = g.conn.execute("SELECT DISTINCT L.nation, L.level, L.name FROM league L JOIN club C ON L.nation = C.nation AND L.level = C.level ORDER BY L.nation, L.level")
    for result in cursor_leagues:
        leagues.append(League(result))

    if not nation and not level: # dafault case
        nation_default = leagues[0].nation
        level_default = leagues[0].level
        matches = []
        cursor_matches = g.conn.execute("SELECT * FROM match WHERE nation = (%s) AND level = (%s) ORDER BY date, time ASC", nation_default, level_default)
        for result in cursor_matches:
            matches.append(Match(result))

        return render_template("home_match.html", leagues = leagues, nation = nation_default, level = level_default, matches = matches)
    else:
        matches = []
        cursor_matches = g.conn.execute("SELECT * FROM match WHERE nation = (%s) AND level = (%s) ORDER BY date, time ASC", nation, level)
        for result in cursor_matches:
            matches.append(Match(result))

        return render_template("home_match.html", leagues = leagues, nation = nation, level = int(level), matches = matches)

@app.route('/home_team')
def home_team():
    nation = request.args.get('nation')
    level = request.args.get('level')

    leagues = [] # All the leagues that contains team infomation.
    cursor_leagues = g.conn.execute("SELECT DISTINCT L.nation, L.level, L.name FROM league L JOIN club C ON L.nation = C.nation AND L.level = C.level ORDER BY L.nation, L.level")
    for result in cursor_leagues:
        leagues.append(League(result))

    if not nation and not level: # dafault case
        nation_default = leagues[0].nation
        level_default = leagues[0].level
        teams = []
        cursor_teams = g.conn.execute("SELECT * FROM club WHERE nation = (%s) AND level = (%s) ORDER BY rank ASC", nation_default, level_default)
        for result in cursor_teams:
            teams.append(Team(result))

        return render_template("home_team.html", leagues = leagues, nation = nation_default, level = level_default, teams = teams)
    else:
        teams = []
        cursor_teams = g.conn.execute("SELECT * FROM club WHERE nation = (%s) AND level = (%s) ORDER BY rank ASC", nation, level)
        for result in cursor_teams:
            teams.append(Team(result))

        return render_template("home_team.html", leagues = leagues, nation = nation, level = int(level), teams = teams)


@app.route('/home_score')
def home_score():
    nation = request.args.get('nation')
    level = request.args.get('level')

    leagues = [] # All the leagues that contains team infomation.
    cursor_leagues = g.conn.execute("SELECT DISTINCT L.nation, L.level, L.name FROM league L JOIN club C ON L.nation = C.nation AND L.level = C.level ORDER BY L.nation, L.level")
    for result in cursor_leagues:
        leagues.append(League(result))

    if not nation and not level: # dafault case
        nation_default = leagues[0].nation
        level_default = leagues[0].level
        scores = []
        cursor_scores = g.conn.execute("SELECT P.cname, P.number, P.name, T.goal FROM player P JOIN (SELECT nation, level, cname, number, sum(goal_num) AS goal FROM score WHERE nation = (%s) AND level = (%s) AND own_goal = 0 GROUP BY nation, level, cname, number) T ON P.nation = T.nation AND P.level = T.level AND P.cname = T.cname AND P.number = T.number ORDER BY T.goal DESC", nation_default, level_default)
        for result in cursor_scores:
            scores.append(result)

        return render_template("home_score.html", leagues = leagues, nation = nation_default, level = level_default, scores = scores)
    else:
        scores = []
        cursor_scores = g.conn.execute("SELECT P.cname, P.number, P.name, T.goal FROM player P JOIN (SELECT nation, level, cname, number, sum(goal_num) AS goal FROM score WHERE nation = (%s) AND level = (%s) AND own_goal = 0 GROUP BY nation, level, cname, number) T ON P.nation = T.nation AND P.level = T.level AND P.cname = T.cname AND P.number = T.number ORDER BY T.goal DESC", nation, level)
        for result in cursor_scores:
            scores.append(result)

        return render_template("home_score.html", leagues = leagues, nation = nation, level = int(level), scores = scores)

@app.route('/news') # This gets nid from '/home'
def news():
    nid = request.args.get('nid')
    cursor = g.conn.execute("SELECT * FROM news WHERE nid = (%s)", nid)
    result = cursor.fetchone()
    if not result.nid: # The enquired news is not in db. May be deleted.
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


@app.route('/coach')
def coach():
    cid = request.args.get('cid')
    coaches = g.conn.execute("SELECT * FROM coach WHERE cid = (%s)", cid)
    coach = coaches.fetchone()
    if not coach.cid: # The enquired coach is not in db. May be deleted.
        return render_template("notfound.html")

    teams = g.conn.execute("SELECT * FROM club WHERE cid = (%s)", cid)
    team = teams.fetchone()

    return render_template("coach.html", coach = coach, team = team)


@app.route('/match')
def match():
    mid = request.args.get('mid')
    matches = g.conn.execute("SELECT * FROM match WHERE mid = (%s)", mid)
    match = matches.fetchone()
    if not match.mid: # The enquired match is not in db. May be deleted.
        return render_template("notfound.html")

    cursor_score_in_match = g.conn.execute("SELECT * FROM score WHERE mid = (%s)", mid)
    if cursor_score_in_match.rowcount == 0: # no match record in score
        no_record = 1
    else:
        no_record = 0

    ## Scores
    home_scores = []
    cursor_home_scores = g.conn.execute("SELECT P.number, P.name, S.goal_num, S.nation, S.level, S.cname FROM score S JOIN player P ON P.number = S.number AND P.cname = S.cname AND P.nation = S.nation AND P.level = S.level WHERE S.mid = (%s) AND S.cname = (%s) AND S.own_goal = 0", mid, match.host)
    for result in cursor_home_scores:
        home_scores.append(result)
    home_own_scores = []
    cursor_home_own_scores = g.conn.execute("SELECT P.number, P.name, S.goal_num, S.nation, S.level, S.cname FROM score S JOIN player P ON P.number = S.number AND P.cname = S.cname AND P.nation = S.nation AND P.level = S.level WHERE S.mid = (%s) AND S.cname = (%s) AND S.own_goal = 1", mid, match.host)
    for result in cursor_home_own_scores:
        home_own_scores.append(result)

    guest_scores = []
    cursor_guest_scores = g.conn.execute("SELECT P.number, P.name, S.goal_num, S.nation, S.level, S.cname FROM score S JOIN player P ON P.number = S.number AND P.cname = S.cname AND P.nation = S.nation AND P.level = S.level WHERE S.mid = (%s) AND S.cname = (%s) AND S.own_goal = 0", mid, match.guest)
    for result in cursor_guest_scores:
        guest_scores.append(result)
    guest_own_scores = []
    cursor_guest_own_scores = g.conn.execute("SELECT P.number, P.name, S.goal_num, S.nation, S.level, S.cname FROM score S JOIN player P ON P.number = S.number AND P.cname = S.cname AND P.nation = S.nation AND P.level = S.level WHERE S.mid = (%s) AND S.cname = (%s) AND S.own_goal = 1", mid, match.guest)
    for result in cursor_guest_own_scores:
        guest_own_scores.append(result)

    num_home_scores = 0
    num_guest_scores = 0
    for s in home_scores:
        num_home_scores += s.goal_num
    for s in guest_own_scores:
        num_home_scores += s.goal_num

    for s in guest_scores:
        num_guest_scores += s.goal_num
    for s in home_own_scores:
        num_guest_scores += s.goal_num
    ## stadium
    cursor_stadium = g.conn.execute("SELECT stadium FROM club WHERE cname = (%s) AND nation = (%s) AND level = (%s)", match.host, match.nation, match.level)
    result = cursor_stadium.fetchone()
    stadium = result.stadium

    return render_template("match.html", match = match, no_record = no_record, home_scores = home_scores, home_own_scores = home_own_scores, guest_scores = guest_scores, guest_own_scores = guest_own_scores, stadium = stadium, num_home_scores = num_home_scores, num_guest_scores = num_guest_scores)

@app.route('/add_match_record')
def add_match_record():
    mid = request.args.get('mid')
    matches = g.conn.execute("SELECT * FROM match WHERE mid = (%s)", mid)
    match = matches.fetchone()
    if not match.mid: # The enquired match is not in db. May be deleted.
        return render_template("notfound.html")

    home_players = []
    cursor_home_players = g.conn.execute("SELECT name, number FROM player WHERE nation = (%s) AND level = (%s) AND cname = (%s)", match.nation, match.level, match.host);
    for result in cursor_home_players:
        home_players.append(result)

    guest_players = []
    cursor_guest_players = g.conn.execute("SELECT name, number FROM player WHERE nation = (%s) AND level = (%s) AND cname = (%s)", match.nation, match.level, match.guest);
    for result in cursor_guest_players:
        guest_players.append(result)

    return render_template("add_match_record.html", match = match, home_players = home_players, guest_players = guest_players)

@app.route('/team')
def team():
    cname = request.args.get('cname')
    nation = request.args.get('nation')
    level = request.args.get('level')
    teams = g.conn.execute("SELECT * FROM club WHERE cname = (%s) AND nation = (%s) AND level = (%s)", cname, nation, level)
    team = teams.fetchone()
    if not team.cname: # The enquired player is not in db. May be deleted.
        return render_template("notfound.html")

    # league
    leagues = g.conn.execute("SELECT * FROM league WHERE nation = (%s) AND level = (%s)", nation, level)
    league = leagues.fetchone()
    # matches of the team:
    matches = []
    cursor_matches = g.conn.execute("SELECT * FROM match WHERE host = (%s) OR guest = (%s) AND nation = (%s) AND level = (%s) ORDER BY date, time", cname, cname, nation, level)
    for result in cursor_matches:
        matches.append(Match(result))
    # coach:
    cursor_coach = g.conn.execute("SELECT * FROM coach WHERE cid = (%s)", team.cid)
    coach = cursor_coach.fetchone()
    # players:
    players = []
    cursor_players = g.conn.execute("SELECT * FROM player WHERE cname = (%s) AND nation = (%s) AND level = (%s) ORDER BY number", cname, nation, level)
    for result in cursor_players:
        players.append(Player(result))

    return render_template("team.html", team = team, league = league, matches = matches, coach = coach, players = players)


@app.route('/player')
def player():
    number = request.args.get('number')
    cname = request.args.get('cname')
    nation = request.args.get('nation')
    level = request.args.get('level')
    players = g.conn.execute("SELECT * FROM player WHERE number = (%s) AND cname = (%s) AND nation = (%s) AND level = (%s)", number, cname, nation, level)
    player = players.fetchone()
    if not player.number: # The enquired player is not in db. May be deleted.
        return render_template("notfound.html")
    ## Scores
    scores = []
    cursor_scores = g.conn.execute("SELECT * FROM score S JOIN match M on S.mid = M.mid WHERE S.number = (%s) AND S.cname = (%s) AND S.nation = (%s) AND S.level = (%s)", number, cname, nation, level)
    for result in cursor_scores:
        scores.append(Score(result))

    any_score = len(scores)

    return render_template("player.html", player = player, any_score = any_score, scores = scores)

@app.route('/add_player', methods=['POST'])
def add_player():
    player = Player(request.form)
    if player.number == "NULL":
        return render_template("insert_null.html")

    g.conn.execute("INSERT INTO player VALUES ({},{},{},\"{}\",{},\"{}\",\"{}\",{},\"{}\",{},{},\"{}\")".format(player.number, player.age, player.position, player.price, player.height, player.nationality, player.name, player.since, player.cname, player.nation, player.level, player.foot))
    return redirect(url_for('team', nation = player.nation, level = player.level, cname = player.cname))






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
