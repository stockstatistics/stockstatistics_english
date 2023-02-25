
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
st.subheader("ANALYSIS OF DAILY RETURNS")
st.markdown(
    "On this page, any stock or index listed on Yahoo Finance can be examined for its behavior after "
    "a special daily return. For example, the Tesla stock can be analyzed for its performance after daily gains of about 6 %."
    )

col1,a, col2 = st.columns((0.5,0.3,1))
stock = col1.text_input("**Insert any Yahoo Finance ticker symbol here:**  \n"
                        "Example Tesla = TSLA , NASDAQ = ^IXIC , S&P500 = ^GSPC", 'TSLA')
st.write("##")

start_date1 = dt.date(2015, 1, 1)
end_date1 = dt.date.today()
format = 'MMM DD, YYYY'
slider = col2.slider('This slider is intended only for the visualization of the respective stock',
                      min_value=dt.date(2010, 1, 1), value=[start_date1,end_date1] ,max_value=end_date1, format=format)

stock_data1 = pdr.get_data_yahoo(stock, start=slider[0], end=slider[1])
my_expander = st.expander("chart",expanded=True)
my_expander.line_chart(stock_data1,y="Adj Close")

st.write("##")

c1, c2 = st.columns((2,1))
st.markdown("**Calculations:**  \n"
            "The methodology is best illustrated using the Tesla share as an example:  \n"
            "Assuming that the Tesla stock increased by 6.4 % yesterday, we are curious how "
            "the stock has performed in the time period from 2020/01/10 - 2023/01/02 after similar daily returns occurred."
            " For this purpose we first have to select the respective \"time period\" and set "
            "the \"daily percentage range\" slider to 6 and 7."
            " A certain range is necessary, since it is unlikely for the stock to have risen by exactly 6.4 % "
            "in the selected time period. If the selected time period is too narrow or the daily returns are unlikely, "
            "it may happen that no days with similar returns are found (date range too small)."
            )

c1, c2 = st.columns((1,2))
calc_range = c1.date_input("Select a **time period** for the calculations:", [dt.date(2020, 1, 10), dt.date(2023, 1, 2)])

stock_data2 = pdr.get_data_yahoo(stock, start=calc_range[0], end=calc_range[1])

low = 6
high = 7
slider_1 = c2.slider('Set the **daily percentage range** of the stock: ', min_value=-25, value=[low,high] ,max_value=25)


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
        #percent = ((100 * stock_data["Adj Close"][i] / stock_data["Adj Close"][i - 1]) - 100)
        percent = ((100 * stock_data["Adj Close"][i] / stock_data["Open"][i]) - 100)
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
df = pd.DataFrame(data, columns=['Median Return %', 'Mean Return %','sd'], index=['next day', 'over the next 2 days','over the next 3 days','over the next 5 days'])
new_df = np.round(df,1).astype(str)
st.write("###")
st.write("###")
c01,a01,c02 = st.columns((1.4,0.1,1))

c01.markdown("In the Tesla example we had 12 days (chart below) where a daily return between 6-7 % occurred. After "
             "each of these days, the return on the following day is evaluated. Then the average of all "
             "these 12 \"next day retuns\" is calculated. The same method is applied to the return over "
             "the next 2 days, the next 3 days and the next 5 days. In the Tesla example, a return "
             "of -0.6 % on average and a median -2.8 % return over the next 5 days was achieved in the selected time "
             "period after a daily return of 6-7 %. The standard deviation (sd) is calcualted as well."
            )
c02.dataframe(new_df)

cdf = pd.DataFrame(calc_data, index=['next day', 'over the next 2 days','over the next 3 days','over the next 5 days','Events','Occurrences']).T
#cdf['Occasions of the selected daily percentage range'] = cdf.index+1

st.write("##")
c11,a1,c22 = st.columns((0.1,1,0.1))

a1.markdown("The blue bars in the chart below represent the days (events) where the daily return lies between the "
             "selected daily percentage range. Thus, in the Tesla example, these fall between 6 and 7 percent. "
             "The orange bars show the respective return of the selected subsequent time period (next day, over "
             "the next 2 days, etc.).")

item_list = [col for col in cdf.columns if cdf[col].dtype in ['float64', 'int64']]
item1 = a1.selectbox('**Charts**', item_list[0:4], index=0)
cdf.index = cdf.index+1

def bachat(day):
    if day == 'over the next 5 days':
        f2 = px.bar(cdf, y=['Occurrences',day],title=day, x=cdf.index, template="none")
        f2.update_xaxes(title="Occurrences")
        f2.update_yaxes(title="Return in %")
        f2.update_layout(plot_bgcolor="white",barmode="group")
        f2.data[0].marker.color = ('lightskyblue')
        f2.data[1].marker.color = ('darkorange')
        a1.plotly_chart(f2)
    else:
        f2 = px.bar(cdf, y=['Events',day], title=day, x=cdf.index, template="none")
        f2.update_xaxes(title="Occurrences")
        f2.update_yaxes(title="Return in %")
        f2.update_layout(plot_bgcolor="white",barmode="group")
        f2.data[0].marker.color = ('lightskyblue')
        f2.data[1].marker.color = ('darkorange')
        a1.plotly_chart(f2)

bachat(item1)

a1.markdown("If the selected time period and the daily percentage range are wide enough, it "
            "makes sense to look only at the frequency distribution of the returns. Based on "
            "the probability theory, the distribution of the returns should converge to a normal "
            "distribution if enough data is available."
             )

f = px.histogram(cdf[item1], nbins=100, title="Frequency distribution of the returns", template="none")
f.update_xaxes(title="Return in %")
f.update_yaxes(title="Frequency")
f.update_layout(plot_bgcolor = "white")
f.data[0].marker.color = ('darkorange')
a1.plotly_chart(f)
