from logging import getLogger

from asyncpg import Connection


logger = getLogger('DataBase')


class DBRepo:
    def __init__(self, connection: Connection):
        self.conn: Connection = connection
        logger.debug(f'New Database Repository instance: {self}')
