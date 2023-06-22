import psycopg2, os
import psycopg2

class PostgresConnector():
    def __init__(self) -> None:
        self._con: psycopg2.connection = None
        self._cur: psycopg2.cursor = None
    
    def open(self) -> any:
        if self._con == None:
            self._con = self._get_connection()
            self._cur = self._con.cursor()
        return [self._con, self._cur]
    
    def close(self) -> None:
        if self._con != None:
            self._con.commit()
            self._cur.close()
            self._con.close()

    def _get_connection(self) -> any:
        return psycopg2.connect(
            host=       os.environ["DB_HOST"],
            database=   os.environ["DB_NAME"],
            user=       os.environ["DB_USER"],
            password=   os.environ["DB_PASS"]
        )