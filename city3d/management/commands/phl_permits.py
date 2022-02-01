import pandas as pd
import json
import re
import requests
import time
import urllib
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine
from django.conf import settings
from datetime import datetime, timedelta

from city3d.models import Permit

class Command(BaseCommand):

    def handle(self, *args, **options):

        # Run json query in browser and save file to folder as 'phl_permits.json'
        # url = 'https://phl.carto.com/api/v2/sql?q=SELECT%20*%20FROM%20permits%20WHERE%20permittype%20LIKE%20%27BUILDING%27%20AND%20typeofwork=%27NEW%20CONSTRUCTION%27%20AND%20status=%27ISSUED%27'

        with open("phl_permits.json", 'r') as f:
            data = json.loads(f.read())

        df = pd.json_normalize(data, record_path=["rows"])

        # Delete unneeded columns
        df = df.drop(['cartodb_id', 'the_geom', 'the_geom_webmercator', 'objectid', 'addressobjectid', 'parcel_id_num', 'permitdescription', 'typeofwork', 'approvedscopeofwork', 'applicanttype', 'contractorname', 'contractoraddress1', 'contractoraddress2', 'contractorcity', 'contractorstate', 'contractorzip', 'mostrecentinsp', 'opa_account_num', 'unit_type', 'unit_num', 'censustract', 'council_district', 'opa_owner', 'systemofrecord', 'geocode_x', 'geocode_y'], axis=1)

        # Match column names to Django Model
        df.rename({
            'permittype': 'permit_type',
            'permitnumber': 'permit_number',
            'commercialorresidential': 'permit_class',
            'posse_jobid': 'project_id',
            'permitissuedate': 'issue_date',
            'permit_expiration_date': 'expires_date',
            'status': 'current_status'

            }, axis=1, inplace=True)

        print("Checkpoint 1: Success")

        # Format zipcodes to 5 int max
        zipcodes =[]
        zips = df['zip'].tolist()
        for zip in zips:
            try:
                new_zip = zip[0:5]
                zipcodes.append(new_zip)

            except:
                new_zip = 00000
                zipcodes.append(new_zip)

        df["zip"] = zipcodes

        print("Checkpoint 2: Success")

        # Webscrap permit page for expiration date and valuation
        expire_date =[]
        cost = []

        ids = df['project_id'].tolist()

        print("Checkpoint 2: Starting...")

        # Define counter variable
        j = 0

        for id in ids:

            j = j + 1

            expires_div = ('ExpirationDate_972087_' + id + '_sp')

            cost_div = ('TotalProjectValue_988772_' + id +'_sp')

            url = ('https://eclipse.phila.gov/phillylmsprod/pub/lms/Default.aspx?PossePresentation=Public&PosseObjectId=' + id)

            url_contents = urllib.request.urlopen(url).read()

            soup = BeautifulSoup(url_contents, 'html.parser')

            expires = soup.find("span", {"id": expires_div}).text
            expires = pd.to_datetime(expires)

            price = soup.find("span", {"id": cost_div}).text

            expire_date.append(expires)
            cost.append(price)


            print("Checkpoint 2: completing ", j, id)

        # Add cost to dataframe for permit.valuation model class
        df.insert(4, "expires_date", expire_date, True)
        df.insert(5, "valuation", cost, True)

        print("Checkpoint 3: Success")

        # Reformat date fields
        df["issue_date"] = pd.to_datetime(df["issue_date"])

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
        df.insert(4, "last_30_days", bools, True)

        df.zip = df.zip.str[:5]
        print(df.zip)

        # Add city and state attributes to dataframe
        df.insert(9,"city", "Philadelphia", True)
        df.insert(10,"state", "PA", True)

        # Add url links to dataframe
        # Manually create list of urls
        vals = df['project_id'].tolist()
        urls = ["https://eclipse.phila.gov/phillylmsprod/pub/lms/Default.aspx?PossePresentation=Public&PosseObjectId=" + val for val in vals]

        # Add urls to dataframe for permit.link model class
        df.insert(12, "link", urls, True)

        print("Checkpoint 4: Success")

        # Declare lsits for future
        delete_list = []
        latitude = []
        longitude = []

        # Map addresses to list
        addresses = df['address'].values.tolist()

        for i in range(len(addresses)):

            # Define base url
            url_2 = "https://api.mapbox.com/geocoding/v5/mapbox.places/"

            # Retrieve mapbox api token from settings
            api_token = settings.MAPBOX_API

            # when address not included, add entry to delete list
            if addresses[i] is None:
                delete_list.append(i)

            else:
                # Use regex to format addresses that list a range of house numbers (https://regex101.com/)
                # r'^(.)\S* selects all numbers until first space
                # r'^(.)\d* selects all digits at start of string until space or dash

                new_digits = re.search('^(.)\d*', addresses[i])
                addresses[i] = re.sub('^(.)\S*', new_digits[0], addresses[i])

                # Insert re-formatted address in search query
                query = str(addresses[i]) + ' PHILADELPHIA, PA' + ".json?access_token=" + api_token
                request_url = url_2 + query

                # Send API request to Mapbox, rate limit 600 per minute
                r = requests.get(url=request_url)
                data = r.json()

                # Save latitude and longitude values to list
                for x, item in enumerate(data["features"]):
                    if x == 0:
                        lat = item["center"][1]
                        latitude.append(lat)
                        long = item["center"][0]
                        longitude.append(long)

                print("Checkpoint 5: completing ", i)

            # Time delay to not overrun api server loads
            time.sleep(.1)


        # once complete, delete dataframe rows with no address field before adding lat, long columns !important order of operations
        for x in range(len(delete_list)):
            y = delete_list[x]
            df = df.drop(y)

        # Add latitude and longitude columns to dataframe
        df.insert(13,"latitude", latitude, True)
        df.insert(14,"longitude", longitude, True)

        print("Checkpoint 5: Success")

        df = df[["permit_type", "permit_number", "permit_class", "project_id", "issue_date", "last_30_days", "current_status", "expires_date", "address", "city", "state", "zip", "link", "latitude", "longitude", "valuation"]]

        # cols = []
        # cols = df.columns.to_list()
        # print(cols)

        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']

        # Retrieve database url
        database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(user=user, password=password, database_name=database_name)

        # Save to Postgres
        engine = create_engine(database_url)
        df.to_sql(Permit._meta.db_table, if_exists='append', con=engine,  index=True)

        print("Checkpoint 6: Success")
        print("Data Migration Successful")
