from Encruption import Encruption

if __name__ == '__main__':
    key = [input("Введите путь к исходному тексту: "), input("Введите путь к ключу: "), input("Введите путь к файлу с результатом: "), int(input("Введите режим (1 - Зашифрование, 2 - Расшшифрование): "))]
    Code = Encruption(key[0], key[1], key[2], key[3])