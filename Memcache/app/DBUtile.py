import mysql.connector

from app import config


class DBUtil:

    def __init__(self):
        self.user = config.db_config['user']
        self.password = config.db_config['password']
        self.host = config.db_config['host']
        self.database = config.db_config['database']

        self.db = self.get_db()

    def get_db(self):
        return mysql.connector.connect(user=self.user,
                                       password=self.password,
                                       host=self.host,
                                       database=self.database)

    def put_statistics(self, num_item, size, num_request, num_get_request, num_miss):
        cursor = self.db.cursor(buffered=True)
        query = "INSERT INTO `statistics` (`timestamp`, `num_item`, `size`," \
                + "`num_request`, `num_GET_request`, `num_miss`)" \
                + "VALUES (NOW(), {}, {}, {}, {}, {});"
        cursor.execute(query.format(num_item, size, num_request, num_get_request, num_miss))

        self.db.commit()
        if cursor.rowcount == 0:
            return -1
        return 0

    def put_config(self, capacity, replace_policy):
        cursor = self.db.cursor(buffered=True)
        query = "UPDATE config SET `capacity` = {}, `replace_policy` = '{}';"
        cursor.execute(query.format(capacity, replace_policy))

        if cursor.rowcount == 0:  # the table is empty
            query = "INSERT INTO `config` (`capacity`, `replace_policy`) VALUES ({}, '{}');"
            cursor.execute(query.format(capacity, replace_policy))

        self.db.commit()

    def get_config(self):
        cursor = self.db.cursor(buffered=True)
        query = "SELECT `capacity`, `replace_policy` FROM config;"
        cursor.execute(query)

        for i in cursor:
            return i

    def clear_statistics(self):
        cursor = self.db.cursor(buffered=True)
        query = "DELETE FROM statistics;"
        cursor.execute(query)

        self.db.commit()
        if cursor.rowcount == 0:
            return -1
        return 0
