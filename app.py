
import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
import pandas as pd
from statistics import median
import streamlit as st
import statistics
import numpy as np
import plotly.express as px
st.set_page_config(layout="wide")
st.subheader("Statistik basierend auf Tages-returns")
st.markdown(
    "Auf dieser Seite kann eine beliebige Aktie/Index, welche auf Yahoo Finance auffindbar ist,"
    " auf ihr Verhalten nach einem beliebigen Tages-return untersucht werden."
    " Zum Beispiel kann die Tesla Aktie auf ihr Verhalten nach einem Tagesreturn von etwa 6 % untersucht werden."
    )

col1,a, col2 = st.columns((0.5,0.3,1))
stock = col1.text_input("**Hier das Kürzel von YahooFinance eingeben:**  \n"
                        "(Zum Beispiel Tesla = TSLA)", 'TSLA')
st.write("##")

start_date1 = dt.date(2015, 1, 1)
end_date1 = dt.date.today()
format = 'MMM DD, YYYY'
slider = col2.slider('Dieser Slider ist nur für eine bessere Visualisierung der jeweiligen Aktie',
                      min_value=dt.date(2010, 1, 1), value=[start_date1,end_date1] ,max_value=end_date1, format=format)

stock_data1 = pdr.get_data_yahoo(stock, start=slider[0], end=slider[1])
my_expander = st.expander("chart",expanded=True)
my_expander.line_chart(stock_data1,y="Adj Close")

st.write("##")

c1, c2 = st.columns((2,1))
st.markdown("**Berechnungen:**  \n"
            "Das Vorgehen wird am Beispiel der Tesla Aktie erläutert:  \n"
            "Angenommen die Tesla Aktie ist Gestern um 6.4 % gestiegen. Uns interessiert nun wie sich die Aktie "
            "im Zeitfenster vom 2020/01/10 – 2023/01/02 nach ähnlichen Tages-returns verhalten hat."
            " Hierfür muss zuerst das entsprechende Zeitfenster ausgewählt und der \"daily percentage-range\" slider auf 6 und 7"
            " gesetzt werden. Eine gewisse Range ist nötig, da es unwahrscheinlich ist, dass die Aktie im gewählten Zeitfenster"
            " ebenso um genau 6.4 % gestiegen war. Bei einem zu eng gewählten Zeitfenster"
            " oder unwahrscheinlichen Tages-renditen kann es vorkommen, dass keine Tage gefunden werden mit ähnlichen Returns"
            " (date range too small)."
            )

c1, c2 = st.columns((1,2))
calc_range = c1.date_input("**wähle Zeitfenster für Berechnungen:**", [dt.date(2020, 1, 10), dt.date(2023, 1, 2)])

stock_data2 = pdr.get_data_yahoo(stock, start=calc_range[0], end=calc_range[1])

low = 6
high = 7
slider_1 = c2.slider('Wähle die **daily percentage-range** der Aktie: ', min_value=-25, value=[low,high] ,max_value=25)


def callculations (slider_1, stock_data2):
    p1 = slider_1[0]
    p2 = slider_1[1]
    stock_data = stock_data2
    lag1 = []
    today = []
    today2 = []
    lag0_2 = []
    lag0_3 = []
    lag0_5 = []
    for i in range(0, len(stock_data)):
        # print(i)
        percent = ((100 * stock_data["Adj Close"][i] / stock_data["Adj Close"][i - 1]) - 100)
        # print(percent)
        # print(stock_data)
        if p1 < percent < p2:
            if len(stock_data) - i > 3:
                today.append(percent)
                lag1.append((100 * stock_data["Adj Close"][i + 1] / stock_data["Adj Close"][i]) - 100)
                lag0_2.append((100 * stock_data["Adj Close"][i + 2] / stock_data["Adj Close"][i]) - 100)
                lag0_3.append((100 * stock_data["Adj Close"][i + 3] / stock_data["Adj Close"][i]) - 100)
            if len(stock_data) - i > 5:
                today2.append(percent)
                lag0_5.append((100 * stock_data["Adj Close"][i + 5] / stock_data["Adj Close"][i]) - 100)

    return (lag1,lag0_2,lag0_3,lag0_5,today,today2)

calc_data = callculations(slider_1, stock_data2)

def meanmedian (calc_data):
    lag1 = []
    lag2 = []
    lag3 = []
    lag5 = []
    if len(calc_data[0]) > 0:
        lag1.append(median(calc_data[0]))
        lag1.append(np.array(calc_data[0]).mean())
        lag1.append(statistics.pstdev(calc_data[0]))

        lag2.append(median(calc_data[1]))
        lag2.append(np.array(calc_data[1]).mean())
        lag2.append(statistics.pstdev(calc_data[1]))

        lag3.append(median(calc_data[2]))
        lag3.append(np.array(calc_data[2]).mean())
        lag3.append(statistics.pstdev(calc_data[2]))

    else:
        lag1.append("date-range to small")
        lag1.append("date-range to small")
        lag1.append("date-range to small")
        lag2.append("date-range to small")
        lag2.append("date-range to small")
        lag2.append("date-range to small")
        lag3.append("date-range to small")
        lag3.append("date-range to small")
        lag3.append("date-range to small")

    if len(calc_data[3]) > 0:
        lag5.append(median(calc_data[3]))
        lag5.append(np.array(calc_data[3]).mean())
        lag5.append(statistics.pstdev(calc_data[3]))
    else:
        lag5.append("date-range to small")
        lag5.append("date-range to small")
        lag5.append("date-range to small")

    #lag1.append(len(calc_data[0]))
    #lag2.append(len(calc_data[1]))
    #lag3.append(len(calc_data[2]))
    #lag5.append(len(calc_data[3]))

    return (lag1,lag2,lag3,lag5)

data = meanmedian(calc_data)
df = pd.DataFrame(data, columns=['Median Return %', 'Mean Return %','sd'], index=['nächster Tag', 'über die nächsten 2 Tage','über die nächsten 3 Tage','über die nächsten 5 Tage'])
new_df = np.round(df,1).astype(str)
st.write("###")
st.write("###")
c01,a01,c02 = st.columns((1.4,0.1,1))

c01.markdown("Im Tesla Beispiel hatten wir 12 Tage (Chart unten), an denen ein Tages-return zwischen 6-7 % auftrat."
             " Nach jedem dieser Tage wird nun der Return am darauffolgenden Tag ermittelt.  "
             "Danach wird der Mittelwert aus all diesen 12 \"nächster Tag retuns\" berechnet. Die selbe Prozedur wird"
             " angewandt auf den Return über die nächsten 2 Tage, die nächsten 3 Tage und die nächsten 5 Tage."
             " Im Tesla Beispiel wurde im gewählten Zeitfenster nach einem Tages-return von 6-7 % eine "
             " Rendite von -1.2 % im Durchschnitt und 3.2 % im Median über die folgenden 5 Tage erzielt."
             " Die Standartabweichung (sd) wird ebenfalls kalkuliert."
            )
c02.dataframe(new_df)

cdf = pd.DataFrame(calc_data, index=['nächster Tag', 'über die nächsten 2 Tage','über die nächsten 3 Tage','über die nächsten 5 Tage','gef. Events','gef. Vorkommnise']).T
#cdf['Occasions of the selected daily percentage range'] = cdf.index+1

st.write("##")
c11,a1,c22 = st.columns((1,0.2,1))

item_list = [col for col in cdf.columns if cdf[col].dtype in ['float64', 'int64']]
item1 = c11.selectbox('**Charts**', item_list[0:4], index=0)
cdf.index = cdf.index+1


c11.write('##')
c11.write('##')
def bachat(day):
    if day == 'über die nächsten 5 Tage':
        f2 = px.bar(cdf, y=['gef. Vorkommnise',day],title=day, x=cdf.index, template="none")
        f2.update_xaxes(title="Vorkommnis")
        f2.update_yaxes(title="return in %")
        f2.update_layout(plot_bgcolor="white",barmode="group")
        f2.data[0].marker.color = ('lightskyblue')
        f2.data[1].marker.color = ('darkorange')
        c11.plotly_chart(f2)
    else:
        f2 = px.bar(cdf, y=['gef. Events',day], title=day, x=cdf.index, template="none")
        f2.update_xaxes(title="Vorkommnis")
        f2.update_yaxes(title="return in %")
        f2.update_layout(plot_bgcolor="white",barmode="group")
        f2.data[0].marker.color = ('lightskyblue')
        f2.data[1].marker.color = ('darkorange')
        c11.plotly_chart(f2)

bachat(item1)


c22.write('##')
c22.markdown("Die blauen Balken stehen für die Tage (Events), an denen der Tages-return zwischen "
             " der ausgewählten daily percentage-range liegt. Die orangen Balken zeigen die jeweilige Rendite"
             " der ausgewählten nachfolgenden Zeitperiode (nächster Tag, über die nächsten 2 Tage, etc.)"
             )
c22.write('##')
c22.write('##')
c22.write('##')
c22.write('##')
c22.write('##')
c22.write('##')
c22.write('##')
c22.write('##')
c22.write('##')
c22.write('##')
c22.write('##')
c22.write('##')
c22.write('##')
c22.write('##')
c22.markdown("Wenn das Zeitfenster und die daily percentage-range gross genug ausgewählt werden macht "
             " es Sinn, nur die Häufigkeits-Verteilung der Renditen anzuschauen. Wenn genug Daten vorhanden sind, sollte sich"
             " die Verteilung der Renditen an eine Normalverteilung angleichen."
             )

c11.write('##')
c11.write('##')
c11.write('##')
c11.write('##')
f = px.histogram(cdf[item1], nbins=100, title="Verteilung der Renditen", template="none")
f.update_xaxes(title="return in %")
f.update_yaxes(title="Häufigkeit")
f.update_layout(plot_bgcolor = "white")
f.data[0].marker.color = ('darkorange')
c11.plotly_chart(f)
