from flask import Flask, render_template
import pymysql
import os
import tvdbsimple as tvdb
app = Flask(__name__)
port = os.environ.get('PORT', 9000)
debug = bool(os.environ.get('DEBUG', True))
db = os.environ.get('DB', 'tvshows')
host = os.environ.get('DBHOST', '127.0.0.1')
user = os.environ.get('DBUSER', 'dbadmin')
password = os.environ.get('DBPASSWORD', 'dbadmin')
tvdb.KEYS.API_KEY = os.environ.get('TVDB_KEY')


class Database:
    def __init__(self):
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
        self.names = []
        self.cur.execute("SELECT name, image FROM tvshows")
        result = self.cur.fetchall()
        for entry in result:
            name = entry['name']
            image = entry['image']
            if name not in self.names:
                self.names.append(name)
            if image == '':
                image = self.get_image(name)
                if image is not None:
                    self.cur.execute("update tvshows set image='%s' where name='%s'" % (image, name))
                    self.con.commit()

    def list_tvshows(self):
        results = []
        for name in self.names:
            self.cur.execute("SELECT name, finale, image FROM tvshows where name='%s' ORDER BY RAND() LIMIT 1" % name)
            result = self.cur.fetchall()
            results.extend(result)
        return results

    def get_image(self, name):
        search = tvdb.Search()
        found = search.series(name)
        if found:
            serieid = search.series[0]['id']
            show = tvdb.Series(serieid)
            return show.info()['banner']
        else:
            return None


@app.route('/')
def tvshows():
    def db_query():
        db = Database()
        emps = db.list_tvshows()
        return emps
    results = db_query()
    return render_template('index.html', results=results, content_type='application/json')


def run():
    """

    """
    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    run()
