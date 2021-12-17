#!/usr/bin/python3
import struct
import sys
import math
import os

def encode(search: bytes=b"", look_ahead: bytes=b"") -> tuple:

     len_search = len(search)
     len_look_ahead = len(look_ahead)

     if len_search == 0:
        return (0, 0, look_ahead[0])
     
     if len_look_ahead == 0:
        return (-1, -1, "")

     best_length = 0
     best_offset = 0 
     buff = search + look_ahead

     for i in range(0, len_search):
        length = 0
        while buff[i + length] == buff[len_search + length]:
            length += 1
            if len_search + length == len(buff):
                length -= 1
                break
            if i + length >= len_search:
                break	 
            if length > best_length:
                best_offset = i
                best_length = length

     return (best_offset, best_length, buff[len_search + best_length])

def int_to_bytes(number: int=0) -> bytes:
    hrepr = hex(number).replace('0x', '')
    if len(hrepr) % 2 == 1:
        hrepr = '0' + hrepr
    return bytes.fromhex(hrepr)

def read_file(filename: str="") -> bytes:
    with open(filename, "rb") as b_file:
        return (b_file.read())

def main(filename: str="") -> int:
    count_bits = 16
    max_offset = 4096
    max_length =  int(math.pow(2, (count_bits  - (math.log(max_offset, 2))))) 

    b_file = read_file("./input/" + filename)
    output = open("./output/" + filename + ".enc", "wb")
    first = 0
    second = 0

    while second < len(b_file):
        search = b_file[first:second]
        look_ahead = b_file[second:second + max_length]
        offset, length, char = encode(search, look_ahead)
        shifted_offset = offset << int(count_bits - math.log(max_offset, 2))
        offset_and_length = shifted_offset + length
        ol_bytes = struct.pack(">Hc", offset_and_length, int_to_bytes(char))
        output.write(ol_bytes) 

        second += length + 1
        first = second - max_offset

        if first < 0:
            first = 0

    output.close()

    return (0)
             
if __name__== "__main__":
    arr = os.listdir("./input")
    for el in arr:
        main(el)
