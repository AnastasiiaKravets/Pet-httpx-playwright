import random

import pytest
from faker import Faker

from API.API_Client import API_Client
from API.PetModels import PetCreateModelRequest, PetCreateModelResponse, PetStatus, PetErrorResponse


@pytest.fixture(scope="module")
def api_client():
    with API_Client() as client:
        yield client

@pytest.fixture(scope="function")
def created_pet(api_client):
    _fake = Faker()
    pet = {
        "id": random.randint(1, 100),
        "name": _fake.name(),
        "photoUrls": [_fake.image_url()],
        "status": PetStatus.AVAILABLE.value
    }
    print(pet)
    api_client.post("pet", json=pet)
    return PetCreateModelRequest(**pet)


class TestAPI:
    @pytest.mark.api
    def test_create_pet(self, api_client):
        payload = PetCreateModelRequest(id=1, name="Doggie")
        print(payload.model_dump_json())

        result = api_client.post("pet", json=payload.model_dump())
        assert result.status_code == 200

        created_pet = PetCreateModelResponse.model_validate(result.json())
        assert created_pet.id == payload.id, "wrong created id"
        assert created_pet.name == payload.name, "wrong created name"
        assert created_pet.status == payload.status, "wrong created status"
        assert not created_pet.photoUrls, "Photo urls should be empty"
        assert not created_pet.tags, "Tags should be empty"

    @pytest.mark.api
    def test_get_pet(self, created_pet: PetCreateModelRequest, api_client):
        result = api_client.get(f"pet/{created_pet.id}")
        assert result.status_code == 200

        pet = PetCreateModelResponse.model_validate(result.json())
        assert pet.id == created_pet.id, "wrong created id"
        assert pet.name == created_pet.name, "wrong created name"
        assert pet.status == created_pet.status, "wrong created status"
        assert pet.photoUrls == created_pet.photoUrls, "Photo urls should be empty"
        assert pet.tags == created_pet.tags, "Tags should be empty"

    @pytest.mark.api
    def test_update_pet(self, created_pet: PetCreateModelRequest, api_client):
        updated_pet = created_pet
        updated_pet.name = created_pet.name + "_Updated"

        result = api_client.put("pet", json=updated_pet.model_dump())
        assert result.status_code == 200

        pet = PetCreateModelResponse.model_validate(result.json())
        assert pet.id == updated_pet.id, "wrong created id"
        assert pet.name == updated_pet.name, "wrong created name"
        assert pet.status == updated_pet.status, "wrong created status"
        assert pet.photoUrls == updated_pet.photoUrls, "Photo urls should be empty"
        assert pet.tags == updated_pet.tags, "Tags should be empty"

    @pytest.mark.api
    def test_delete_pet(self, created_pet: PetCreateModelRequest, api_client):
        result = api_client.delete(f"pet/{created_pet.id}")
        assert result.status_code == 200

        get_result = api_client.get(f"pet/{created_pet.id}")
        assert get_result.status_code == 404
        PetErrorResponse.model_validate(get_result.json())


    @pytest.mark.api
    @pytest.mark.parametrize("status", [pet_status.value for pet_status in PetStatus])
    def test_get_pet_by_status(self, api_client, status: PetStatus):
        result = api_client.get("/pet/findByStatus", params={"status": status})
        assert result.status_code == 200
        for pet_item in result.json():
            assert pet_item["status"] == status, f"Pet id {pet_item['id']}"
