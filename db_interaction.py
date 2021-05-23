"""
Main module to interact with the database
"""
from sqlalchemy.orm import sessionmaker
from db_connect import engine


# def _catch_pg_errors(func):
#     def wrapper(cls, query):
#         try:
#             return func(cls, query)
#         except (psycopg2.IntegrityError, psycopg2.InternalError) as err:
#             # constraint not satisfied
#             print("Error happened: ", err)
#             cls.curs.execute("ROLLBACK")
#             cls.conn.commit()
#
#     return wrapper


class DBInteraction:
    def __init__(self):
        self.session = sessionmaker(bind=engine)





