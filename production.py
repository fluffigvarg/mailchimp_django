from base import BaseMailChimpClient
from tasks import add_user_to_mailchimp, trigger_journey, add_or_remove_tags
import os
from hashlib import md5
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

UserModel = get_user_model()

MAILCHIMP_LIST_ID = os.environ.get("MAILCHIMP_LIST_ID")


class MailChimpClient(BaseMailChimpClient):
    def _add_user(self, email, tags, fname, lname, status="subscribed"):
        member_info = {
            "email_address": email,
            "status_if_new": status,
            "merge_fields": {"FNAME": fname, "LNAME": lname},
        }
        response = add_user_to_mailchimp.delay(MAILCHIMP_LIST_ID, email, member_info)
        return response
        if tags:
            self._add_tags(MAILCHIMP_LIST_ID, email, tags)

    def _event_trigger(self, email, journey_id, step_id):
        response = trigger_journey.delay(email, journey_id, step_id)
        return response

    def _add_tags(self, list_id, email, tags):
        hashed_email = self._convert_email_to_md5(email)
        response = add_or_remove_tags(MAILCHIMP_LIST_ID, hashed_email, tags)
        return response

    def _convert_email_to_md5(self, email):
        """Hashed email needed for some calls to MailChimp"""
        hash_object = md5(email.lower().encode())
        md5_hash = hash_object.hexdigest()
        return md5_hash


@receiver(post_save, sender=UserModel)
def new_user_signup(instance, **kwargs):
    """Automatically add new users to MailChimp"""
    email = instance.email
    first_name = instance.first_name
    last_name = instance.last_name
    tags = "new signup"
    mailchimp = MailChimpClient()
    mailchimp._add_user(email, tags, first_name, last_name)
