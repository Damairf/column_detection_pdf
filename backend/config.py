import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:fakhruddin@localhost:5432/column_detection"
)