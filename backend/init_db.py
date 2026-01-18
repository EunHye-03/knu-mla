"""
Database initialization script
Creates all tables defined in the models
"""
from app.db.session import engine
from app.db.base import Base

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✓ Database tables created successfully!")

# Verify tables were created
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"\nCreated {len(tables)} tables:")
for table in sorted(tables):
    print(f"  - {table}")
