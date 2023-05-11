import pytest
from api import PetFriends
from settings import valid_email, valid_password, empty_email, empty_password, empty_auth_key, incorrect_auth_key
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Тест запроса api ключа на статус 200"""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert "key" in result


def test_get_all_pets_with_valid_key(filter=""):
    """ Тест на запрос списка всех питомцев"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result["pets"]) > 0


def test_add_new_pet_valid_data(name="Белка", animal_type="Белка", age="1", pet_photo="images/squirrel.jpg"):
    """ Тест на добавление питомца с корректными данными """

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result["name"] == name


def test_delete_pet():
    """ Тест на удаления ранее добавленного своего питомца """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "Рэй", "Собака", "8", "images/Ray.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets["pets"][0]["id"]
    status = pf.delete_pet(auth_key, pet_id)

    assert status == 200
    assert pet_id not in my_pets.values()

def test_update_pet_info(name="Мася", animal_type="коха", age="1"):
    """ Тест возможности обновления информации о своем питомце """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets["pets"][0]["id"], name, animal_type, age)

        assert status == 200
        assert result["name"] == name
    else:
        raise Exception("No pets")


def test_add_new_pet_without_photo_valid_data(name="Собака", animal_type="пес", age="2"):
    """ Тест на добавления питомца без фото с корректными данными """

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result["name"] == name


def test_get_api_key_for_data_user_empty(email=empty_email, password=empty_password):
    """ Тест запроса api ключа c пустыми значениями логина и пароля на статус 403"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert "key" not in result


def test_get_api_key_for_password_user_empty(email=valid_email, password=empty_password):
    """ Тест запроса api ключа c валидным значением логина и пустым значением пароля на статус 403"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert "key" not in result


def test_get_all_pets_with_empty_key(filter=""):
    """ Тест запроса всех питомцев c пустым значением api ключа на статус 403 """

    status, result = pf.get_list_of_pets(empty_auth_key, filter)

    assert status == 403


def test_get_all_pets_with_incorrect_key(filter=""):
    """ Тест запроса всех питомцев c некорректным значением api ключа на возврат статуса 403 """

    status, result = pf.get_list_of_pets(incorrect_auth_key, filter)

    assert status == 403


def test_add_new_pet_empty_data(name="", animal_type="", age="", pet_photo="images/Rona.jpg"):
    """ Негативный тест на возможность добавить питомца с фото и незаполненными данными """

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result["name"] == name


def test_delete_not_your_pet(name="BIM", animal_type="Dog", age="2"):
    """ Негативный тест на возможность удаления не своего питомца """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    if len(all_pets["pets"]) > 0:
        pet_id = all_pets["pets"][0]["id"]
        status = pf.delete_pet(auth_key, pet_id)

        assert status == 200
        assert pet_id not in all_pets.values()
    else:
        raise Exception("No pets")