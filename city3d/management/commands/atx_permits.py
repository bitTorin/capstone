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

        search_results = "permittype,permit_number,permit_class_mapped,issue_date,issued_in_last_30_days,status_current,expiresdate,original_address1,original_city,original_state,original_zip,project_id,latitude,longitude,total_job_valuation"

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

        # Match column names to Django Model
        df.rename({
            'permittype': 'permit_type',
            'permit_class_mapped': 'permit_class',
            'issued_in_last_30_days': 'last_30_days',
            'status_current': 'current_status',
            'expiresdate': 'expires_date',
            'original_address1': 'address',
            'original_city': 'city',
            'original_state': 'state',
            'original_zip': 'zip',
            'total_job_valuation': 'valuation'
            }, axis=1, inplace=True)


        # Manually create list of urls
        vals = df['project_id'].tolist()
        urls = ["https://abc.austintexas.gov/web/permit/public-search-other?t_related-folder=1&t_selected_folderrsn=" + val for val in vals]

        # Add urls to dataframe for permit.link model class
        df.insert(13, "link", urls, True)

        # Convert to title case
        df['address'] = df['address'].str.title()
        df['city'] = df['city'].str.title()

        # Reformat expires_date
        df["issue_date"] = pd.to_datetime(df["issue_date"])

        # Reformat expires_date
        df["expires_date"] = pd.to_datetime(df["expires_date"])

        # Remove additional permits at same location, permits will be found when visiting linked url
        df = df.drop_duplicates(subset=['latitude', 'longitude'], keep='last')

        # Database info
        # database_name = settings.DATABASES['default']['NAME']
        # database_url = 'sqlite:///{}'.format(database_name)
        database_url = settings.DATABASES['default']

        # Save to database
        engine = create_engine(database_url)

        df.to_sql(Permit._meta.db_table, if_exists='append', con=engine,  index=False)

        # df.to_csv('atx_permits.csv', sep='\t', index=False)
