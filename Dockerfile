FROM python:3.9.1

RUN pip install pandas sqlalchemy psycopg2 pyarrow fastparquet

WORKDIR /app
COPY parquet_to_db.py parquet_to_db.py

ENTRYPOINT ["python", "parquet_to_db.py"]