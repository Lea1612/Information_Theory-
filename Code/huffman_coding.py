import os
import heapq
from datetime import datetime
from struct import pack

from heap_node import HeapNode



class HuffmanCoding:
	def __init__(self, file_extension_encode, file_extension_decode):
		self.file_extension_encode = file_extension_encode
		self.file_extension_decode = file_extension_decode
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}

	def make_frequency_dict(self, text):
		frequency = {}
		for i in text:
			if i not in frequency:
				frequency[i] = 0
			frequency[i] += 1

		return frequency

	def make_heap(self, frequency):
		for key in frequency:
			node = HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node)

	def merge_nodes(self):
		while(len(self.heap) > 1):
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)

	def make_codes_helper(self, root, current_code):
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")

	def make_codes(self):
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)

	def get_encoded_text(self, text):
		encoded_text = []
		for character in text:
			encoded_text.append(self.codes[character])
		return ''.join(encoded_text)

	def pad_encoded_text(self, encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"

		padded_info = "{0:08b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text

	def get_byte_array(self, padded_encoded_text):
		if(len(padded_encoded_text) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
		return b

	def remove_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:]
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text

	def decode_text(self, encoded_text):
		current_code = ""
		decoded_text = []

		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]

				decoded_text.append(chr(character))
				current_code = ""

		return "".join(decoded_text)

	def encode(self, file_input_path, file_output_path):
		filename, file_extension = os.path.splitext(file_input_path)

		with open(file_input_path, 'rb') as file, open(file_output_path, 'wb') as output:
			print(datetime.now(), ": Start huffman")
			text = file.read()
			text = text.rstrip()
			print(datetime.now(), ": Create frequency")
			frequency = self.make_frequency_dict(text)
			self.make_heap(frequency)
			self.merge_nodes()
			self.make_codes()
			print(datetime.now(), ": Start encode")
			encoded_text = self.get_encoded_text(text)
			print(datetime.now(), ": Padding encoded")
			padded_encoded_text = self.pad_encoded_text(encoded_text)
			print(datetime.now(), ": Get byte array")
			b = self.get_byte_array(padded_encoded_text)
			print(datetime.now(), ": Write file")
			output.write(bytes(b))
			print(datetime.now(), ": Finish huffman")

	def decode(self, file_input_path, file_output_path):
		filename, file_extension = os.path.splitext(file_input_path)
		print(datetime.now(), ": Start decode huffman")
		with open(file_input_path, 'rb') as file, open(file_output_path, 'wb') as output:
			bit_lst = []
			print(datetime.now(), ": Read file")
			byte = file.read(1)
			while len(byte) > 0:
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_lst.append(bits)
				byte = file.read(1)
			bit_string = ''.join(bit_lst)
			print(datetime.now(), ": Remove padding")
			encoded_text = self.remove_padding(bit_string)
			print(datetime.now(), ": Decoding")
			decompressed_text = self.decode_text(encoded_text)

			print(datetime.now(), ": Writing decoded")
			for data in decompressed_text:
				output.write(pack('B', ord(data)))
			print(datetime.now(), ": Finish huffman")
