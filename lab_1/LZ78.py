import sys

class LZ78:
    def compress(self, input_string):
        dictionary = {}
        current_string = ""
        compressed_data = []
        dict_size = 1

        for char in input_string:
            current_string += char
            if current_string not in dictionary:
                dictionary[current_string] = dict_size
                dict_size += 1
                # Add the index of the prefix and the new character
                prefix_index = dictionary.get(current_string[:-1], 0)
                compressed_data.append((prefix_index, char))
                current_string = ""

        if current_string:
            prefix_index = dictionary.get(current_string[:-1], 0)
            compressed_data.append((prefix_index, current_string[-1]))

        return compressed_data

    def decompress(self, compressed_data):
        dictionary = {}
        dict_size = 1
        decompressed_string = ""

        for prefix_index, char in compressed_data:
            if prefix_index == 0:
                entry = char
            else:
                entry = dictionary[prefix_index] + char

            decompressed_string += entry
            dictionary[dict_size] = entry
            dict_size += 1

        return decompressed_string

# Utility function for size comparison
def calculate_compression_metrics(original, compressed, decompressed):
    original_size = len(original) * 8  # size in bits
    compressed_size = sum(8 + 8 for _ in compressed)  # prefix (8 bits) + char (8 bits) per entry
    decompressed_size = len(decompressed) * 8

    compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0

    return original_size, compressed_size, compression_ratio, decompressed_size

# Example usage
if __name__ == "__main__":
    input_file_path = 'original_text.txt'
    with open(input_file_path, 'r', encoding='utf-8') as file:
        input_string = file.read()
    lz78 = LZ78()

    compressed = lz78.compress(input_string)
    print("Compressed:", compressed)

    decompressed = lz78.decompress(compressed)
    print("Decompressed:", decompressed)

    # Calculate and display metrics
    original_size, compressed_size, compression_ratio, decompressed_size = calculate_compression_metrics(input_string, compressed, decompressed)
    print("\nCompression Metrics:")
    print(f"Original Size: {original_size} bits")
    print(f"Compressed Size: {compressed_size} bits")
    print(f"Compression Ratio: {compression_ratio:.2f}%")
    print(f"Decompressed Size: {decompressed_size} bits")

    # Ensure decompression correctness
    assert input_string == decompressed, "Decompressed data does not match the original!"
