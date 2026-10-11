def get_difference(expected, actual):
    return expected - actual

def get_shortage_cost(expected, actual, price):
    return get_difference(expected, actual) * price

def main():
    print("Сервис инвентаризации офисных помещений")
    room_name = '204'
    item_number = '1001'
    item_name = "Кресло офисное"
    expected = 12
    actual = 10
    price = 4500.50
    is_working = True
    print(f"Помещение: Кабинет {room_name}")
    print(f"Предмет: {item_name} (инв. номер {item_number})")
    print(f"По учету: {expected}, фактически: {actual}")
    print(f"Цена: {price} руб.")
    print(f"Исправен: {is_working}")

    difference = get_difference(expected, actual)
    print(f"Разница: {difference}")
    shortage_cost = get_shortage_cost(expected, actual, price)
    print(f"Сумма недостачи: {shortage_cost} руб.")
    

if __name__ == "__main__":
    main()


