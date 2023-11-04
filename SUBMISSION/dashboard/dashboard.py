import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style='dark')

# Membuat Helper Function
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by="dateday").agg({
        "count": "sum"
    })
    daily_rent_df = daily_rent_df.reset_index()
    
    return daily_rent_df

def creat_sum_byseason_df(df):
    sum_byseason_df = df.groupby(by="season").agg({
        "count": "sum"
    })
    sum_byseason_df = sum_byseason_df.reset_index()

    return sum_byseason_df

def create_performing_month_2011_df(df):
    performing_month_2011_df = df.groupby(by=["year", "month"]).agg({
        "count": "sum"
    })
    performing_month_2011_df=performing_month_2011_df.reset_index()
    
    return performing_month_2011_df

# Load Berkas csv
all_df = pd.read_csv("https://raw.githubusercontent.com/Rzkoxd/bike-share-tes/main/SUBMISSION/dashboard/main_data.csv")

datetime = ["dateday"]
all_df.sort_values(by=["dateday", "month"], inplace=True)
all_df.reset_index()

for x in datetime:
    all_df[x] = pd.to_datetime(all_df[x])

# Membuat Komponen Filter
min_date = all_df["dateday"].min()
max_date = all_df["dateday"].max()

with st.sidebar:
    # Mengambil start_date & end_date
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Menambah logo
    st.image("https://thumbs.dreamstime.com/z/bike-sharing-thin-line-icon-bicycle-pointers-logo-rental-service-modern-vector-illustration-193221556.jpg")

main_df = all_df[(all_df["dateday"] >= str(start_date)) &
                 (all_df["dateday"] <= str(end_date))]

daily_rent_df = create_daily_rent_df(main_df)
sum_byseason_df = creat_sum_byseason_df(main_df)
performing_month_2011_df = create_performing_month_2011_df(main_df)

# Mengambil tabel 2011
performing_month_2011_df = performing_month_2011_df[(performing_month_2011_df["year"] == 2011)]
# Mengurutkan bulan
performing_month_2011_df=performing_month_2011_df.set_index("month")
bulan_urutan = ["January", "February", "March", "April", "May", "June", "July", "Augustus", "September", "October", "November", "December"]
performing_month_2011_df = performing_month_2011_df.reindex(bulan_urutan)

# Melengkapi dashboard dgn berbagai visualisasi
st.header("Bike Sharing Dashboard")
st.subheader("Daily Rent")

total_rent = daily_rent_df["count"].sum()
st.metric("Total Rent", value=total_rent)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rent_df["dateday"],
    daily_rent_df["count"],
    marker="o", 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis="y", labelsize=20)
ax.tick_params(axis="x", labelsize=20)
st.pyplot(fig)

st.subheader("Number of Bike Sharing by Season")
fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"]
sns.barplot(
    data = sum_byseason_df.sort_values(by="count", ascending=True),
    x = "season",
    y = "count",
    ax = ax,
    palette = colors
)
ax.set_title("Number of Bike Sharing by Season in 2011-2012", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis="y", labelsize=13)
ax.tick_params(axis="x", labelsize=13)
st.pyplot(fig)

st.subheader("Performing Bike Sharing by Month in 2011")
fig, ax = plt.subplots(figsize=(25, 15))
sns.lineplot(
    data=performing_month_2011_df,
    x="month",
    y="count",
    color="red",
    marker="o"
)
ax.set_title("Performing Bike Sharing per Month in 2011", fontsize=30)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis="y", labelsize=23)
ax.tick_params(axis="x", labelsize=23)
st.pyplot(fig)

