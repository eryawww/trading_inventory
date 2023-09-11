from django.test import TestCase, Client
from main.models import Item, TIME_ZONE

from datetime import datetime
import pytz

class ItemTestCase(TestCase):
    def setUp(self) -> None:
        Item.objects.create(
            name="BBCA", 
            amount=300, 
            buy_price=10_000, 
            time_buy=datetime.now(tz=TIME_ZONE),
            description='Fomo guys hehe'
        )
        Item.objects.create(
            name="ANTM", 
            amount=10, 
            buy_price=2_000, 
            time_buy=datetime.now(tz=TIME_ZONE),
            description='TESLA MAU MASUK INDO!'
        )
        # TODO: fetch database to test
    
    def test_item_attr(self):
        STRING_ATTR = ['name', 'description']
        FLOAT_ATTR = ['buy_price']
        INT_ATTR = ['amount']
        TIME_ATTR = ['time_buy']

        items = Item.objects.all()
        for item in items:
            for attr in STRING_ATTR:
                self.assertIsInstance(getattr(item, attr), str)
            for attr in INT_ATTR:
                self.assertIsInstance(getattr(item, attr), int)
            for attr in FLOAT_ATTR:
                self.assertIsInstance(getattr(item, attr), float)
            for attr in TIME_ATTR:
                self.assertIsInstance(getattr(item, attr), type(datetime.now()))
    
    def test_date_validation(self):
        items = Item.objects.all()
        for item in items:
            if item.time_buy.tzinfo != TIME_ZONE:
                self.assertLess(item.time_buy.replace(tzinfo=TIME_ZONE), datetime.now(tz=TIME_ZONE))
            else:
                self.assertLess(item.time_buy, datetime.now(tz=TIME_ZONE))

class ViewTestCase(TestCase):
    def test_routing_architecture(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)        