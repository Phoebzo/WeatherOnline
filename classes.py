import plotly.express as px
import pandas as pd

import time
from datetime import datetime, timedelta

import csv
import io
import os
import urllib.request



class GraphDrawer:
    #Graffunktion för kombination av flera grafer
    def to_graph_multiple(self, df_list):
        df = df_list[0]
        
        for item in df_list:
            column = item.columns[2]
            df[column] = item[column]
        
        df["Date"] = df["Datum"].astype(str) + " " + df["Tid (UTC)"].astype(str)
        
        df_long=pd.melt(df, id_vars=['Date'], value_vars=[df.columns[x] for x in range(2,2+len(df_list))])
        fig = px.line(df_long, x='Date', y='value', color='variable')

        return fig.show()

    #Graffunktion
    def to_graph(self, df):
        df["Date"] = df["Datum"].astype(str) + " " + df["Tid (UTC)"].astype(str)
        y = df.columns[2]
        fig = px.line(df, x='Date', y=y)
        return fig.show()


class TimeReader:
    def clock(self):
        cet = datetime.now()
        utc = cet - timedelta(hours=2)
        return utc
    
    def timestr(self, time):
        return time.strftime('%Y-%m-%d %H:%M')

    def timeint(self, yyyy, mm, dd, hh):
        time = datetime.timestamp(datetime(yyyy,mm,dd,hh))
        return time

    def possible_days(self, yyyy, mm):
        if mm < 8:
            if mm%2 == 0:
                days = 30
                if mm == 2:
                    days = 28
                    if yyyy%4==0:
                        days = 29
            else:
                days = 31
        elif mm >= 8:
            if mm%2 == 0:
                days = 31
            else:
                days = 30
        return days


class DataReader:
    def filter(self, in_name, out_name, parameter):
        try:
            lines = []
            with open(out_name, 'r') as outfile:
                for line in outfile:
                    lines.append(line)
        except FileNotFoundError:
            lines = []

        with open(out_name, 'w') as outfile, open(in_name, 'r', encoding='utf-8') as infile:
            line_nr = 0
            indexsaved = []
            for line in infile:
                if line_nr < 9:
                    line_nr+=1
                elif line_nr == 9:
                    words = line.split(";")
                    saved_words = []
                    for word in words:
                        if word in ["Datum", "Tid (UTC)", parameter]:
                            indexsaved.append(words.index(word))
                            saved_words.append(word)
                    
                    out_line = ",".join(saved_words)
                    outfile.writelines(out_line+"\n")
                    line_nr += 1

                else:
                    words = line.split(";")
                    saved_words = []
                    for index in indexsaved: 
                        saved_words.append(words[index])
                    
                    out_line = ",".join(saved_words)
                    out_line = out_line+"\n"
                    if out_line not in lines:
                        outfile.writelines(out_line)


    def get_sunshine(self):
        data = pd.DataFrame()
        for period in ["latest-months", "corrected-archive"]:
            url = f"https://opendata-download-metobs.smhi.se/api/version/latest/parameter/10/station/65075/period/{period}/data.csv"
            
            infile = "infile_sun.xls"
            outfile = "outfile_sun.xls"
            urllib.request.urlretrieve(url, infile)

            self.filter(infile, outfile, "Solskenstid")

            raw = pd.read_csv(outfile, dtype= "category", sep= ",")
            temp = pd.DataFrame(raw)
            data = data.append(temp)
            os.remove(infile)
            os.remove(outfile)


        return data

    def get_data(self, dict, parameter, date_from, date_to, time_from, time_to):
        data = pd.DataFrame()

        for period in ["latest-months", "corrected-archive"]:
            url = f"https://opendata-download-metobs.smhi.se/api/version/latest/parameter/{dict[parameter]}/station/65090/period/{period}/data.csv"
            infile = "infile_data.xls"
            outfile = "outfile_data.xls"
            urllib.request.urlretrieve(url, infile)

            self.filter(infile, outfile, parameter)

            raw = pd.read_csv(outfile, dtype= "category", sep= ",")
            temp = pd.DataFrame(raw)
            data = data.append(temp, ignore_index=True)
            os.remove(infile)

        os.remove(outfile)
        data = self.periodize(data, date_from, date_to, time_from, time_to)
        data = self.fill_blanks(data, parameter)
        return data

    def periodize(self, data, date_from, date_to, time_from, time_to):
        data.sort_values(by=["Datum", "Tid (UTC)"], inplace=True, ascending=True)
        start = self.find_row(date_from, time_from, data)
        end = self.find_row(date_to, time_to, data)
        data = data.loc[start:end]
        data = data.reset_index()
        data = data.drop('index', 1)
        return data

    def fill_blanks(self, data, parameter):
        start = (data.iloc[0]["Datum"]+ " "+ data.iloc[0]["Tid (UTC)"])
        time_start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        end = (data.iloc[-1]["Datum"]+ " "+ data.iloc[-1]["Tid (UTC)"])
        time_end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        time_correct = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        length = int(self.length(time_start, time_end))
        index = 0

        for _ in range(length):
            time_correct_str = datetime.strftime(time_correct, "%Y-%m-%d %H:%M:%S")
            time_to_test = (data.iloc[index]["Datum"]+ " "+ data.iloc[index]["Tid (UTC)"])
            if time_to_test == time_correct_str:
                index += 1
            else: 
                time_correct_str = datetime.strftime(time_correct, "%Y-%m-%d %H:%M:%S")
                time = time_correct_str.split(" ")
                dicton = {
                    "Datum": time[0],
                    "Tid (UTC)": time[1],
                    parameter: ""
                }
                data = data.append(dicton, ignore_index=True)

            time_correct = time_correct + timedelta(hours=1)

        data.sort_values(by=["Datum", "Tid (UTC)"], inplace=True, ascending=True)
        data = data.reset_index()
        data = data.drop('index', 1)
        return data

    def length(self, date_from, date_to):
        diffrence = date_to - date_from
        # Divide difference in seconds by number of seconds in hour (3600)  
        diffrence = diffrence.total_seconds() / 3600
        return diffrence

    def find_row(self, date,time, data):
        for index , row in data.iterrows():
            if row['Datum'] == date and row['Tid (UTC)'] == time:
                return index

    def sunshine_percent(self, date_from, date_to, time_from, time_to):
        data = self.get_sunshine()
        start = self.find_row(date_from, time_from, data)
        end = self.find_row(date_to, time_to, data)
        solsken_toint = data.loc[start:end, 'Solskenstid'].astype('int64')
        sum_is = solsken_toint.sum(axis = 0)
        total_sum = (end - start + 1) * 3600
        percent = (sum_is / total_sum) * 100
        return percent

        