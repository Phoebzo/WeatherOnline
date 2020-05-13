### project file
 
import csv
import io
from datetime import datetime
import pandas as pd
import os
import urllib.request

# For the gui
import pygame
import gui
import time

# For rhe graphs
import plotly.express as px

def main():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now)
    # response = get_data("latest-day", "Lufttemperatur" )
    # print(response)
    response2 = get_sunshine("latest-day")
    # print(response2)

    

def calender(yyyy, mm, dd, hh):
    time = datetime.timestamp(datetime(yyyy,mm,dd,hh))
    return time

def filter(in_name, out_name):
    with open(out_name, 'w') as outfile, open(in_name, 'r', encoding='utf-8') as infile:
        line_nr = 0
        for line in infile:
            if line_nr < 9:
                line_nr+=1
            else:
                count = 0
                out_line = ""
                for char in line:
                    if char == ";":
                        count+=1
                        if count==3:
                            outfile.writelines(out_line+"\n")
                            break
                        out_line += ","
                    else:
                        out_line += char


def get_sunshine(period):
    url = f"https://opendata-download-metobs.smhi.se/api/version/latest/parameter/10/station/65075/period/{period}/data.csv"
    
    infile = "infile_sun.xls"
    outfile = "outfile_sun.xls"
    urllib.request.urlretrieve(url, infile)

    filter(infile, outfile)
    raw = pd.read_csv(outfile, dtype= "category", sep= ",")
    data = pd.DataFrame(raw)
    return data

def get_data(date, parameter):
    period = date
    para_dict = {
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
        "Daggpunktstemperatur":39
    }
 
    url = f"https://opendata-download-metobs.smhi.se/api/version/latest/parameter/{para_dict[parameter]}/station/65090/period/{period}/data.csv"

    infile = "infile_data.xls"
    outfile = "outfile_data.xls"
    urllib.request.urlretrieve(url, infile)

    filter(infile, outfile)
    raw = pd.read_csv(outfile, dtype= "category", sep= ",")
    data = pd.DataFrame(raw)
    return data


if __name__ == "__main__":
    main()