import json

from datastore.tests_base import DataStoreTestCaseBase

class FormListTestCase(DataStoreTestCaseBase):
    def setUp(self):
        super().setUp()
        self.url = "/api/store/forms/"

    def test_get(self):
        response = self.client.get(
            self.url,
        )
        self.assertEqual(
            response.status_code,
            200
        )

    def test_post_missing_required_fields(self):
        # case-1: missing name
        response = self.client.post(
            self.url,
            json.dumps(
                {
                    # "name": self.create_random_text(),
                    "user_uid": "invalid-value",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(
            str(response.data.get('name')[0]),
            'This field is required.'
        )
        self.assertEqual(
            response.status_code,
            400
        )

        # case-2 missing user_uid
        user_uid = self.create_random_uid()
        response = self.client.post(
            self.url,
            json.dumps(
                {
                    "name": self.create_random_text(),
                    # "user_uid": user_uid,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(
            str(response.data.get('user_uid')[0]),
            'This field is required.'
        )
        self.assertEqual(
            response.status_code,
            400
        )

    def test_post_invalid_data(self):
        # case-1: invalid user_uid
        response = self.client.post(
            self.url,
            json.dumps(
                {
                    "name": self.create_random_text(),
                    "user_uid": "invalid-value",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(
            str(response.data.get('user_uid')[0]),
            '“invalid-value” is not a valid UUID.'
        )
        self.assertEqual(
            response.status_code,
            400
        )

        # case-2 user doesn't exists
        user_uid = self.create_random_uid()
        response = self.client.post(
            self.url,
            json.dumps(
                {
                    "name": self.create_random_text(),
                    "user_uid": user_uid,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(
            str(response.data.get('user_uid')[0]),
            f"Object with uid={user_uid} does not exist."
        )
        self.assertEqual(
            response.status_code,
            400
        )

    def test_post_successful(self):
        user_uid = str(self.create_user().uid)
        response = self.client.post(
            self.url,
            json.dumps(
                {
                    "name": self.create_random_text(),
                    "user_uid": user_uid,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(
            response.status_code,
            201
        )
