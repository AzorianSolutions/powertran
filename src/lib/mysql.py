import MySQLdb
import os
from loguru import logger
from MySQLdb.connections import Connection


class MySQLClient:
    """ A MySQL client for the Powercode database. """

    _db: Connection = None

    @staticmethod
    def db() -> Connection:
        """ Return the MySQL database connection. Instantiate if necessary. """
        if MySQLClient._db is None:
            logger.debug('Instantiating MySQL database connection')
            MySQLClient._db = MySQLdb.connect(
                host=os.getenv('PT_MYSQL_HOST', 'localhost'),
                port=int(os.getenv('PT_MYSQL_PORT', 3306)),
                user=os.getenv('PT_MYSQL_USER', 'root'),
                passwd=os.getenv('PT_MYSQL_PASSWORD'),
                database=os.getenv('PT_MYSQL_DATABASE', 'powernoc'),
                cursorclass=MySQLdb.cursors.DictCursor,
            )
        return MySQLClient._db
