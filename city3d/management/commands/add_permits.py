import pandas as pd
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine
from django.conf import settings
from sodapy import Socrata
import io

from city3d.models import Permit

class Command(BaseCommand):

    def handle(self, *args, **options):

        # Retrieve app token
        app_token = settings.APP_TOKEN

        # App token authentication
        client = Socrata("data.austintexas.gov", app_token)

        # Austin Construction Permits Dataset
        data_set = "3syk-w9eu"

        search_results = "permittype,permit_number,permit_class_mapped,issue_date,issued_in_last_30_days,status_current,expiresdate,original_address1,original_city,original_state,original_zip,link,project_id,latitude,longitude,total_job_valuation"

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

        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']

        # Retrieve database url
        database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(user=user, password=password, database_name=database_name)

        # Save to Postgres (faster than 'to_sql' https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table)
        engine = create_engine(database_url)

        df.to_sql(Permit._meta.db_table, if_exists='replace', con=engine,  index=False)
        # df.head(0).to_sql('active_permits', if_exists='replace', con=engine,  index=False)
        #
        # conn = engine.raw_connection()
        # cur = conn.cursor()
        # output = io.StringIO()
        # df.to_csv(output, sep='\t', header=False, index=False)
        # output.seek(0)
        # contents = output.getvalue()
        # cur.copy_from(output, 'active_permits', null="") # null values become ''
        # conn.commit()