import unittest
import logging
import requests
from pydantic import BaseModel
import config

FAVORITE_DELETED_MESSAGE = {"message": "Item successfully deleted"}
FAVORITE_NOT_FOUND_MESSAGE = {"detail": "Item not found"}

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

ENTRYPOINT = cfg.FAVORITE_SERVICE_ENTRYPOINT


class FavoriteItem(BaseModel):
    id: int
    name: str
    description: str
    product_id: int

favorite_items = [
    {
        "id": "1",
        "name": "Imya1",
        "description": "Opisanie1",
        "product_id": "1",
    },
    {
        "id": "2",
        "name": "Imya2",
        "description": "Opisanie2",
        "product_id": "2",
    },
]

class TestCase(unittest.TestCase):
    def _create_favorite_item(self, payload: FavoriteItem) -> FavoriteItem:
        response = requests.post(f"{ENTRYPOINT}favorites", json=payload.dict())
        self.assertEqual(response.status_code, 201)
        return FavoriteItem(**response.json())

    def _update_favorite_item(self, favorite_id, payload: FavoriteItem) -> FavoriteItem:
        response = requests.put(f"{ENTRYPOINT}favorites/{favorite_id}", json=payload.dict())
        self.assertEqual(response.status_code, 200)
        return FavoriteItem(**response.json())

    def _delete_favorite_item(self, favorite_id) -> requests.Response:
        response = requests.delete(f"{ENTRYPOINT}favorites/{favorite_id}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), FAVORITE_DELETED_MESSAGE)
        return response

    def test_service_availability(self):
        response = requests.get(ENTRYPOINT + "testing")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, FAVORITE_NOT_FOUND_MESSAGE)

    def test_get_favorite_items(self, limit=10, offset=0):
        payload = {
            "limit": limit,
            "offset": offset
        }
        response = requests.get(f"{ENTRYPOINT}favorites", params=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_add_favorite_item(self):
        payload = FavoriteItem(id=1, name="Imya1", description="Opisanie1", product_id=101)
        data = self._create_favorite_item(payload)
        try:
            self.assertIsInstance(data, FavoriteItem)
            self.assertEqual(data, payload)
        except requests.exceptions.HTTPError as exc:
            logger.error(exc.response.text)
            logger.error(exc)
        finally:
            self._delete_favorite_item(data.id)

    def test_update_favorite_item(self):
        payload = FavoriteItem(id=1, name="Imya1", description="Opisanie1", product_id=101)
        data = self._create_favorite_item(payload)
        try:
            updated_payload = FavoriteItem(id=1, name="Novoe_Imya1", description="Novoe_opisanie1", product_id=102)
            data = self._update_favorite_item(data.id, updated_payload)
            self.assertIsInstance(data, FavoriteItem)
            self.assertEqual(data, updated_payload)
        finally:
            self._delete_favorite_item(data.id)


if __name__ == "__main__":
    unittest.main()