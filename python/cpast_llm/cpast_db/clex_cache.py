import sqlite3
import sys
import cpast_utils.models


def __sqlite3_run(*sqlite_query):
    """
    The function will take multiple queries and
    output the result in form of list
    such that output of query1 lies at index 0 ,
    Query2 at index 1 and so on.
    """
    output = []
    try:
        sqlite_connection = sqlite3.connect(cpast_utils.models.CLEX_CACHE_DB_FILENAME)
        cursor = sqlite_connection.cursor()
        for query in sqlite_query:
            if isinstance(query, (list, tuple)):
                if len(query) == 2:
                    query, val = query
                else:
                    query = query[0]
                    val = ()
            else:
                val = ()
            cursor.execute(query, val)
            if query.upper().startswith(('SELECT', 'DESC', 'SHOW')):
                output.append(cursor.fetchall())
            else:
                sqlite_connection.commit()
                output.append([])
        cursor.close()
        return output
    except sqlite3.Error as error:
        print(error, file=sys.stderr)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def __model_init() -> bool:
    def_query = """Create table IF NOT EXISTS clex_cache(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform varchar(255) NOT NULL,
            question_identifier varchar(255) NOT NULL,
            clex_generated varchar(255) NOT NULL);"""
    return __sqlite3_run(def_query) is not None


def add_cache(platform: str, question_identifier: str, clex_generated: str) -> bool:
    if __model_init():
        query = """INSERT INTO clex_cache (platform, question_identifier, clex_generated) VALUES(?,?,?);"""
        return (
            __sqlite3_run([query, (platform, question_identifier, clex_generated)])
            is not None
        )
    return False


def retrieve_cache(platform: str, question_identifier: str) -> str:
    if __model_init():
        query = """SELECT clex_generated FROM clex_cache WHERE platform=? AND question_identifier=?;"""
        response = __sqlite3_run([query, (platform, question_identifier)])
        if response and response[0]:
            return response[0][0][0]

    return ''


def update_cache(platform: str, question_identifier: str, clex_generated: str) -> bool:
    if __model_init():
        query = """UPDATE clex_cache SET clex_generated=? WHERE platform=? AND question_identifier=?;"""

        return (
            __sqlite3_run([query, (clex_generated, platform, question_identifier)])
            is not None
        )
    return False
