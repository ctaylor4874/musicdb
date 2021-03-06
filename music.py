import json
import pycurl
import StringIO
import urllib
import mysql.connector
import sys
import dbconfig

dbUser = dbconfig.dbUser
dbPass = dbconfig.dbPass
dbHost = dbconfig.dbHost
dbName = dbconfig.dbName


#API:
# http://www.theaudiodb.com/forum/viewtopic.php?t=7
# get albums from artist
def getAlbums(artistName):
    url = "http://www.theaudiodb.com/api/v1/json/1/searchalbum.php?s=%s" % urllib.quote_plus(artistName)
    response = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, response.write)
    c.setopt(c.HTTPHEADER, ['Content-Type: application/json', 'Accept-Charset: UTF-8'])
    # c.setopt(c.HTTPHEADER, ['Content-Type: application/json'])
    c.setopt(c.POSTFIELDS, '@request.json')
    c.perform()
    c.close()
    albums = json.loads(response.getvalue())
    # albums = _byteify(json.load(response.getvalue(), object_hook=_byteify),ignore_dicts=True)
    response.close()
    return albums

# get tracks from album
def getTracks(idAlbum):
    url = "http://www.theaudiodb.com/api/v1/json/1/track.php?m=%s" % idAlbum
    response = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, response.write)
    c.setopt(c.HTTPHEADER, ['Content-Type: application/json', 'Accept-Charset: UTF-8'])
    # c.setopt(c.HTTPHEADER, ['Content-Type: application/json'])
    c.setopt(c.POSTFIELDS, '@request.json')
    c.perform()
    c.close()
    tracks = json.loads(response.getvalue())
    return tracks

# connect to database
class Database(object):
    @staticmethod
    def getConnection():
        return mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)

    @staticmethod
    def escape(value):
        return value.replace("'", "''")

    @staticmethod
    def getResult(query, getOne=False):
        conn = Database.getConnection()
        cur = conn.cursor()
        cur.execute(query)
        if getOne:
            result_set = cur.fetchone()
        else:
            result_set = cur.fetchall()
        cur.close()
        conn.close()
        return result_set

    @staticmethod
    def doQuery(query):
        conn = Database.getConnection()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        lastId = cur.lastrowid
        cur.close()
        conn.close()
        return lastId

# save artist
class Artist(object):
    def __init__(self, id=0):
        self.name = ""

        if (not type(id) == int):
            id = int(id)
        query = "SELECT id,name FROM artist where id=%d " % id
        result_set = Database.getResult(query, True)
        self.id = id
        if not result_set is None:
            self.id = result_set[0]
            self.content = result_set[1]
        return

    def save(self):
        if self.id > 0:
            return self.update()
        else:
            return self.insert()

    def insert(self):
        query = "insert into artist (name) values ('%s')" % (Database.escape(self.name))
        self.id = Database.doQuery(query)
        return self.id

    def update(self):
        query = "update artist set name='%s' where id=%d" % (Database.escape(self.name), self.id)
        # query = ("delete from page where id=%s" % id)
        return Database.doQuery(query)

# save albums from artist
class Album(object):
    def __init__(self, id=0):
        self.name = ""
        self.artist_id = 0
        self.release_date = 0000
        self.genre = ""

        if (not type(id) == int):
            id = int(id)
        query = "SELECT id,name,artist_id,release_date,genre FROM album where id=%d " % id
        result_set = Database.getResult(query, True)
        self.id = id
        if not result_set is None:
            self.id = result_set[0]
            self.content = result_set[1]
            self.artist_id = result_set[2]
            self.release_date = result_set[3]
            self.genre = result_set[4]
        return

    def save(self):
        if self.id > 0:
            return self.update()
        else:
            return self.insert()

    def insert(self):
        query = "insert into album (name,artist_id,release_date,genre) values ('%s',%d,%d,'%s')" % (
            Database.escape(self.name), self.artist_id, self.release_date,Database.escape(self.genre))
        self.id = Database.doQuery(query)
        return self.id

    def update(self):
        query = "update album set name='%s',artist_id=%d,release_date=%d,genre = '%s' where id=%d" % (
            Database.escape(self.name), self.artist_id, self.id, self.release_date,Database.escape(self.genre))
        # query = ("delete from page where id=%s" % id)
        return Database.doQuery(query)

# save tracks from albums
class Track(object):
    def __init__(self, id=0):
        self.name = ""
        self.album_id = 0
        self.duration = 0

        if (not type(id) == int):
            id = int(id)
        query = "SELECT id,name,album_id,duration FROM track where id=%d " % id
        result_set = Database.getResult(query, True)
        self.id = id
        if not result_set is None:
            self.id = result_set[0]
            self.content = result_set[1]
            self.artist_id = result_set[2]
            self.duration = result_set[3]
        return

    def save(self):
        if self.id > 0:
            return self.update()
        else:
            return self.insert()

    def insert(self):
        query = "insert into track (name,album_id,duration) values ('%s',%d,%d)" % (
            Database.escape(self.name), self.album_id, self.duration)
        self.id = Database.doQuery(query)
        return self.id

    def update(self):
        query = "update track set name='%s',album_id=%d,duration=%d where id=%d" % (
            Database.escape(self.name), self.album_id, self.duration, self.id)
        # query = ("delete from page where id=%s" % id)
        return Database.doQuery(query)


artistName = sys.argv[1]
albums = getAlbums(artistName)
artist = Artist()
artist.name = artistName
artist.save()
for album in albums["album"]:
    print('************************************')
    print album["strAlbum"]
    print album["intYearReleased"]
    print('************************************')
    a = Album()
    a.name = album["strAlbum"]
    a.artist_id = artist.id
    a.release_date = int(album["intYearReleased"])
    a.genre = album["strGenre"]
    a.save()
    idAlbum = album["idAlbum"]
    tracks = getTracks(idAlbum)
    for track in tracks["track"]:
        print track["strTrack"]
        t = Track()
        t.name = track["strTrack"]
        t.duration=int(track["intDuration"])
        t.album_id = a.id
        t.save()
