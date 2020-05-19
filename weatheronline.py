### project file


# For the data
import csv
import io
from datetime import datetime, timedelta
import pandas as pd
import os
import urllib.request

# For the gui
import pygame
import time

# For rhe graphs
import plotly.express as px

# import classes
import classes

parameter_dict = {
            "Lufttemperatur": 1,
            "Vindriktning":3,
            "Vindhastighet":4,
            "Nederbördsmängd":5,
            "Relativ Luftfuktighet":6,
            "Lufttryck reducerat havsytans nivå":9,
            "Sikt":12,
            "Rådande väder":13,
            "Total molnmängd":16,
            "Byvind":21,
            "Molnbas":28,
            "Molnmängd":29,
            "Daggpunktstemperatur":39,
            "Sunshine procentage": None
        }

timereader = classes.TimeReader()
graphdrawer = classes.GraphDrawer()
datareader = classes.DataReader()


def main():
    running = True
    while running:
        running = menu()

def menu():
    print(f"\nTime (UTC) now: {timereader.clock()} \n\nRemember, at any point in the menu you can exit by typing exit and pressing enter.\n")
    try:
        print("1. Enter Parameters (comma-separated) from available: ")
        for para in parameter_dict.keys():
            print(para)
        parameter = input("or Sunshine procentage: ")
        if "exit" == parameter.lower():
            return False
        for para in parameter.split(","):
            if para not in parameter_dict.keys():
                raise ValueError
        time = input("2. Enter timeperiod (yyyy-mm-dd hh:mm to yyyy-mm-dd hh:mm):")
        if "exit" == time.lower():
            return False
        if len(time.split("-")) != 5:
            raise ValueError
        reptype = input("3. Enter how data should be presented (file, graph, dataframe): ")
        if "exit" == reptype.lower():
            return False
        if not(reptype in ["file", "graph", "dataframe"]):
            raise ValueError

    except Exception:
        print("Wrong type, try again...")
        menu()
    
    parameter = list(parameter.split(","))
    period = time_manage(time)
    choice(parameter, period, reptype)
    return True

def time_manage(time):
    time = time.split(" to ")
    timefrom = time[0]
    timefrom = timefrom.split(" ")
    timeto = time[1]
    timeto = timeto.split(" ")
    period = {
        "date_from": timefrom[0],
        "date_to": timeto[0],
        "time_from": timefrom[1]+":00",
        "time_to": timeto[1]+":00"
    }
    return period


def choice(para, period, reptype):
    print("Loading data, may take a while...")
    frame = pd.DataFrame()
    for parameter in para:
        if parameter == "Sunshine procentage":
            data = datareader.sunshine_percent(period["date_from"], period["date_to"], period["time_from"],period["time_from"])
        else:
            data = datareader.get_data(parameter_dict, parameter, period["date_from"], period["date_to"], period["time_from"],period["time_from"])
        frame = append_parameter_data(frame, data, parameter, para)

    if reptype.lower() == "file":
        try:
            os.remove("data.xls")
            frame.to_csv("data.xls", index=False)
        except FileNotFoundError:
            frame.to_csv("data.xls", index=False)
    elif reptype.lower() == "graph":
        graphdrawer.to_graph_multiple(frame)
    elif reptype.lower() == "dataframe":
        print(frame)


def append_parameter_data(frame, data, parameter, para):
    for column in data.columns:
        if column not in frame.columns:
            frame[column] = data[column].tolist()

    return frame

if __name__ == "__main__":
    main()

