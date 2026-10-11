# сколько штук не хватает: плюс - недостача, минус - излишек, 0 - сошлось
def get_difference(expected, actual):
    return expected - actual


# сумма недостачи в рублях, если недостачи нет - 0
def get_shortage_cost(expected, actual, price):
    if actual >= expected:
        return 0.0
    return round(get_difference(expected, actual) * price, 2)


# возраст предмета в годах на дату проверки
def get_age_years(purchase_date, check_date):
    return round((check_date - purchase_date).days / 365, 1)


# нужна ли замена: предмет сломан или старше срока службы
def needs_replacement(age_years, service_life, is_working):
    return not is_working or age_years > service_life


# итог проверки предмета по разнице и признаку замены
def get_result(difference, replace):
    if difference > 0:
        return "недостача"
    elif difference < 0:
        return "излишек"
    elif replace:
        return "в наличии, требуется замена"
    else:
        return "в наличии"
