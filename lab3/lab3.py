def text_to_binary(text):
    binary_string = ""
    for char in text:
        binary_char = bin(ord(char))[2:]
        binary_char = binary_char.zfill(8)
        binary_string += binary_char
    return binary_string

def count_ones(binary_string):
    return binary_string.count('1')



filename = "input.txt"
output_filename = "output.txt"
total_ones = 0

with open(filename, 'r', encoding='utf-8') as file, open(output_filename, 'w', encoding='utf-8') as output_file:
    for line in file:
        line = line.rstrip()
        number = text_to_binary(line)
        ones_count = count_ones(number)
        total_ones += ones_count
        output_file.write(f"Строка:\n {line}\n")
        output_file.write(f"Двоичное представление: {number}\n")
        output_file.write(f"Сумма единиц: {ones_count}\n")
        if ones_count % 2 == 0: 
            output_file.write('Сумма единиц четная -> Y\n\n')
        else: 
            output_file.write('Сумма единиц нечетная -> N\n\n')
        # Также выводим на консоль
        print(f"Строка:\n {line}")
        print(f"Двоичное представление: {number}")
        print(f"Сумма единиц: {ones_count}")
        if ones_count % 2 == 0: 
            print('Сумма единиц четная -> Y\n')
        else: 
            print('Сумма единиц нечетная -> N\n')