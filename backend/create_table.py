from dbengine import engine
from db_models import Base

print("Creating table....")
Base.metadata.create_all(engine)
print("Table created successfully")