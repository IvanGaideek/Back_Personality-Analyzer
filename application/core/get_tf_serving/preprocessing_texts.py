import re


def categorize_percentage(number):
    """Категоризация процентов по диапазонам и типам"""
    num = float(number)
    # Денежные диапазоны
    if num < 10:
        return '<procent_very_tiny>'
    elif num < 20:
        return '<procent_tiny>'
    elif num < 50:
        return '<procent_very_small>'
    elif num < 100:
        return '<procent_small>'
    elif num < 1000:
        return '<procent_medium>'
    else:
        return '<procent_large>'


def categorize_usd(number):
    """Категоризация для USD"""
    if number < 100:
        return '<money_small>'
    elif number < 2000:
        return '<money_medium>'
    elif number < 100000:
        return '<money_large>'
    else:
        return '<money_huge>'


def categorize_eur(number):
    """Категоризация для EUR"""
    if number < 100:
        return '<money_small>'
    elif number < 1500:
        return '<money_medium>'
    elif number < 50000:
        return '<money_large>'
    else:
        return '<money_huge>'


def categorize_gbp(number):
    """Категоризация для GBP"""
    if number < 75:
        return '<money_small>'
    elif number < 750:
        return '<money_medium>'
    elif number < 7500:
        return '<money_large>'
    else:
        return '<money_huge>'


def categorize_rub(number):
    """Категоризация для RUB"""
    if number < 5000:
        return '<money_small>'
    elif number < 200000:
        return '<money_medium>'
    elif number < 1000000:
        return '<money_large>'
    else:
        return '<money_huge>'


def categorize_phone(phone):
    """Категоризация телефонных номеров"""  # Удаляем все не цифры
    cleaned = re.sub(r'\D', '', phone)
    if len(cleaned) == 11:  # Полный номер с кодом страны
        return '<phone_full>'
    elif len(cleaned) == 10:  # Обычный номер
        return '<phone_standard>'
    else:
        return '<phone_other>'


def preprocess_text_fraud_detection(text):
    if not isinstance(text, str):
        return ""

    # Удаляем < и > перед обработкой
    text = text.replace('<', ' ').replace('>', ' ')
    text = text.lower()

    # Сохраняем оригинальный текст для обработки
    processed_text = text

    patterns = {
        # Денежные суммы с разными валютами
        'money_usd': r'(?:\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)|(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:usd|\$))',
        'money_eur': r'(?:(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:eur|€)|€\s*(\d+(?:,\d{3})*(?:\.\d{2})?))',
        'money_gbp': r'(?:£\s*(\d+(?:,\d{3})*(?:\.\d{2})?)|(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:gbp|£))',
        'money_rub': r'(?:₽\s*(\d+(?:,\d{3})*(?:\.\d{2})?)|(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:руб|rub|₽))',

        # Телефонные номера
        'phone': r'\b\+?[\d\-$$]{10,}\b',

        # Email адреса
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',

        # URL адреса
        # Разделяем URL на HTTP и HTTPS
        'url_secure': r'https://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*$$,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        'url_unsecure': r'http://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*$$,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',

        # Проценты
        'percentage': r'\b\d+(?:\.\d+)?%',

        # Даты
        'date': r'\b(?:\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4}|\d{4}[-/\.]\d{1,2}[-/\.]\d{1,2})\b'
    }
    moneys_tokenizers_func = {'money_usd': categorize_usd, 'money_eur': categorize_eur, 'money_gbp': categorize_gbp,
                              'money_rub': categorize_rub}
    # Обработка URL первой (чтобы избежать конфликтов с другими паттернами)
    # HTTPS URLs
    https_matches = re.finditer(patterns['url_secure'], processed_text)
    for match in https_matches:
        processed_text = processed_text.replace(match.group(0), ' <url_secure> ')

    # HTTP URLs
    http_matches = re.finditer(patterns['url_unsecure'], processed_text)
    for match in http_matches:
        processed_text = processed_text.replace(match.group(0), ' <url_unsecure> ')

    percentage_matches = re.finditer(patterns['percentage'], processed_text)
    for match in percentage_matches:
        try:
            full_match = match.group(0)
            number = int(match.group(1))
            number_category = categorize_percentage(number)
            processed_text = processed_text.replace(full_match, f' {number_category} <percentage>')
        except (ValueError, IndexError):
            continue

    # Замена оставшихся одиночных символов %
    processed_text = processed_text.replace('%', ' <percentage> ')
    # Замена паттернов специальными токенами
    for pattern_name, pattern in patterns.items():
        if pattern_name in ['percentage', 'url_secure', 'url_unsecure']:
            continue  # Пропускаем, так как уже обработали
        if pattern_name.startswith('money'):
            # Для денежных сумм используем категоризацию
            matches = re.finditer(pattern, processed_text)
            for match in matches:
                amount_str = next(group for group in match.groups() if group is not None)
                amount = float(re.sub(r'[^\d.]', '', amount_str))
                category = moneys_tokenizers_func[pattern_name](amount)
                processed_text = processed_text.replace(match.group(0), f' {category} ')

        elif pattern_name == 'phone':
            # Для телефонов используем специальную категоризацию
            matches = re.finditer(pattern, processed_text)
            for match in matches:
                category = categorize_phone(match.group(0))
                processed_text = processed_text.replace(match.group(0), f' {category} ')
        else:
            # Для остальных паттернов используем простую замену
            processed_text = re.sub(pattern, f' <{pattern_name}> ', processed_text)

    processed_text = re.sub(r'[^\w\s<>]', ' ', processed_text)  # Удаляем спецсимволы
    processed_text = re.sub(r'\s+', ' ', processed_text)  # Удаляем лишние пробелы
    processed_text = re.sub(r'Â', ' ', processed_text);
    processed_text = re.sub(r'&lt', ' ', processed_text)
    processed_text = re.sub(r'&gt', ' ', processed_text)

    return processed_text.strip()


def preprocess_text_fraud_mbti(examples):
    for num, el in enumerate(examples):
        el = el.lower()
        el = re.sub(r'http[s]?://[^ ]+|www\.[^ ]+', '', el)
        el = re.sub(r'\|\|\|', ' ', el)
        el = re.sub(r'!', ' exclamationpoint', el)
        examples[num] = re.sub(r"[,.!?;:'\"(){}$$<>_/\\@#$%^&*\-+=~`]", ' ', el)
