import copy
import numpy as np
from key import key

class Encruption:
    def __init__(self, text_path : str, key_path : str, result_path : str, mode : int):
        self.Substitution = np.array([["c", "4", "6", "2", "a", "5", "b", "9", "e", "8", "d", "7", "0", "3", "f", "1"],
                                    ["6", "8", "2", "3", "9", "a", "5", "c", "1", "e", "4", "7", "b", "d", "0", "f"],
                                    ["b", "3", "5", "8", "2", "f", "a", "d", "e", "1", "7", "4", "c", "9", "6", "0"],
                                    ["c", "8", "2", "1", "d", "4", "f", "6", "7", "0", "a", "5", "3", "e", "9", "b"],
                                    ["7", "f", "5", "a", "8", "1", "6", "d", "0", "9", "3", "e", "b", "4", "2", "c"],
                                    ["5", "d", "f", "6", "9", "2", "c", "a", "b", "7", "8", "1", "4", "3", "e", "0"],
                                    ["8", "e", "2", "5", "6", "9", "1", "c", "f", "4", "b", "0", "d", "a", "3", "7"],
                                    ["1", "7", "e", "d", "0", "5", "8", "3", "4", "f", "a", "6", "9", "c", "b", "2"]])

        self.keys = key(key_path)

        self.text = []
        hex_bits = ""
        with open(text_path, "rb") as f:
            open_text = f.read()
            hex_bits = bytes.hex(open_text)
        if len(hex_bits) % 16 != 0:
            hex_bits += ("0" * (16 - (len(hex_bits) % 8)))

        block_size = 16
        for i in range(len(hex_bits) // 16):
            start = i * block_size
            end = start + block_size
            self.text.append(hex_bits[start:end])

        self.__Encruption(result_path, mode)

    def __Encruption(self, result_path : str, mode : int):
        if mode == 2:
            self.keys.round_key.reverse()
        elif mode != 1 and mode != 2:
            raise ValueError(f"Invalid mode")
        
        new_text = copy.copy(self.text)
        for i in range(len(self.text)):
            current_text = [self.text[i][:8], self.text[i][8:]]
            for j in range(len(self.keys.round_key)):
                first_stage = self.__Encruption_first_step(current_text[1], self.keys.round_key[j])
                second_stage = self.__Encruption_second_step(first_stage)
                third_stage = self.__Encruption_third_step(second_stage)
                four_stage = self.__Encruption_four_step(current_text[0], third_stage)
                current_text = [current_text[1], four_stage]
            new_text[i] = current_text[1] +  current_text[0]

        encruption = ""
        for i in new_text:
            encruption += i
        with open(result_path, "wb") as f:
            f.write(bytes.fromhex(encruption))
        print(bytes.fromhex(encruption))

    def __Encruption_first_step(self, second_current_text, round_key):
        summ_mod = (int(second_current_text, 16) + int(round_key, 16)) % (2 ** 32)
        hex_summ = hex(summ_mod)[2:]
        if len(hex_summ) <8:
            hex_summ = ("0" * (8 - len(hex_summ))) + hex_summ
        return hex_summ

    def __Encruption_second_step(self, first_step):
        for i in range(8):
            first_step = first_step[:i] + self.Substitution[7 - i][int(first_step[i], 16)] + first_step[i + 1:]
        return first_step

    def __Encruption_third_step(self, second_step):
        bin_string = bin(int(second_step, 16))[2:]
        if len(bin_string) < 32:
            bin_string = ("0" * (32 - len(bin_string))) + bin_string
        bin_string = bin_string[11:] + bin_string[:11]
        return bin_string

    def __Encruption_four_step(self, first_current_text, third_step):
        bin_form = bin(int(first_current_text, 16))[2:]
        if len(bin_form) % 4 != 0:
            bin_form = ("0" * (4 - (len(bin_form) % 4))) + bin_form
        
        xor = str(int(bin_form) + int(third_step))
        if len(xor) % 4 != 0:
            xor = ("0" * (4 - (len(xor) % 4))) + xor
        for i in range(len(xor)):
            xor = xor[:i] + str(int(xor[i]) % 2) + xor[i + 1:]

        hex_form = ""
        while len(xor) != 0:
            hex_form += hex(int(xor[:4], 2))[2:]
            xor = xor[4:]

        return hex_form