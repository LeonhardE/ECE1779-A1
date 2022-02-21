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

    def put_image_key(self, imagekey, fname):
        cursor = self.db.cursor()
        query = '''INSERT INTO `image` (`image_name`, `image_location`)
                   VALUES (%s, %s);'''
        cursor.execute(query, (imagekey, fname))

        self.db.commit()

        return 0

    def get_all_list(self):
        cursor = self.db.cursor()
        query = "SELECT * FROM image;"
        cursor.execute(query)
        return cursor

    def get_all_key(self):
        cursor = self.db.cursor()
        query = "SELECT `image_name` FROM image;"
        cursor.execute(query)
        return cursor

    def set_config(self, capacity, replace_policy):
        cursor = self.db.cursor()
        query = '''UPDATE config SET `capacity` = %s, `replace_policy` = %s;'''
        cursor.execute(query, (capacity, replace_policy))

        # if the table is empty
        if cursor.rowcount == 0:  
            query = '''INSERT INTO `config` (`capacity`, `replace_policy`) VALUES (%s, %s);'''
            cursor.execute(query, (capacity, replace_policy))

        self.db.commit()
        return 0

    def get_location(self, key):
        cursor = self.db.cursor()
        query ="SELECT `image_location` FROM image WHERE `image_name` = '{}';"
        cursor.execute(query.format(key))
        return cursor

    def get_statistics(self, timestamp, num_item, size, num_request, num_miss):
        cursor = self.db.cursor()
        query = "SELECT `timestamp`,`num_item`,`size`,`num_request`,`num_miss` FROM `statistics` WHERE `timestamp` BETWEEN date_add(now(), interval - 10 minute) and now();"
        cursor.execute(query, (timestamp, num_item, size, num_request, num_miss))
        return cursor
