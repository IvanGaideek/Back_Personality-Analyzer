from phonenumbers import geocoder, carrier
import phonenumbers
import re


def get_information_about_phone(text) -> dict:
    phone = get_num_phone(text)
    if not phone:
        return {'phone': None, 'country': None, 'carrier': None, 'message': 'not found'}
    try:
        obj_analyze_phone = phonenumbers.parse(phone, None)
        valid = phonenumbers.is_valid_number(obj_analyze_phone)
        if not valid:
            return {'phone': phone, 'country': None, 'carrier': None, 'message': 'not existing'}
        carrier_v = carrier.name_for_number(obj_analyze_phone, "en")  # оператор
        region_v = geocoder.country_name_for_number(obj_analyze_phone, "en") + ', ' +\
                   geocoder.description_for_number(obj_analyze_phone, "en")  # страна + город
        return {'phone': phone, 'country': region_v, 'carrier': carrier_v, 'message': 'success'}
    except Exception:
        return {'phone': phone, 'country': None, 'carrier': None, 'message': 'error'}


def get_num_phone(text):
    pattern_phone = re.compile(r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{2,4})(?:[-.x ]*(\d+))?\b', re.VERBOSE)
    match = pattern_phone.search(text)
    if not match:
        return None  # Номер не найден
    # Получаем найденный номер
    raw_phone_number = match.group(0)

    # Удаляем лишние символы и пробелы
    digits = re.sub(r'\D', '', raw_phone_number)
    # Преобразуем в формат +7(XXX)YYY-ZZ-NN
    if len(digits) == 11 and (digits.startswith('7') or digits.startswith('8')):
        formatted_number = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    elif len(digits) == 10:  # Если номер без кода страны
        formatted_number = f"+7({digits[0:3]}){digits[3:6]}-{digits[6:8]}-{digits[8:10]}"
    else:
        return None  # Если номер не подходит по формату

    return formatted_number
