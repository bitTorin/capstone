from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from django.conf import settings
import pandas as pd
import psycopg2
import io
from sodapy import Socrata
from sqlalchemy import create_engine


# app = city3d()

# @app.on_after_configure.connect
# @periodic_task(60)
def main():
    AUS_active_permits()
    AUS_closed_permits()


def AUS_active_permits():

    # Retrieve app token
    app_token = settings.APP_TOKEN

    # App token authentication
    client = Socrata("data.austintexas.gov", app_token)

    # Austin Construction Permits Dataset
    data_set = "3syk-w9eu"

    search_results = "permit_type_desc,permit_class_mapped,issue_date,issued_in_last_30_days,status_current,expiresdate,work_class,original_address1,original_city,original_state,original_zip,link,project_id,latitude,longitude"

    # Count number of active 'NEW' construction permits
    count = client.get(data_set, where="permittype='BP' AND status_current='Active' AND work_class='New'", select="COUNT(*)")

    # Find all active building permits for 'NEW' construction
    # Iterate over dataset thanks to https://holowczak.com/getting-started-with-nyc-opendata-and-the-socrata-api/5/
    start = 0
    chunk_size = 50000
    results = []
    while True:
        # First 50000 results, returned as JSON from API / converted to Python list of dictionaries by sodapy.
        results.extend(client.get(data_set, where="permittype='BP' AND status_current='Active' AND work_class='New'", select=search_results, offset=start, limit=chunk_size))
        # Shift query to next chunk
        start = start + chunk_size
        # If all records fetched, end loop
        if (start > int(count[0]['COUNT'])):
            break

    # Count number of active 'SHELL' construction permits
    count = client.get(data_set, where="permittype='BP' AND status_current='Active' AND work_class='Shell'", select="COUNT(*)")

    # Find all active building permits for 'Shell' construction
    # Iterate over dataset thanks to https://holowczak.com/getting-started-with-nyc-opendata-and-the-socrata-api/5/
    start = 0
    chunk_size = 50000
    while True:
        # First 50000 results, returned as JSON from API / converted to Python list of dictionaries by sodapy.
        results.extend(client.get(data_set, where="permittype='BP' AND status_current='Active' AND work_class='Shell'", select=search_results, offset=start, limit=chunk_size))
        # Shift query to next chunk
        start = start + chunk_size
        # If all records fetched, end loop
        if (start > int(count[0]['COUNT'])):
            break

    # Convert to pandas DataFrame
    df = pd.DataFrame.from_records(results)

    # print(df)

    # Retrieve database url
    database_url = settings.DATABASE_URL

    # Save to Postgres (faster than 'to_sql' https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table)
    engine = create_engine(database_url)

    df.head(0).to_sql('active_permits', engine, if_exists='replace', index=False)

    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    df.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, 'active_permits', null="") # null values become ''
    conn.commit()

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

if __name__ == "__main__":
    main()