from flask import Flask, render_template, request, jsonify
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
        info = {}
        for entry in result:
            name = entry['name']
            image = entry['image']
            if image == '':
                image = info[name] if name in info else get_image(name)
                if image is not None:
                    self.cur.execute("update tvshows set image='%s' where name='%s'" % (image, name))
                    self.con.commit()
            info[name] = image
        self.names = sorted([name for name in info])

    def list_tvshows(self):
        results = []
        for name in self.names:
            self.cur.execute("SELECT name, finale, image FROM tvshows where name='%s' ORDER BY RAND() LIMIT 1" % name)
            result = self.cur.fetchall()
            results.extend(result)
        return results

    def add_tvshow(self, name, finale):
        self.cur.execute("insert into tvshows  values (0, '%s','%s','')" % (name, finale))
        self.con.commit()

    def delete_tvshow(self, name):
        self.cur.execute("delete from tvshows  where name = '%s'" % (name))
        self.con.commit()


@app.route('/')
def index():
    db = Database()
    tvshows = db.list_tvshows()
    return render_template('index.html', tvshows=tvshows, content_type='application/json')


@app.route('/tvshows')
def list_tvshows():
    """

    :return:
    """
    db = Database()
    tvshows = db.list_tvshows()
    return render_template('tvshows.html', tvshows=tvshows, content_type='application/json')


@app.route('/new', methods=['POST'])
def add_tvshow():
    name = request.form['name']
    finale = request.form['finale']
    db = Database()
    db.add_tvshow(name, finale)
    result = {'result': 'success'}
    response = jsonify(result)
    response.status_code = 200
    return response


@app.route('/delete', methods=['POST'])
def delete_tvshow():
    name = request.form['name']
    db = Database()
    db.delete_tvshow(name)
    result = {'result': 'success'}
    response = jsonify(result)
    response.status_code = 200
    return response


def run():
    """

    """
    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    run()
