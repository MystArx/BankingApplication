from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy.engine import URL
from config.settings import db_host,db_name,db_password,db_port,db_username

databaseurl=URL.create(drivername="mysql+pymysql",
                       username=db_username,
                       host=db_host,
                       database=db_name,
                       password=db_password,
                       port=db_port)


engine=create_engine(databaseurl)
LocalSession=sessionmaker(bind=engine)

Base=declarative_base()
