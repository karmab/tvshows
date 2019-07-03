from flask import Flask, render_template
import pymysql
import os
from tvdbhelper import get_image
app = Flask(__name__)
port = os.environ.get('PORT', 9000)
debug = bool(os.environ.get('DEBUG', True))
db = os.environ.get('DB_NAME', 'tvshows')
host = os.environ.get('DB_HOST', '127.0.0.1')
user = os.environ.get('DB_USER', 'dbadmin')
password = os.environ.get('DB_PASSWORD', 'dbadmin')


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
                image = get_image(name)
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

    def add_tvshow(self, name, finale):
        self.cur.execute("insert into tvshows  values (0, '%s','%s','');" % (name, finale))
        self.con.commit()


@app.route('/')
def list_tvshows():
    db = Database()
    tvshows = db.list_tvshows()
    return render_template('index.html', tvshows=tvshows, content_type='application/json')


@app.route('/new')
def add_tvshow():
    name, finale = '', ''
    db = Database()
    db.add_tvshow(name, finale)


def run():
    """

    """
    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    run()
