import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title("Streamlit Test - DTA Data")

dtadf = pd.read_csv('dtaDATA.csv')

dtadf["TotalFuel"] = dtadf["TotalFuel"].apply(lambda x: x - 29156,3219)
dtadf["TotalFuel"] = dtadf["TotalFuel"].apply(lambda x: x *10)

dtadf["EngineTorque"] = dtadf["EngineTorque"].apply(lambda x: x/100)

st.write(dtadf)

st.map(dtadf)

new_dataset = dtadf[['EngineTorque','SPEED', 'TotalFuel']]

st.line_chart(new_dataset)

st.title("Streamlit test")

# Streamlit demo code - Uber data

DATE_TIME = "date/time"
DATA_URL = (
    "http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)

st.subheader("Uber Pickups in New York City")

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data


data = load_data(100000)

hour = st.slider("Hour to look at", 0, 23)

data = data[data[DATE_TIME].dt.hour == hour]

st.subheader("Geo data between %i:00 and %i:00" % (hour, (hour + 1) % 24))
midpoint = (np.average(data["lat"]), np.average(data["lon"]))
st.deck_gl_chart(
    viewport={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        {
            "type": "HexagonLayer",
            "data": data,
            "radius": 100,
            "elevationScale": 4,
            "elevationRange": [0, 1000],
            "pickable": True,
            "extruded": True,
        }
    ],
)

if st.checkbox("Show raw data", False):
    st.subheader("Raw data by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    st.write(data)

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data[
    (data[DATE_TIME].dt.hour >= hour) & (data[DATE_TIME].dt.hour < (hour + 1))
]
hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})
st.write(alt.Chart(chart_data, height=150)
    .mark_area(
        interpolate='step-after',
        line=True
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ))



