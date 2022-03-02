from urllib import response
from django.test import TestCase
from production import MailChimpClient
from mailchimp_marketing import Client
import os
from datetime import datetime
from string import ascii_lowercase
from random import choice

MAILCHIMP_TOKEN = os.environ.get("MAILCHIMP_KEY")
MAILCHIMP_SERVER = "us1"
MAILCHIMP_CONFIG = {
    "api_key": MAILCHIMP_TOKEN,
    "server": MAILCHIMP_SERVER,
}
MAILCHIMP_LIST_ID = os.environ.get("MAILCHIMP_LIST_ID")
mail_chimp_client = MailChimpClient()


class TestMailChimpIntegration(TestCase):
    def test_connection(self):
        mailchimp = Client()
        mailchimp.set_config(MAILCHIMP_CONFIG)
        response = mailchimp.ping.get()
        self.assertEqual(response["health_status"], "Everything's Chimpy!")

    def test_add_user(self):
        # generate a random username @asdf.com and compare against API call
        current_datetime = datetime.now()
        current_datetime_str = current_datetime.strftime("%Y%m%d%H%M%S")
        test_email = "test" + current_datetime_str + "@asdf.com"

        # expected result from API call
        expected_result = {
            "email_address": test_email,
            "status": "unsubscribed",
        }

        test_add_user = mail_chimp_client._add_user(
            test_email, "test", "TestFName", "TestLName", "unsubscribed"
        )

        self.assertEqual(
            expected_result["email_address"], test_add_user["email_address"]
        )

    def test_add_tags(self):
         # generate a random tag and compare against API call
        current_datetime = datetime.now()
        current_datetime_str = current_datetime.strftime("%Y%m%d%H%M%S")
        test_tag = "test_tag" + current_datetime_str

        # expected result from API call, null means success
        expected_result = {}
        test_add_tag = mail_chimp_client._add_tags(MAILCHIMP_LIST_ID, "test@asdf.com", test_tag)
        self.assertEqual(expected_result, test_add_tag)
