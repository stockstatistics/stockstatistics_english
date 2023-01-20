
import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
st.set_page_config(layout="wide")
st.subheader("Durchschnittliche monatliche Returns")
st.markdown(
    "Auf dieser Seite können die Durchschnitts- und Medianrenditen in jedem Monat berechnet werden."
    " Hierfür muss nur das Zeitfenster über welches die Berechnungen stattfinden sollen"
    " und das jeweilige Aktienkürzel ausgewählt werden. Dargestellt werden die Resultate in der Tabelle sowie im Balken Diagramm.")
st.write("##")
col1,a, col2 = st.columns((0.4,0.1,1.2))

stock = col1.text_input("**shortcut of YahooFinance**"
                       "(For example Apple = AAPL)", 'AAPL')

st.write("##")

start_date1 = dt.date(2010, 1, 1)
end_date1 = dt.date.today()
format = 'MMM DD, YYYY'
slider = col2.slider('Zeitfenster für Berechnungen:',
                      min_value=dt.date(1970, 1, 1), value=[start_date1,end_date1] ,max_value=end_date1, format=format)

stock_data_m = pdr.get_data_yahoo(stock, start=slider[0], end=slider[1],interval='1mo')

col2.line_chart(stock_data_m,y="Adj Close" )

df_m = stock_data_m[['Open','Close']]

def monthcalc():
    mds = list(range(1,13,1))
    l_m = []
    l_med = []
    for i in mds:
        i = df_m[df_m.index.month == int(i)]
        i['return'] = ((100 * i['Close'])/i['Open'])-100
        mean = i['return'].mean()
        median=i['return'].median()
        l_m.append(mean)
        l_med.append(median)
    d = {'average return in %': l_m,'median return in %': l_med}
    df = pd.DataFrame(data=d,index=['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dez'])

    return np.round(df,1)

month_avg = monthcalc()

col11, a1,col22 = st.columns((0.4,0.1,1.2))
col11.write("##")
col11.markdown("**Berechnungen:**")
col11.dataframe(month_avg.astype(str))

f = px.bar(month_avg,y=["average return in %","median return in %"], x=month_avg.index, template="none")
f.update_xaxes(title="Monat")
f.update_yaxes(title="percent")
f.update_layout(plot_bgcolor="white",barmode="group")
f.data[0].marker.color = ('lightskyblue')
f.data[1].marker.color = ('darkorange')
col22.plotly_chart(f)
