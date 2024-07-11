import json
import os
import pathlib
import random

import allure
import requests

from constants import HOST
from jsonschema import validate, Draft7Validator

from params.pet import schema_get_by_status, schema_get_by_id

method_get_by_status = "/api/v3/pet/findByStatus"
method_get_by_id_delete = "/api/v3/pet/{petID}"
method_add_edit = "/api/v3/pet"


class PetStep:
    @staticmethod
    @allure.step('Получение питомца по ID')
    def get_pet_by_id(pet_id, is_positive=True):
        dir_ = pathlib.Path(__file__).parent.parent.resolve()
        with open(os.path.join(dir_, 'schemas', 'pet.json'), encoding='utf-8') as fh:
            templates = json.load(fh)
        get_by_id = method_get_by_id_delete.replace("{petID}", str(pet_id))
        url = HOST + get_by_id
        with allure.step(f"Отправка get запроса с id питомца {pet_id}"):
            response = requests.get(url, headers={"accept": "application/json"})
        if is_positive:
            assert response.status_code == 200
            with allure.step(f"Проверка валидности ответа в соответствии со схемой"):
                validate(response.json(), templates)
            return response.json()
        else:
            return response

    @staticmethod
    @allure.step('Получение питомцев с определённым статусом')
    def get_pets_by_status(status):
        url = HOST + method_get_by_status
        with allure.step(f"Отправка get запроса со статусом {status}"):
            response = requests.get(url, params={"status": status}, headers={"accept": "application/json"})
            assert response.status_code == 200
        with allure.step(f"Проверка валидности ответа в соответствии со схемой"):
            validate(response.json(), schema_get_by_status)
        return response.json()

    @staticmethod
    @allure.step('Add a new pet to the store')
    def add_pet(category_id=1, category_name="Dogs", status='available', name=None, id_tags=None):
        if name is None:
            name = "Test" + str(random.randrange(100, 999))
        if id_tags is None:
            id_tags = random.randrange(100, 999)
        data = {
                  "id": random.randrange(100, 999),
                  "name": name,
                  "category": {
                    "id": category_id,
                    "name": category_name
                  },
                  "photoUrls": [
                    "string"
                  ],
                  "tags": [
                    {
                      "id": id_tags,
                      "name": "tag_name"+str(id_tags)
                    }
                  ],
                  "status": status
                }
        url = HOST + method_add_edit
        with allure.step(f"Отправка post запроса на добавление питомца"):
            response = requests.post(url, json=data, headers={"accept": "application/json"})
            assert response.status_code == 200
        return response.json(), data

    @staticmethod
    @allure.step('Update an existent pet in the store')
    def update_existent_pet(pet):
        url = HOST + method_add_edit
        pet_edit = pet.copy()
        pet_edit['name'] = "Тотошка"
        with allure.step(f"Отправка post запроса на добавление питомца"):
            response = requests.put(url, json=pet_edit, headers={"accept": "application/json"})
            assert response.status_code == 200
        return response.json()

    @staticmethod
    @allure.step('Delete a pets')
    def delete_pet(pet_id):
        method_delete = method_get_by_id_delete.replace("{petID}", str(pet_id))
        url = HOST + method_delete
        with allure.step(f"Отправка post запроса на добавление питомца"):
            response = requests.delete(url, headers={"accept": "application/json"})
            assert response.status_code == 200

    @staticmethod
    @allure.step('Проверка корректности добавления питомца')
    def assertion_add_pet(data_pet, add_pet):
        assert add_pet['name'] == data_pet['name']
        assert add_pet['status'] == data_pet['status']
        assert add_pet['tags'][0] == data_pet['tags'][0]


def test_1():
    address =   """  {
      "$id": "https://example.com/schemas/address",

      "type": "object",
      "properties": {
        "street_address": { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string" }
      },
      "required": ["street_address", "city", "state"],
      "additionalProperties": false
    }"""

    customer = """{
      "$id": "https://example.com/schemas/customer",
      "type": "object",
      "properties": {
        "first_name": { "type": "string" },
        "last_name": { "type": "string" },
        "shipping_address": { "$ref": "/schemas/address" },
        "billing_address": { "$ref": "/schemas/address" }
      },
      "required": ["first_name", "last_name", "shipping_address", "billing_address"],
      "additionalProperties": false
    }"""

    data =  """ {
      "first_name": "John",
      "last_name": "Doe",
      "shipping_address": {
        "street_address": "1600 Pennsylvania Avenue NW",
        "city": "Washington",
        "state": "DC"
      },
      "billing_address": {
        "street_address": "1st Street SE",
        "city": "Washington",
        "state": "DC"
      }
    }"""

    address_schema = json.loads(address)
    customer_schema = json.loads(customer)
    schema_store = {
        address_schema['$id']: address_schema,
        customer_schema['$id']: customer_schema,
    }

    from jsonschema import RefResolver
    resolver = RefResolver.from_schema(customer_schema, store=schema_store)
    validator = Draft7Validator(customer_schema, resolver=resolver)

    jsonData = json.loads(data)
    validator.validate(jsonData)

