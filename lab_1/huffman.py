from collections import defaultdict
import heapq
import math

# Класс узла дерева Хаффмана
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Построение дерева Хаффмана
def build_huffman_tree(text):
    # Подсчет частоты символов
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1

    # Создание кучи из узлов
    heap = [HuffmanNode(char, frequency) for char, frequency in freq.items()]
    heapq.heapify(heap)

    # Построение дерева
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

# Генерация кодов Хаффмана
def generate_codes(node, prefix='', codebook=None):
    if codebook is None:
        codebook = {}
    if node:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_codes(node.left, prefix + '0', codebook)
        generate_codes(node.right, prefix + '1', codebook)
    return codebook

def bitstring_to_bytes(s):  
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

# Кодирование текста
def encode(text, codebook):
    return ''.join(codebook[char] for char in text)



# Декодирование текста с записью в файл
def decode(encoded_text, root):
    decoded_text = []
    current_node = root
    byteString = bin(int.from_bytes(encoded_text, byteorder='big'))[2:]
    for bit in byteString:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded_text.append(current_node.char)
            current_node = root

    decoded_string = ''.join(decoded_text)
    
    return decoded_string


file = open('original_text.txt', 'rt')
original_text = file.read()
file.close()

# Построение дерева Хаффмана
root = build_huffman_tree(original_text)

# Генерация кодов
codebook = generate_codes(root)

# Кодирование текста
encoded_text = encode(original_text, codebook)

output_file = open('Huffman.link', 'wb')
output_file.write(bitstring_to_bytes(encoded_text))
output_file.close()

file = open('Huffman.link' , 'rb' )
data = file.read()
file.close()
# Декодирование текста с записью в файл
decoded_text = decode(file, root)

freq = defaultdict(int)
for char in original_text:
    freq[char] += 1

original_size = len(original_text.encode('utf-8'))  # Размер исходного текста в байтах

# Вычесляем энтропию
entropy = math.log2(len(codebook))
entropy2 = - sum([freq/original_size * math.log2(freq/original_size) for key , freq in freq.items()])
L = sum([freq[char]*len(codebook[char]) / original_size for char in freq.keys()])

compressed_size = len(encoded_text) / 8  # Размер закодированного текста в байтах (бит -> байт)
compression_ratio = entropy / L  # Коэффициент сжатия
efficiency_ratio = entropy2 / L # Коэффициент относительной эффективности
compression_percent = (1 - compressed_size / original_size) * 100  # Процент сжатия
restored_size = len(decoded_text.encode('utf-8'))  # Размер восстановленного текста в байтах

print(f"Начальный размер файла: {original_size} байт")
print(f"Размер после сжатия: {compressed_size:.2f} байт")
print(f"Коэффициент сжатия: {compression_ratio:.2f}")
print(f"Процент сжатия: {compression_percent:.2f}%")
print(f"Коэффициент относительной эффективности: {efficiency_ratio:.2f}")
print(f"Размер после восстановления: {restored_size} байт")

