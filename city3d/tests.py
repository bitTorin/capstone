from django.test import TestCase
from django.conf import settings

from .tasks import AUS_active_permits, AUS_closed_permits

# Create your tests here.
class PermitTest(TestCase):
    def permitTest():
        app_token = settings.APP_TOKEN
        print(app_token)
        try:
            AUS_active_permits(app_token)

        except:
            print(f"test failed")
