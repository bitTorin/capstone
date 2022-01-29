from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from django.conf import settings
import pandas as pd
import psycopg2
import io
from sodapy import Socrata
from sqlalchemy import create_engine

# from .models import Permit
from .models import State


# app = city3d()

# @app.on_after_configure.connect
# @periodic_task(60)
def main():
    # AUS_active_permits()
    # AUS_closed_permits()

def AUS_active_permits():

    # Retrieve app token
    # app_token = settings.APP_TOKEN
    app_token = 'YoQv3uVAF8Q6UuI4ZzWRUO54Z'

    # App token authentication
    client = Socrata("data.austintexas.gov", app_token)

    # Austin Construction Permits Dataset
    data_set = "3syk-w9eu"

    search_results = "permittype,permit_number,permit_class_mapped,issue_date,issued_in_last_30_days,status_current,expiresdate,work_class,original_address1,original_city,original_state,original_zip,link,project_id,latitude,longitude,total_job_valuation"

    # Count number of active 'NEW' construction permits
    count = client.get(data_set, where="permittype='BP' AND status_current='Active' AND work_class='New' AND original_zip='78701'", select="COUNT(*)")

    # Find all active building permits for 'NEW' construction
    # Iterate over dataset thanks to https://holowczak.com/getting-started-with-nyc-opendata-and-the-socrata-api/5/
    start = 0
    chunk_size = 50000
    results = []
    while True:
        # First 50000 results, returned as JSON from API / converted to Python list of dictionaries by sodapy.
        results.extend(client.get(data_set, where="permittype='BP' AND status_current='Active' AND work_class='New' AND original_zip='78701'", select=search_results, offset=start, limit=chunk_size))
        # Shift query to next chunk
        start = start + chunk_size
        # If all records fetched, end loop
        if (start > int(count[0]['COUNT'])):
            break

    # Count number of active 'SHELL' construction permits
    count = client.get(data_set, where="permittype='BP' AND status_current='Active' AND work_class='Shell' AND original_zip='78701'", select="COUNT(*)")

    # Find all active building permits for 'Shell' construction
    # Iterate over dataset thanks to https://holowczak.com/getting-started-with-nyc-opendata-and-the-socrata-api/5/
    start = 0
    chunk_size = 50000
    while True:
        # First 50000 results, returned as JSON from API / converted to Python list of dictionaries by sodapy.
        results.extend(client.get(data_set, where="permittype='BP' AND status_current='Active' AND work_class='Shell' AND original_zip='78701'", select=search_results, offset=start, limit=chunk_size))
        # Shift query to next chunk
        start = start + chunk_size
        # If all records fetched, end loop
        if (start > int(count[0]['COUNT'])):
            break

    # Convert to pandas DataFrame
    df = pd.DataFrame.from_records(results)

    print(df)

    # engine = create_engine('sqlite:///db.sqlite3')
    #
    # df.to_sql(Permit._meta.db_table, if_exists='append' con=engine, index=True)
    #
    # df_records = df.to_dict('df')
    #
    # model_instances = [Permit(
    #     type=record['permittype'],
    #     city_permit_num=record['permit_number'],
    #     permit_class=record['permit_class_mapped'],
    #     issued_date=record['issue_date'],
    #     last30days=record['issued_in_last_30_days'],
    #     current_status=record['status_current'],
    #     expires_date=record['expiresdate'],
    #     address=record['original_address1'],
    #     zip_code=record['original_zip'],
    #     link=record['link'],
    #     city_project_id=record['project_id'],
    #     latitude=record['latitude'],
    #     longitude=record['longitude'],
    #     valutation=record['total_job_valuation'],
    # ) for record in df_records]
    #
    # Permit.objects.bulk_create(model_instances)

    # Retrieve database url
    database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(user='postgres', password='Austin2019', database_name='city3d')

    # Save to Postgres (faster than 'to_sql' https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table)
    engine = create_engine(database_url)

    df.to_sql(Permit._meta.db_table, if_exists='replace', con=engine,  index=True)

    # df.head(0).to_sql(Permit._meta.db_table, if_exists='replace', con=engine,  index=True)

    # conn = engine.raw_connection()
    # cur = conn.cursor()
    # output = io.StringIO()
    # df.to_csv(output, sep='\t', header=False, index=False)
    # output.seek(0)
    # contents = output.getvalue()
    # cur.copy_from(output, 'active_permits', null="") # null values become ''
    # conn.commit()

def AUS_closed_permits():

    # Retrieve app token
    app_token = settings.APP_TOKEN

    # App token authentication
    client = Socrata("data.austintexas.gov", app_token)

    # Austin Construction Permits Dataset
    data_set = "3syk-w9eu"

    search_results = "permit_type_desc,permit_class_mapped,issue_date,issued_in_last_30_days,status_current,expiresdate,work_class,original_address1,original_city,original_state,original_zip,link,project_id,latitude,longitude"

    #Count number of closed building permits for 'NEW' construction
    count = client.get(data_set, where="permittype='BP' AND status_current!='Active' AND work_class='New'", select="COUNT(*)")

    # Find all closed building permits for 'NEW' construction
    # Iterate over dataset thanks to https://holowczak.com/getting-started-with-nyc-opendata-and-the-socrata-api/5/
    start = 0
    chunk_size = 50000
    results = []
    while True:
        # First 50000 results, returned as JSON from API / converted to Python list of dictionaries by sodapy.
        results.extend(client.get(data_set, where="permittype='BP' AND status_current!='Active' AND work_class='New'", select=search_results, offset=start, limit=chunk_size))
        # Shift query to next chunk
        start = start + chunk_size
        # If all records fetched, end loop
        if (start > int(count[0]['COUNT'])):
            break


    #Count number of closed building permits for 'Shell' construction
    count = client.get(data_set, where="permittype='BP' AND status_current!='Active' AND work_class='Shell'", select="COUNT(*)")

    # Find all closed building permits for 'Shell' construction
    # Iterate over dataset thanks to https://holowczak.com/getting-started-with-nyc-opendata-and-the-socrata-api/5/
    start = 0
    chunk_size = 50000
    while True:
        # First 50000 results, returned as JSON from API / converted to Python list of dictionaries by sodapy.
        results.extend(client.get(data_set, where="permittype='BP' AND status_current!='Active' AND work_class='Shell'", select=search_results, offset=start, limit=chunk_size))
        # Shift query to next chunk
        start = start + chunk_size
        # If all records fetched, end loop
        if (start > int(count[0]['COUNT'])):
            break

    # Convert results list to pandas DataFrame
    df = pd.DataFrame.from_records(results)

    # print(df)

    # Retrieve database url
    database_url = settings.DATABASE_URL

    # Save to Postgres (faster than 'to_sql' https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table)
    engine = create_engine(database_url)

    df.head(0).to_sql('closed_permits', engine, if_exists='replace', index=False)

    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    df.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, 'closed_permits', null="") # null values become ''
    conn.commit()


def the_independent_test():

    # App token authentication
    client = Socrata("data.austintexas.gov",'YoQv3uVAF8Q6UuI4ZzWRUO54Z')

    # Austin Construction Permits Dataset
    data_set = "3syk-w9eu"

    #Count number of active permits
    count = client.get(data_set, where="latitude='30.26775294' AND longitude='-97.75093592'", select="COUNT(*)")

    # Find all closed building permits for new construction
    # Iterate over dataset thanks to https://holowczak.com/getting-started-with-nyc-opendata-and-the-socrata-api/5/
    start = 0
    chunk_size = 50000
    results = []
    while True:
        # First 50000 results, returned as JSON from API / converted to Python list of dictionaries by sodapy.
        results.extend(client.get(data_set, where="latitude='30.26775294' AND longitude='-97.75093592'", select="permit_type_desc,permit_class_mapped,issue_date,issued_in_last_30_days,status_current,expiresdate,work_class,original_address1,original_city,original_state,original_zip,link,project_id,latitude,longitude", offset=start, limit=chunk_size))
        # Shift query to next chunk
        start = start + chunk_size
        # If all records fetched, end loop
        if (start > int(count[0]['COUNT'])):
            break

    # Convert list to pandas DataFrame
    df = pd.DataFrame.from_records(results)

    print(df)

    # Retrieve database url
    database_url = 'postgresql://postgres:' + 'Austin2019' + '@localhost:5432/Buildings_Austin'

    # Save to Postgres (faster than 'to_sql' https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table)
    engine = create_engine(database_url)

    df.head(0).to_sql('the_independent', engine, if_exists='replace', index=False)

    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    df.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, 'the_independent', null="") # null values become ''
    conn.commit()

def the_republic():

    # App token authentication
    client = Socrata("data.austintexas.gov",'YoQv3uVAF8Q6UuI4ZzWRUO54Z')

    # Austin Construction Permits Dataset
    data_set = "3syk-w9eu"

    #Count number of active permits
    results = client.get(data_set, where="original_address='401 W 4TH ST'")

    # Convert list to pandas DataFrame
    df = pd.DataFrame.from_records(results)

    print(df)



if __name__ == "__main__":
    main()
