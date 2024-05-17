from time import time
import pandas as pd
from sqlalchemy import create_engine
import argparse
import os 

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db_name = params.db_name
    table_name = params.table_name
    url = params.url
    parquet_name = 'output.parquet'
    csv_name = 'output.csv'

    # Execute terminal command
    os.system(f'curl -0 {url} --output {parquet_name}')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    engine.connect()

    df = pd.read_parquet(parquet_name)
    df.to_csv(csv_name)
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    
    while True:
        time_start = time()
        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine, if_exists="append")
        time_end = time()
        print(f'Inserted chunk in {time_end - time_start:.3f} second(s)')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Insert data from CSV to Postgres")

    parser.add_argument('--user', help="username for postgres")
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db_name', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the postgres table where csv data will be stored')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)