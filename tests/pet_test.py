import random

import allure
import pytest

from steps.pet_step import PetStep


@pytest.mark.pet
@allure.title("Проверка получения доступных питомцев")
def test_get_available_pets():
    available_pets = PetStep.get_pets_by_status('available')
    # дальше я бы залезла в БД, посчитала в БД сколько питомцев в статусе доступности и сравнила ответы,
    # полученные от бэка и из БД


@pytest.mark.pet
@allure.title("Проверка добавления питомца")
def test_add_pet():
    data_add_pet, data = PetStep.add_pet()
    get_pet = PetStep.get_pet_by_id(data['id'])
    PetStep.assertion_add_pet(data, get_pet)
    PetStep.delete_pet(data['id'])


@pytest.mark.pet
@allure.title("Проверка изменения питомца")
def test_edit_pet():
    data_pet, data = PetStep.add_pet()
    PetStep.update_existent_pet(data)
    get_pet = PetStep.get_pet_by_id(data['id'])
    assert get_pet['name'] == "Тотошка"
    PetStep.delete_pet(data['id'])


def test_negative_get_pet_by_id():
    response = PetStep.get_pet_by_id(random.randrange(100000, 999999), is_positive=False)
    assert response.status_code == 404
    assert response.text == 'Pet not found'
