import sqlite3
import gossip_pb2
import datetime

def get_build_from_row(row):
    build = gossip_pb2.AddBuildRequest()
    build.sha1 = row[0]
    build.node = row[1]
    build.uname = row[2]
    build.toolchain = row[3]
    build.revision = row[4]
    build.start_time = row[5]
    build.end_time = row[6]
    build.log = row[7]
    build.status = row[8]
    return build

class DB(object):
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def get_all_builds(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM builds")
        builds = []
        for row in c.fetchall():
            builds.append(get_build_from_row(row))
        return builds

    def insert_build(self, build):
        c = self.conn.cursor()
        start_time = str(datetime.datetime.fromtimestamp(float(build.start_time) / 1000000.0))
        end_time = str(datetime.datetime.fromtimestamp(float(build.end_time) / 1000000.0))
        c.execute("INSERT INTO builds VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (build.sha1, build.node, build.uname, build.toolchain, build.revision,
                   start_time, end_time, build.log, build.status))
        self.conn.commit()

    def exists_build(self, build):
        c = self.conn.cursor()
        c.execute("SELECT * FROM builds WHERE sha1=?", (build.sha1,))
        return c.fetchone() != None

    def bootstrap(self, sql_file):
        c = self.conn.cursor()
        c.executescript(open(sql_file, "r").read())
        self.conn.commit()
