import os
import pickle

class LZ78:
    def compress(self, input_string):
        dictionary = {}  # Словарь для хранения строк и их индексов
        current_string = ""  # Текущая строка, которая будет добавляться в словарь
        compressed_data = []  # Список для хранения сжатых данных
        dict_size = 1  # Начальный размер словаря

        # Проходим по каждому символу во входной строке
        for char in input_string:
            current_string += char 
            if current_string not in dictionary:
                dictionary[current_string] = dict_size 
                dict_size += 1 
                
                prefix_index = dictionary.get(current_string[:-1], 0)
                compressed_data.append((prefix_index, char))
                current_string = ""  

        if current_string:
            prefix_index = dictionary.get(current_string[:-1], 0)
            compressed_data.append((prefix_index, current_string[-1]))

        return compressed_data

   
    def decompress(self, compressed_data):
        dictionary = {}  # Словарь для хранения данных по индексам
        dict_size = 1  # Начальный размер словаря
        decompressed_string = ""  # Результат декомпрессии

        for prefix_index, char in compressed_data:
            if prefix_index == 0:
                entry = char
            else:
                entry = dictionary[prefix_index] + char  

            decompressed_string += entry  
            dictionary[dict_size] = entry  
            dict_size += 1 

        return decompressed_string

# функция для вычисления метрик сжатия
def calculate_compression_metrics(original, compressed, decompressed):
    original_size = len(original) * 8 
    compressed_size = sum(8 + 8 for _ in compressed)  
    decompressed_size = len(decompressed) * 8 

    compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0  

    return original_size, compressed_size, compression_ratio, decompressed_size

def write_compressed_data_to_file(compressed_data, filename):
    # Записываем сжатые данные (список кортежей) в бинарный файл
    with open(filename, 'wb') as file:
        pickle.dump(compressed_data, file)

def read_compressed_data_from_file(filename):
    # Читаем сжатые данные из бинарного файла
    with open(filename, 'rb') as file:
        return pickle.load(file)

def write_decompressed_data_to_file(decompressed_data, filename):
    # Записываем декомпрессированные данные в текстовый файл
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(decompressed_data)

def read_file(filename):
    # Читаем исходный файл как строку
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == "__main__":
    input_file_path = 'original_text.txt'
    compressed_file_path = 'lz78.link'

    input_string = read_file(input_file_path)
    

    lz78 = LZ78()

    compressed = lz78.compress(input_string)

    write_compressed_data_to_file(compressed, compressed_file_path)

    compressed_from_file = read_compressed_data_from_file(compressed_file_path)

    decompressed = lz78.decompress(compressed_from_file)

    original_size, compressed_size, compression_ratio, decompressed_size = calculate_compression_metrics(input_string, compressed, decompressed)
    print(f"Размер оригинала: {original_size} бит")
    print(f"Размер сжатого файла: {compressed_size} бит")
    print(f"Коэффициент сжатия: {compression_ratio:.2f}%")
    print(f"Размер после восстановления: {decompressed_size} бит")
