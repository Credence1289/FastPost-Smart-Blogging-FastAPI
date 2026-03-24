from backend.db.dbengine import engine
from backend.schema.db_models import Base

print("Creating table....")
Base.metadata.create_all(engine)
print("Table created successfully")