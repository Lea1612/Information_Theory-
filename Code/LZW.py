from datetime import datetime
from struct import *
import struct


class LZWAlgorithm(object):

    def __init__(self, file_extension_encode, file_extension_decode):
        self.file_extension_encode = file_extension_encode
        self.file_extension_decode = file_extension_decode

    def encode(self, file_input_path, file_output_path):
        # taking the input file and the number of bits from command line
        # defining the maximum table size
        # opening the input file
        # reading the input file and storing the file data into data variable
        print(datetime.now(), ": Start encode LZW")
        n = 16
        maximum_table_size = pow(2, int(n))-1
        file = open(file_input_path)
        data = file.read()

        # Building and initializing the dictionary.
        dictionary_size = 256
        dictionary = {chr(i): i for i in range(dictionary_size)}
        string = ""             # String is null.
        compressed_data = []    # variable to store the compressed data.

        # iterating through the input symbols.
        # LZW Compression algorithm
        print(datetime.now(), ": Encode")
        for symbol in data:
            string_plus_symbol = string + symbol  # get input symbol.
            if string_plus_symbol in dictionary:
                string = string_plus_symbol
            else:
                compressed_data.append(str(dictionary[string]))
                if(len(dictionary) <= maximum_table_size):
                    dictionary[string_plus_symbol] = dictionary_size
                    dictionary_size += 1
                string = symbol

        if string in dictionary:
            compressed_data.append(str(dictionary[string]))

        # storing the compressed string into a file (byte-wise).
        out = file_output_path
        output_file = open(out, "wb")
        print(datetime.now(), ": Start writing encoded text")
        for data in compressed_data:
            output_file.write(pack('>H', int(data)))


        output_file.close()
        file.close()
        print(datetime.now(), ": Finish encode LZW")

    def decode(self, file_input_path, file_output_path):
        print(datetime.now(), ": Start decode LZW")
        n = 10
        maximum_table_size = pow(2, int(n))
        file = open(file_input_path, "rb")
        compressed_data = []
        next_code = 256
        decompressed_data = ""
        string = ""
        print(datetime.now(), ": Reading compressed file")
        # Reading the compressed file.
        while True:
            rec = file.read(2)
            if len(rec) != 2:
                break
            (data, ) = unpack('>H', rec)
            compressed_data.append(data)
        print(datetime.now(), ": Init dictionary")
        # Building and initializing the dictionary.
        dictionary_size = 256
        dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])
        print(datetime.now(), ": Re")
        # iterating through the codes.
        # LZW Decompression algorithm
        temp = []
        for code in compressed_data:
            if not (code in dictionary):
                dictionary[code] = string + (string[0])
            temp.append(dictionary[code])
            if not(len(string) == 0):
                dictionary[next_code] = string + (dictionary[code][0])
                next_code += 1
            string = dictionary[code]
        decompressed_data = "".join(temp)
        # storing the decompressed string into a file.
        out = file_output_path
        output_file = open(out, "w")
        for data in decompressed_data:
            output_file.write(data)

        output_file.close()
        file.close()
