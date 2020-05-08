

import pandas as pd
import numpy as np
import os

# For the gui
import pygame
import gui
import time

def main():
    csv_frame = pd.DataFrame()
    directory = os.fsencode(directory_in_str)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".asm") or filename.endswith(".py"): 
            # print(os.path.join(directory, filename))
            continue
        else:
            continue
    csv_frame = load_csv_file(file_name, csv_frame)
    time.sleep(2)
    interface = gui.Interface()
    interface.run()


def load_csv_file(file_name, csv_frame):
    try:
        csv_frame = pd.read_csv(file_name, dtype= "category", sep= ",")
    except FileNotFoundError:
        print(f"\nError when reading file: File '{file_name}' does not exist")
    return csv_frame


if __name__ == "__main__":
    main()