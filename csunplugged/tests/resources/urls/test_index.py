from tests.BaseTestWithDB import BaseTestWithDB
from django.urls import reverse


class IndexURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = "en"

    def test_valid_resources_index(self):
        url = reverse("resources:index")
        self.assertEqual(url, "/en/resources/")

        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
