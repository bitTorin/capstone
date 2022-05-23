import pandas as pd
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine
from django.conf import settings
from sodapy import Socrata
import io
import os
from datetime import datetime, timedelta

from city3d.models import Permit

class Command(BaseCommand):

    def handle(self, *args, **options):

        # Retrieve app token
        app_token = settings.APP_TOKEN

        # App token authentication
        client = Socrata("data.sfgov.org", app_token)

        # Austin Construction Permits Dataset
        data_set = "i98e-djp9"

        search_results = "permit_type,permit_number,permit_type_definition,record_id,issued_date,status,permit_expiration_date,street_number,street_name,street_suffix,zipcode,location,estimated_cost"

        # Count number of issued 'new construction' building permits
        count = client.get(data_set, where="status='issued' AND permit_type='1'", select="COUNT(*)")

        # Find all issued 'new construction' building permits
        # Iterate over dataset thanks to https://holowczak.com/getting-started-with-nyc-opendata-and-the-socrata-api/5/
        start = 0
        chunk_size = 50000
        results = []
        while True:
            # First 50000 results, returned as JSON from API / converted to Python list of dictionaries by sodapy.
            results.extend(client.get(data_set, where="status='issued' AND permit_type='1'", select=search_results, offset=start, limit=chunk_size))
            # Shift query to next chunk
            start = start + chunk_size
            # If all records fetched, end loop
            if (start > int(count[0]['COUNT'])):
                break

        # Convert to pandas DataFrame
        df = pd.DataFrame.from_records(results)

        # Filter by issued dates in the last five years
        df["issued_date"] = pd.to_datetime(df["issued_date"])

        df = df[(df['issued_date'] > "2017-01-01")]

        # Match column names to Django Model
        df.rename({
            'permit_type_definition': 'permit_class',
            'record_id': 'project_id',
            'issued_date': 'issue_date',
            'status': 'current_status',
            'permit_expiration_date': 'expires_date',
            'street_number': 'address',
            'zipcode': 'zip',
            'estimated_cost': 'valuation'
            }, axis=1, inplace=True)

        # Reformat expires_date
        df["expires_date"] = pd.to_datetime(df["expires_date"])

        # Check if issue date is in last 30 days, add to dataframe
        dates = df['issue_date'].to_list()
        today = datetime.now()
        ref = today - timedelta(days=30)
        bools = []
        for date in dates:
            if today < ref:
                bools.append("Yes")
            else:
                bools.append("No")
        df.insert(5, "last_30_days", bools, True)

        # Re-format addresses
        # Convert int to string
        df['address'] = df['address'].astype(str)

        # Merge address attributes to new column
        df['address'] = df["address"].str.cat(df["street_name"],sep=" ").str.cat(df["street_suffix"],sep=" ")

        # Delete old address columns
        df = df.drop(['street_name', 'street_suffix'], axis=1)


        # Add city and state attributes to dataframe
        df.insert(9,"city", "San Francisco", True)
        df.insert(10,"state", "CA", True)


        # Add url links to dataframe
        # Manually create list of urls
        vals = df['permit_number'].tolist()
        urls = ["https://dbiweb02.sfgov.org/dbipts/default.aspx?page=Permit&PermitNumber=" + val for val in vals]

        # Add urls to dataframe for permit.link model class
        df.insert(12, "link", urls, True)

        #Split locations into latitude and longitude, save to two columns
        temp_df = (pd.DataFrame(df["location"].apply(pd.Series)))
        locations = []
        lats = []
        longs = []
        locations = temp_df["coordinates"].to_list()
        for i in locations:
            lat = i[1]
            lats.append(lat)

            long = i[0]
            longs.append(long)

        # Delete old location column
        df = df.drop('location', axis=1)

        df.insert(13, "latitude", lats, True)
        df.insert(14, "longitude", longs, True)

        # Remove additional permits at same location, permits will be found when visiting linked url
        df = df.drop_duplicates(subset=['latitude', 'longitude'], keep='last')

        # Database info
        database_name = settings.DATABASES['default']['NAME']
        database_url = 'sqlite:///{}'.format(database_name)

        # Save to Postgres (faster than 'to_sql' https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table)
        engine = create_engine(database_url)

        df.to_sql(Permit._meta.db_table, if_exists='append', con=engine,  index=False)

        # df.to_csv('sfo_permits.csv', sep='\t', index=False)
