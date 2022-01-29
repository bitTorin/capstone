import pandas as pd
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine
from django.conf import settings

from city3d.models import State

class Command(BaseCommand):

    def handle(self, *args, **options):

        excel_file = 'state_list.xlsx'
        df = pd.read_excel(excel_file)

        print(df)

        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']

        # Retrieve database url
        database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(user=user, password=password, database_name=database_name)

        engine = create_engine(database_url, echo=False)

        df.to_sql(State._meta.db_table, if_exists='replace', con=engine,  index=True)
