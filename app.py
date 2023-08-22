import streamlit as st
import pandas as pd
import plotly.express as px

st. set_page_config(
   layout="wide",
   page_title="Rekapitulasi Perkara Mahkamah Syariah Kota Langsa",
)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        .css-z5fcl4{
            padding-top: 1em !important;
        }
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

def load_data():
   data = pd.read_csv("dataset/ms-langsa.csv", sep=";")
   data['Jumlah'] = data.groupby(['Klasifikasi Perkara', 'Tahun'])['Klasifikasi Perkara'].transform('count')
   data = data[["Klasifikasi Perkara", "Tahun", "Jumlah"]]
   data = data.drop_duplicates()
   return data

@st.cache_data
def get_data():
    return load_data()

# Mendapatkan data dari cache
data = get_data()


st.title("Rekapitulasi Perkara Mahkamah Syariah Kota Langsa")
st.markdown('App dikembangkan oleh :blue [syukriyansyah]((www.linkedin.com/in/syukriyansyah) dengan menggunakan data yang dikumpulkan secara otomatis menggunakan tehnik scraping pada website :blue [Mahkamah Syariah Kota Langsa](http://sipp.pn-langsa.go.id/list_perkara/search).')

st.markdown("<br/>",unsafe_allow_html=True)

col1, col2 = st.columns([1,3])

with col1:
   with st.spinner('Memuat data...'):
      # Menampilkan hasil pemrosesan data
      years = (list(data["Tahun"].drop_duplicates()))
      year_selected = st.multiselect(
         'Tahun:',
         years,
         key="year"
      )

with col2:
   # with st.spinner('Memuat data...'):
      if year_selected == []:
         types = list(data["Klasifikasi Perkara"].drop_duplicates())
      else:
         types = list(data["Klasifikasi Perkara"][data["Tahun"].isin(list(year_selected))].drop_duplicates())

      type_selected = st.multiselect(
         'Jenis Perkara:',
         types,
         key="type"
      )
   
   

if year_selected == []:
   if type_selected == []:
      fig = px.line(data, x="Tahun", y="Jumlah", color='Klasifikasi Perkara', text="Jumlah", symbol="Klasifikasi Perkara")
      fig.update_traces(textposition="top center")
      fig.update_layout(legend=dict(orientation='h', y=-0.2))
      st.plotly_chart(fig, theme="streamlit", use_container_width=True)
   else:
      data_df = data[data["Klasifikasi Perkara"].isin(list(type_selected))]

      fig = px.line(data_df, x="Tahun", y="Jumlah", color='Klasifikasi Perkara', text="Jumlah", symbol="Klasifikasi Perkara")
      fig.update_traces(textposition="top center")
      fig.update_layout(legend=dict(orientation='h', y=-0.2))
      st.plotly_chart(fig, theme="streamlit", use_container_width=True)
else:
   if type_selected == []:
      data_df = data[data["Tahun"].isin(list(year_selected))]

      fig = px.line(data_df, x="Tahun", y="Jumlah", color='Klasifikasi Perkara', text="Jumlah", symbol="Klasifikasi Perkara")
      fig.update_traces(textposition="top center")
      fig.update_layout(legend=dict(orientation='h', y=-0.2))
      st.plotly_chart(fig, theme="streamlit", use_container_width=True)
   else:
      data_df = data[data["Tahun"].isin(list(year_selected))]
      data_df = data_df[data_df["Klasifikasi Perkara"].isin(list(type_selected))]

      fig = px.line(data_df, x="Tahun", y="Jumlah", color='Klasifikasi Perkara', text="Jumlah", symbol="Klasifikasi Perkara")
      fig.update_traces(textposition="top center")
      fig.update_layout(legend=dict(orientation='h', y=-0.2))
      st.plotly_chart(fig, theme="streamlit", use_container_width=True)

st.markdown("<p style='text-align:center; margin-top:8em'><b>LinkedIn:</b> :blue [syukriyansyah](www.linkedin.com/in/syukriyansyah) | <b>Email:</b> :blue syukrieyansyah@gmail.com | <b>Instagram:</b> :blue [syukriyansyah_] (https://www.instagram.com/syukriyansyah_/)</p>", unsafe_allow_html=True)
