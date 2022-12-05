from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key,
                                            my_pets['pets'][0]['id'],
                                            name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом
        # об отсутствии своих питомцев
        raise Exception("There is no my pets")

###############################
#  TASK_19.7.2
# Ещё 10 вариантов тест-кейсов
###############################

# Test_1
def test_add_new_pet_no_photo_with_valid_data(name='Барсик', animal_type='дворокот',
                                              age='6'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name,
                                           animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] is ''

# Test_2
def test_add_pet_photo_valid_data(pet_photo='images/cat1.jpg'):
    # self, auth_key: json, pet_id: str, pet_photo: str
    """Проверяем возможность добавления/замены фото существующему питомцу"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_photo = os.path.join(os.path.dirname (__file__), pet_photo)

    # Если список пустой, то пробуем вначале добавлем нового питомца
    # и получаем список заново
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple (auth_key, "Барсик", "жук", "4")
        _, my_pets = pf.get_list_of_pets (auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на
    # добавление фотографии
    status, result = pf.add_pet_photo (auth_key,
                                       my_pets['pets'][0]['id'],
                                       pet_photo)
    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert 'pet_photo' in result

# Test_3
def test_add_new_pet_simple_invalid_age(name='JPMorgan',
                                           animal_type='cat',
                                           age='#@%$'):
    """Проверяем что можно добавить питомца без фото с
    некорректными данными - символы вместо чисел возраста"""

#     Получаем api key  и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

#     Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200

# Test_4
def test_add_new_pet_with_invalid_symbols(name='ASD#^', animal_type='$%DDdd',
                                  age='5', pet_photo='images/dog01.jpg'):
    """Проверяем что можно ли добавить питомца со спецсимволами в имени и типе"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type

# Test_5
def test_add_pet_with_empty_value_in_variable_name(name='', animal_type='cat',
                                                   age='2', pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавления питомца с пустым значением в переменной name"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == ''


def test_get_api_key_for_invalid_username(email=invalid_email, password=valid_password):
    """ Проверяем что запрос api ключа с несуществующим именем пользователя
     возвращает статус 403 и в результате содержится строка
     'This user wasn&#x27;t found in database'"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result

# Test_6
def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем что запрос api ключа с неправильным паролем возвращает статус 403
    и в результате содержится строка 'This user wasn&#x27;t found in database'"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result

# Test_7
def test_get_all_pets_with_invalid_key(filter=''):
    """Проверяем, что запрос всех питомцев с неверным api ключом возвращает код 403"""
    # Задаем неверный ключ api и сохраняем в переменную auth_key
    auth_key = {'key': '123'}
    # Запрашиваем список питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

# Test_8
def test_get_all_pets_with_incorrect_filter(filter='qwerty'):
    """ Проверяем что запрос питомцев c некорректным значением поля filter возвращает ошибку.
    Доступное значение параметра filter - 'my_pets' либо '' """

    # Получаем ключ auth_key и запрашиваем список питомцев с неправильным фильтром
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500
    assert 'Filter value is incorrect' in result


# Test_9
def test_get_my_pets_with_valid_key(filter='my_pets'):
    """ Проверяем что запрос своих питомцев возвращает не пустой список.
    Доступное значение параметра filter - 'my_pets' либо '' """

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter)

    # Проверяем - если список своих питомцев пуст, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, 'Барсик', 'Кот', '6')
        _, my_pets = pf.get_list_of_pets(auth_key, filter)

    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

# Test_10
