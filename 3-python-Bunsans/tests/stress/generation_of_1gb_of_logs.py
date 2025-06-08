import os

INPUT_FILENAME = "./input.txt"
OUTPUT_FILENAME = "./output.txt"
AMOUNT_OF_GB = 1

file_stats = os.stat(INPUT_FILENAME)
file_size_in_bytes = file_stats.st_size

input_text = ""
with open(INPUT_FILENAME, "r") as f:
    input_text = f.read()

times = (AMOUNT_OF_GB * 256 * 1024 * 1024) // file_size_in_bytes

with open(OUTPUT_FILENAME, "w") as file:
    file.write("\n".join(input_text for _ in range(times)))
