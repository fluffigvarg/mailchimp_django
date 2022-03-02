from base import BaseMailChimpClient


class MailChimpClient(BaseMailChimpClient):
    def _add_user(self, email, fname, lname, list_id=None, tags=None):
        if list_id or tags:
            print(
                f"User {fname} {lname}:{email} added to {list_id} with the tag(s) {tags}"
            )
        else:
            print(f"User {fname} {lname}:{email} added to CRM system!")
