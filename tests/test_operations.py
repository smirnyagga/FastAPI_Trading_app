from datetime import datetime

from httpx import AsyncClient
from conftest import client
from src.operations.schemas import OperationCreate


async def test_add_specific_operations(ac: AsyncClient):
    response = await ac.post("/operations", json={
      "id": 27,
      "quantity": "string",
      "figi": "string",
      "instrument_type": "string",
      "date": "2023-12-05T02:40:42.297",
      "type": "штраф"
    })
    assert response.status_code == 200, 'операция не добавлена'


async def test_get_specific_operations(ac: AsyncClient):
    response = await ac.get("/operations", params={
        "operation_type": "штраф",
    })
    assert response.status_code == 200
    # assert response.json()["status"] == "success"
    assert len(response.json()) == 1
