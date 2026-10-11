def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Нужно ввести целое число")
