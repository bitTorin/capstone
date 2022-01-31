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

        expire_date =[]
        cost = []

        project_id = '278745881'

        expires_div = ('ExpirationDate_972087_' + project_id + '_sp')

        cost_div = ('TotalProjectValue_988772_' + project_id +'_sp')

        url = ('https://eclipse.phila.gov/phillylmsprod/pub/lms/Default.aspx?PossePresentation=Public&PosseObjectId=' + project_id)

        url_contents = urllib.request.urlopen(url).read()

        soup = BeautifulSoup(url_contents, 'html.parser')

        expires = soup.find("span", {"id": expires_div}).text
        expires = pd.to_datetime(expires)

        price = soup.find("span", {"id": cost_div}).text

        print(expires, price)
        expire_date.append(expires)
        cost.append(price)
