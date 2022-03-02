from config import celery_app
import mailchimp_marketing as MailChimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import os

MAILCHIMP_TOKEN = os.environ.get("MAILCHIMP_KEY")
MAILCHIMP_SERVER = "us1"
MAILCHIMP_CONFIG = {
    "api_key": MAILCHIMP_TOKEN,
    "server": MAILCHIMP_SERVER,
}
mailchimp = MailChimpMarketing.Client()
mailchimp.set_config(MAILCHIMP_CONFIG)


@celery_app.task(
    bind=True, name="mail.crm.backends.mailchimp.tasks.add_user_to_mailchimp"
)
def add_user_to_mailchimp(self, list_id, email, member_info):
    try:
        # This will either add or update email on a list
        response = mailchimp.lists.set_list_member(list_id, email, member_info)
        print("response: {}".format(response))
        return response
    except ApiClientError as error:
        print("An exception occured: {}".format(error.text))
        return error


def add_or_remove_tags(list_id, hashed_email, tags):
    try:
        response = mailchimp.lists.update_list_member_tags(
            list_id, hashed_email, {tags}
        )
        print(response)
    except ApiClientError as error:
        print("Error: {}".format(error.text))


@celery_app.task(bind=True, name="mail.crm.backends.mailchimp.tasks.trigger_journey")
def trigger_journey(email, journey_id, step_id):
    try:
        response = mailchimp.customerJourneys.trigger(
            journey_id, step_id, {"email_address": email}
        )
        print(response)
        return response
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return error
