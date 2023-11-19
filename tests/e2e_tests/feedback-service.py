import unittest
import logging
import requests
from pydantic import BaseModel
from typing import Optional
import config

FEEDBACK_DELETED_MESSAGE = {"message": "Deleted"}
FEEDBACK_NOT_FOUND_MESSAGE = {"detail": "Not Found"}

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-9s | %(message)s"
)

cfg: config.Config = config.load_config()

logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.json()}'
)

ENTRYPOINT = cfg.FEEDBACK_SERVICE_ENTRYPOINT


class Feedback(BaseModel):
    title: str
    description: str
    id: str


class FeedbackCreate(BaseModel):
    title: str
    description: str


class FeedbackUpdate(BaseModel):
    title: str
    description: str


class TestCase(unittest.TestCase):
    def _create_feedback(self, payload: FeedbackCreate) -> Feedback:
        response = requests.post(f"{ENTRYPOINT}feedbacks", json=payload.dict())
        self.assertEqual(response.status_code, 200)
        return Feedback(**response.json())

    def _update_feedback(self, feedback_id: str, payload: FeedbackUpdate) -> Feedback:
        response = requests.put(f"{ENTRYPOINT}feedbacks/{feedback_id}", json=payload.dict())
        self.assertEqual(response.status_code, 200)
        return Feedback(**response.json())

    def _delete_feedback(self, feedback_id: str) -> requests.Response:
        response = requests.delete(f"{ENTRYPOINT}feedbacks/{feedback_id}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), FEEDBACK_DELETED_MESSAGE)
        return response

    def test_service_availability(self):
        response = requests.get(ENTRYPOINT + "tests")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, FEEDBACK_NOT_FOUND_MESSAGE)

    def test_get_feedbacks(self, skip=0, limit=10):
        response = requests.get(f"{ENTRYPOINT}feedbacks?skip={skip}&limit={limit}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_add_feedback(self):
        payload = FeedbackCreate(title="Test Feedback", description="This is a test feedback.")
        data = self._create_feedback(payload)
        try:
            self.assertIsInstance(data, Feedback)
            self.assertEqual(data.title, payload.title)
            self.assertEqual(data.description, payload.description)
        except requests.exceptions.HTTPError as exc:
            logger.error(exc.response.text)
            logger.error(exc)
        finally:
            self._delete_feedback(data.id)

    def test_update_feedback(self):
        create_payload = FeedbackCreate(title="Test Feedback", description="This is a test feedback.")
        data = self._create_feedback(create_payload)
        try:
            update_payload = FeedbackUpdate(title="Updated Feedback", description="This feedback has been updated.")
            data = self._update_feedback(data.id, update_payload)
            self.assertIsInstance(data, Feedback)
            self.assertEqual(data.title, update_payload.title)
            self.assertEqual(data.description, update_payload.description)
        finally:
            self._delete_feedback(data.id)


if __name__ == '__main__':
    unittest.main()