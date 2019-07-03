import os
import tvdbsimple as tvdb
tvdb.KEYS.API_KEY = os.environ.get('TVDB_KEY')


def get_image(name):
    search = tvdb.Search()
    try:
        search.series(name)
        serieid = search.series[0]['id']
        show = tvdb.Series(serieid)
        return show.info()['banner']
    except:
        return None
