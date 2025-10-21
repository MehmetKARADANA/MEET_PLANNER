from app.config import Base, engine
from app.models import employee,department,meeting


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Database tables created!")