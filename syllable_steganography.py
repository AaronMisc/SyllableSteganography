# SyllableSteganography - Encode hidden messages in plain text, by counting the syllables.
# Copyright (C) 2026 AaronMisc
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# 
# This file includes code from Pyphen, which is licensed under a tri-license:
# GPL 2.0+, LGPL 2.1+, MPL 1.1. You may choose to use it under any of these licenses.

import pyphen
import re
import csv
from typing import Callable

# CONFIGURATION
LANGUAGE = "en_US"

CSV_DELIMITER = ";"
CSV_QUOTECHAR = '"'

SHOW_SYLLABLES = True

SYLLABLE_GROUP_SIZE = 4
BINARY_GROUP_SIZE = 4

CHARACTERS_TO_ID_PATH = "data/characters_to_id.csv"
SYLLABLE_OVERRIDE_PATH = "data/syllable_overrides.csv"

# INITIALIZATION
PYPHEN_DICTIONARY = pyphen.Pyphen(lang=LANGUAGE)

# CSV UTILITIES
def convert_csv_to_dict(
    file_path: str,
    reverse: bool = False,
    first_type: type = str,
    second_type: type = str
) -> dict:
    output = {}

    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=CSV_DELIMITER, quotechar=CSV_QUOTECHAR)
        for row in reader:
            if len(row) != 2:
                continue

            if reverse:
                key, value = row[1].strip(), row[0].strip()
            else:
                key, value = row[0].strip(), row[1].strip()

            output[first_type(key)] = second_type(value)

    return output

def load_syllable_overrides(file_path: str) -> dict[str, int]:
    overrides = {}

    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=CSV_DELIMITER, quotechar=CSV_QUOTECHAR)
            for row in reader:
                if len(row) != 2:
                    continue

                word = remove_non_letter_characters(row[0])
                try:
                    overrides[word] = int(row[1])
                except ValueError:
                    continue
    except FileNotFoundError:
        pass  # Silent by design

    return overrides

# TEXT UTILITIES
def split_dict_key_strings(dictionary: dict, split_by: str = "") -> dict:
    output = {}

    for key, value in dictionary.items():
        parts = list(key) if split_by == "" else key.split(split_by)
        for part in parts:
            output[part] = value

    return output

def remove_non_letter_characters(string: str) -> str:
    return re.sub(r"[^a-zA-Z']", "", string).lower()

# SYLLABLE LOGIC
def count_syllables(word: str) -> int:
    word = remove_non_letter_characters(word)
    if not word:
        return 0

    if word in SYLLABLE_OVERRIDES:
        syllables = SYLLABLE_OVERRIDES[word]
        if SHOW_SYLLABLES:
            print(f"{word}\t{syllables} (override)")

        return syllables

    hyphenated = PYPHEN_DICTIONARY.inserted(word)
    syllables = max(1, hyphenated.count("-") + 1)

    if SHOW_SYLLABLES:
        print(f"{hyphenated}\t{syllables}")

    return syllables

def syllables_from_string(string: str) -> list[int]:
    return [count_syllables(word) for word in string.split()]

# BIT CONVERSION
def odd_even_converter(n: int) -> int:
    return 0 if n % 2 == 0 else 1

def convert_syllable_group(
    syllables: list[int],
    converter: Callable = odd_even_converter
) -> list:
    output = []

    for i in range(len(syllables) // SYLLABLE_GROUP_SIZE):
        start = i * SYLLABLE_GROUP_SIZE
        stop = start + SYLLABLE_GROUP_SIZE
        output.append(converter(sum(syllables[start:stop])))

    return output

def convert_listed_binary_to_integers(listed_binary: list[int]) -> list[int]:
    output = []

    for i in range(len(listed_binary) // BINARY_GROUP_SIZE):
        start = i * BINARY_GROUP_SIZE
        stop = start + BINARY_GROUP_SIZE
        bits = "".join(map(str, listed_binary[start:stop]))
        output.append(int(bits, 2))

    return output

# DICTIONARY ENCODING
def encode_string_with_dictionary(string: str, dictionary: dict[str, int]) -> list[int]:
    return [dictionary[char] for char in string]

def decode_ids_with_dictionary(ids: list[int], dictionary: dict[int, str]) -> list[str]:
    return [dictionary[_id] for _id in ids]

# STEGANOGRAPHY PIPELINE
def steganography_decode_string(string: str, decode_dictionary: dict[int, str]) -> list[str]:
    syllables = syllables_from_string(string)
    bits = convert_syllable_group(syllables)
    integers = convert_listed_binary_to_integers(bits)
    return decode_ids_with_dictionary(integers, decode_dictionary)


# LOAD DATA
CHARACTERS_TO_ID = split_dict_key_strings(convert_csv_to_dict(CHARACTERS_TO_ID_PATH, second_type=int))

ID_TO_CHARACTERS = convert_csv_to_dict(CHARACTERS_TO_ID_PATH, reverse=True, first_type=int)

SYLLABLE_OVERRIDES = load_syllable_overrides(SYLLABLE_OVERRIDE_PATH)

if __name__ == "__main__":
    string = """Today I went shopping at the local store. I started acting strangely which was kinda dumb. I ate some food from the pyrotechnics store and now I'm stuffed. It was real fun."""
    decoded = steganography_decode_string(string, ID_TO_CHARACTERS)
    print(decoded)