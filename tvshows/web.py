from flask import Flask, render_template
import pymysql
import os
app = Flask(__name__)
port = os.environ.get('PORT', 9000)
debug = bool(os.environ.get('DEBUG', True))
db = os.environ.get('DB', 'tvshows')
# host = os.environ.get('DBHOST', '127.0.0.1')
host = os.environ.get('DBHOST', '192.168.122.66')
user = os.environ.get('DBUSER', 'dbadmin')
password = os.environ.get('DBPASSWORD', 'dbadmin')


class Database:
    def __init__(self):
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def list_tvshows(self):
        self.cur.execute("SELECT distinct name FROM tvshows")
        names = [value['name'] for value in self.cur.fetchall()]
        results = []
        for name in names:
            self.cur.execute("SELECT name, finale, image FROM tvshows where name='%s' ORDER BY RAND() LIMIT 1" % name)
            result = self.cur.fetchall()
            results.extend(result)
        return results


@app.route('/')
def tvshows():
    def db_query():
        db = Database()
        emps = db.list_tvshows()
        return emps
    results = db_query()
    return render_template('tvshows.html', results=results, content_type='application/json')


def run():
    """

    """
    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    run()
