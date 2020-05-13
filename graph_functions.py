import plotly.express as px
import pandas as pd


#Graffunktion för kombination av flera grafer
def to_graph_multiple(df_list):
    df = df_list[0]
    
    for item in df_list:
        column = item.columns[2]
        df[column] = item[column]
       
    df["Date"] = df["Datum"].astype(str) + " " + df["Tid (UTC)"].astype(str)
    
    df_long=pd.melt(df, id_vars=['Date'], value_vars=[df.columns[x] for x in range(2,2+len(df_list))])
    fig = px.line(df_long, x='Date', y='value', color='variable')

    return fig.show()

#Graffunktion
def to_graph(df):
    df["Date"] = df["Datum"].astype(str) + " " + df["Tid (UTC)"].astype(str)
    y = df.columns[2]
    fig = px.line(df, x='Date', y=y)
    return fig.show()
