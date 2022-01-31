import pandas as pd
import json
import requests
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
        url = 'https://phl.carto.com/api/v2/sql?q=SELECT%20*%20FROM%20permits%20WHERE%20permittype%20LIKE%20%27BUILDING%27%20AND%20typeofwork=%27NEW%20CONSTRUCTION%27%20AND%20status=%27ISSUED%27'

        with open("phl_permits.json", 'r') as f:
            data = json.loads(f.read())

        df = pd.json_normalize(data, record_path=["rows"])

        # Delete unneeded columns
        df = df.drop(['cartodb_id', 'the_geom', 'the_geom_webmercator', 'objectid', 'parcel_id_num', 'permitdescription', 'typeofwork', 'approvedscopeofwork', 'applicanttype', 'contractorname', 'contractoraddress1', 'contractoraddress2', 'contractorcity', 'contractorstate', 'contractorzip', 'mostrecentinsp', 'opa_account_num', 'unit_type', 'unit_num', 'censustract', 'council_district', 'opa_owner', 'systemofrecord'], axis=1)

        # Match column names to Django Model
        df.rename({
            'permittype': 'permit_type',
            'permitnumber': 'permit_number',
            'commercialorresidential': 'permit_class',
            'posse_jobid': 'project_id',
            'permitissuedate': 'issue_date',
            'addressobjectid': 'address',
            'permit_expiration_date': 'expires_date',
            'status': 'current_status'

            }, axis=1, inplace=True)

        # Webscrap permit page for expiration date and valuation
        expire_date =[]
        cost = []

        ids = df['project_id'].tolist()

        for id in ids:

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

        # Add cost to dataframe for permit.valuation model class
        df.insert(4, "expires_date", expire_date, True)
        df.insert(5, "valuation", cost, True)


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

        # https://api.mapbox.com/search/v1/forward/{search_text}
        # #Split locations into latitude and longitude, save to two columns
        # temp_df = (pd.DataFrame(df["location"].apply(pd.Series)))
        # locations = []
        # lats = []
        # longs = []
        # locations = temp_df["coordinates"].to_list()
        # for i in locations:
        #     lat = i[1]
        #     lats.append(lat)
        #
        #     long = i[0]
        #     longs.append(long)
        #
        # # Delete old location column
        # df = df.drop('location', axis=1)
        #
        # df.insert(13, "latitude", lats, True)
        # df.insert(14, "longitude", longs, True)
        #
        # print(df)

        df = df[["permit_type", "permit_number", "permit_class", "project_id", "issue_date", "last_30_days", "current_status", "expires_date", "address", "city", "state", "zip", "link", "geocode_x", "geocode_y", "valuation"]]

        cols = []
        cols = df.columns.to_list()
        print(cols)
        #
        # user = settings.DATABASES['default']['USER']
        # password = settings.DATABASES['default']['PASSWORD']
        # database_name = settings.DATABASES['default']['NAME']
        #
        # # Retrieve database url
        # database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(user=user, password=password, database_name=database_name)
        #
        # # Save to Postgres (faster than 'to_sql' https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table)
        # engine = create_engine(database_url)
        #
        # df.to_sql(Permit._meta.db_table, if_exists='append', con=engine,  index=True)
