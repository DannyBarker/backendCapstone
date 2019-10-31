from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pandas as pd
import sqlite3 as sql
import folium
from folium import plugins
from folium.plugins import MarkerCluster
from capstone.models import Customer

def create_map(id_for_map):
    conn = sql.connect("db.sqlite3")
    pay_df = pd.read_sql_query("SELECT * FROM capstone_payment;", conn)

    cust_df = pd.read_sql_query("SELECT * FROM capstone_customer;", conn)

    payment_zipcode = pd.merge(pay_df, cust_df, left_on="customer_id", right_on="id")

    card_df = pd.read_sql_query("SELECT * FROM capstone_giftcard;", conn)

    company_df = pd.read_sql_query("SELECT * FROM capstone_company;", conn)

    company_card_df = pd.merge(card_df, company_df, left_on="company_id", right_on="id")

    payment_company_zip_df = pd.merge(payment_zipcode, company_card_df, left_on="giftcard_id", right_on="id_x")

    final_df = payment_company_zip_df[['payment_date', 'amount_donated', 'zipcode', 'id_y_y', 'name']]
    final_df = final_df.rename(columns={'id_y_y': 'company_id'})
    final_df = final_df[final_df.company_id==int(id_for_map)]
    final_df = final_df.groupby("zipcode")["amount_donated"].sum().reset_index()

    geo_df = pd.read_json("./data/USCities.json", orient="records")

    geo_df = geo_df[['latitude', 'longitude', 'zip_code', 'city']]

    latt_long_df = pd.merge(final_df, geo_df, left_on="zipcode", right_on="zip_code")

    base_map = folium.Map(location=[37.0902, -95.7129], control_scale=True, zoom_start=4.5)

    plugins.HeatMap(data=latt_long_df[['latitude', 'longitude', 'amount_donated']].groupby(['latitude', 'longitude']).sum().reset_index().values.tolist(),radius=18, max_zoom=13).add_to(base_map)

    mc = MarkerCluster()
    for idx,row in latt_long_df.iterrows():
        mc.add_child(folium.Marker(location=[row.latitude,  row.longitude], popup=f"{row.zipcode}: ${str(row.amount_donated)}"))

    base_map.add_child(mc)


    base_map.save('capstone/templates/report/gift_cards.html')


@login_required
def Map(request):
    customer = Customer.objects.get(pk=request.user.id)
    create_map(customer.company.id)
    if request.method == 'GET':
        template_name = 'report/gift_cards.html'
        return render(request, template_name, {})