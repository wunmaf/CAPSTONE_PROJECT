import configparser
import boto3 
import pandas as pd
import psycopg2 
import logging
import redshift_connector



from utils.helper import create_bucket
from sqlalchemy import create_engine
from sql_statements.create import dev_tables ,transformed_tables
from sql_statements.transform import transformation_queries



config = configparser.ConfigParser()
config.read('.env')


access_key = config['AWS']['access_key']
secret_key = config['AWS']['secret_key']
bucket_name = config['AWS']['bucket_name']
region = config['AWS']['region']
role=config['AWS']['arn']


db_host = config['DB_CRED']['host']
db_user = config['DB_CRED']['user']
db_password = config['DB_CRED']['password']
db_database = config['DB_CRED']['database']


dwh_host = config['DWH']['host']
dwh_user =config['DWH']['user']
dwh_password = config['DWH']['password']
dwh_database = config['DWH']['database']


#STEP1 : Create S3 Bucket(datalake)

create_bucket(access_key, secret_key, bucket_name, region)
print(bucket_name,region)

#Step2 : extract data from database(postgres) to datalake(S3)

conn =  create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/{db_database}')

#storing the database tables in a list 
db_tables = ['calldetails','calllog']

for table in db_tables :
    query = f'SELECT * FROM {table}'
    logging.info(f'============= Executing{query}')
    df = pd.read_sql_query(query,conn)#reading from the tables
    print('===success=====')
    print(query)

    df.to_csv(
        f's3://{bucket_name}/{table}.csv'
        ,index=False
        ,storage_options={
            'key':access_key
            ,'secret': secret_key
        }

    )


# #Step3 Load into initial schema

dwh_conn = redshift_connector.connect(
    host=dwh_host,
    database=dwh_database,
    user=dwh_user,
    password=dwh_password
 )
print('DWH connection Established!')
cursor=dwh_conn.cursor()

dev_schema ='dev'
staging_schema = 'staging'

#--- create dev schema
cursor.execute(f'''CREATE SCHEMA {dev_schema};''')
dwh_conn.commit()

#----create the tables
for query in dev_tables:
    print(f'=========  {query[:50]}')
    cursor.execute(query)
    dwh_conn.commit()

#--- copy tables from S3(datalake) to redshift(data warehouse)

for table in db_tables:
    cursor.execute(f'''
        COPY {dev_schema}.{table}
        FROM 's3://{bucket_name}/{table}.csv'
        IAM_ROLE '{role}'
        DELIMITER ','
        IGNOREHEADER 1;
    ''')
dwh_conn.commit()

#STEP4 : Create fact and dimensions


#...... create staging schema

cursor.execute(f'''CREATE SCHEMA {staging_schema};''')
dwh_conn.commit()

#...... create star schema tables(facts and dimensions)

for query in transformed_tables:
    print(f'=========  {query[:50]}')
    cursor.execute(query)
    dwh_conn.commit()

#......insert the data into facts and dimensions

for query in transformation_queries:
    print(f'=========  {query[:50]}')
    cursor.execute(query)
    dwh_conn.commit()





cursor.close()
dwh_conn.close()

