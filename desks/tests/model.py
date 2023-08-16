from django.test import TestCase
from desks.models import Desks

class TestAppModels(TestCase):

    def test_model_str(self):
        d_id = Desks.objects.create(d_id=123)
        name = Desks.objects.create(name="test_schreibtisch")
        client = Desks.objects.create(client="test_client")
        licence = Desks.objects.create(licence=False)
        active = Desks.objects.create(active=True)
        self.assertEqual(str(name), "test_schreibtisch")