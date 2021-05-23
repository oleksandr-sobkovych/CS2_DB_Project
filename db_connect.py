import os
from sqlalchemy import create_engine
from credentials import DATABASE as DATABASE_URL

os.environ['DATABASE_URL'] = DATABASE_URL

engine = create_engine(DATABASE_URL)


