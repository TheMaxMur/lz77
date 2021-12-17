#!/usr/bin/python3
import math
import struct
import os

def bytes_to_int(byte: bytes=b"") -> int:
    result = 0
    for b in byte:
        result = result * 256 + int(b)
    return result

def read_file(filename: str="") -> bytes:
    with open(filename, "rb") as b_file:
        return (b_file.read())

def write_file(filename: str="", data: bytearray=bytearray()) -> None:
    with open(filename, "wb") as b_file:
        b_file.write(data)

def decoder(filename: str="") -> bytearray:
    max_offset = 4096
    b_file = read_file(filename)
    
    char_array = bytearray()
    i = 0

    while i < len(b_file):
        offset_and_length, char = struct.unpack(">Hc", b_file[i:i+3])
        offset = offset_and_length >> int(16 - math.log(max_offset, 2))
        length = offset_and_length - (offset << int(16 - math.log(max_offset, 2)))
        i = i + 3

        if (offset == 0) and (length == 0):
            char_array.append(bytes_to_int(char))
        else:
            index1 = len(char_array) - max_offset
            if index1 < 0:
                index1 = offset
            else:
                index1 += offset
            for index2 in range(length):
                char_array.append(char_array[index1 + index2])
            char_array.append(bytes_to_int(char))
                            
    return (char_array)

def main(filename: str="") -> int:
    result = decoder("./output/" + filename)
    write_file("./decode/" + filename[:-4], result)

    return (0)

if __name__== "__main__":
    arr = os.listdir("./output")
    for el in arr:
        main(el)
