from sqlalchemy import create_engine, text
from dotenv import load_dotenv 
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database(), version()")
        )

        print("Database connected successfully")

        for row in result:
            print("Database:", row[0])
            print("Version: ", row[1])

except Exception as error:
    print("Database connection failed")
    print(error)