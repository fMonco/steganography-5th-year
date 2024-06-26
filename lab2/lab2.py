def mtk2_encode(text):
    # Таблица соответствия символов и их кодов в МТК2

    mtk2_table = {
        'А': "00011", 'Б': "11001", 'Ц': "01110", 'Д': "01001", 'Е': "00001", 'Ф': "01101", 'Г': "11010", 'Х': "10100",
        'И': "00110", 'Й': "01011", 'К': "01111", 'Л': "10010", 'М': "11100", 'Н': "01100", 'О': "11000", 'П': "10110",
        'Я': "10111", 'Р': "01010", 'С': "00101", 'Т': "10000", 'У': "00111", 'Ж': "11110", 'В': "10011", 'Ь': "11101",
        'Ы': "10101", 'З': "10001", '1': "11111", '2': "11110", '3': "11101", '4': "11100", '5': "11011", '6': "11010",
        '7': "11001", '8': "11000", '9': "10111", '0': "10110", ' ': "00100"
    }
    encoded_text = ""
    for char in text.upper():
        if char in mtk2_table:
            encoded_text += mtk2_table[char] + ""
        else:

            pass

    return encoded_text.strip()

# Пример использования
text = "Человек рожден для труда"
encoded_text = mtk2_encode(text)
print(encoded_text)
