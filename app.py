import streamlit as st
import pandas as pd
import plotly.express as px

import functions

st.set_page_config(layout = "wide", page_icon = 'Melita Handayani.png', page_title='Hyhy')

st.header("Analisis Data Eksplorasi")

st.write('<p style="font-size:160%">You will be able to✅:</p>', unsafe_allow_html=True)

st.write('<p style="font-size:100%">&nbsp 1. Mencari file yang terdapat banyak kumpulan data</p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 2. Mendapatkan nama data dan info tipe data</p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 3. Mendapatkan hitungan dan persentase nilai dari NA</p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 4. Mendapatkan deskripsi dari analisis </p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 5. Memeriksa ketidakseimbangan atau distribusi variabel target:</p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 6. Mengetahui distribusi dari kolom numerik</p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 7. Menghitung plot kolom kategori</p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 8. Mendapatkan data outlier dari boxplot</p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 9. Mendapatkan info varians nilai target dengan kolom kategorikal</p>', unsafe_allow_html=True)
#st.image('header2.png', use_column_width = True)

functions.space()
st.write('<p style="font-size:130%">Impor File</p>', unsafe_allow_html=True)

file_format = st.radio('Pilih Format File:', ('csv', 'excel'), key='file_format')
dataset = st.file_uploader(label = 'Choose a file')

use_defo = st.checkbox('Gunakan contoh dataset')
if use_defo:
    dataset = 'CarPrice_Assignment.csv'

st.sidebar.header('Impor File Dataset untuk Menggunakan Fitur yang Tersedia: 👉')

if dataset is not None:
    if file_format == 'csv' or use_defo:
        df = pd.read_csv(dataset)
    else:
        df = pd.read_excel(dataset)
    
    st.subheader('Dataframe:')
    n, m = df.shape
    st.write(f'<p style="font-size:130%">Dataset contains {n} rows and {m} columns.</p>', unsafe_allow_html=True)   
    st.write(df)


    all_vizuals = ['Info', 'NA Info', 'Analisis Deskripsi', 'Analisis Target', 
                   'Distribusi dari Kolom Numerik', 'Grafik Jumlah Data pada Kolom Kategori', 
                   'Box Plots', 'Data Outlier', 'Varian Target dengan Kolom Kategori']
    functions.sidebar_space(3)         
    vizuals = st.sidebar.multiselect("Pilih visualisasi yang ingin dilihat 👇", all_vizuals)

    if 'Info' in vizuals:
        st.subheader('Info:')
        c1, c2, c3 = st.columns([1, 2, 1])
        c2.dataframe(functions.df_info(df))

    if 'NA Info' in vizuals:
        st.subheader('Informasi Nilai NA:')
        if df.isnull().sum().sum() == 0:
            st.write('Tidak ada nilai NA dalam dataset Anda.')
        else:
            c1, c2, c3 = st.columns([0.5, 2, 0.5])
            c2.dataframe(functions.df_isnull(df), width=1500)
            functions.space(2)
            

    if 'Analisis Deskripsi' in vizuals:
        st.subheader('Analisis Deskripsi:')
        st.dataframe(df.describe())
        
    if 'Analisis Target' in vizuals:
        st.subheader("Pilih Kolom Target:")    
        target_column = st.selectbox("", df.columns, index = len(df.columns) - 1)
    
        st.subheader("Histogram dari Kolom Target")
        fig = px.histogram(df, x = target_column)
        c1, c2, c3 = st.columns([0.5, 2, 0.5])
        c2.plotly_chart(fig)


    num_columns = df.select_dtypes(exclude = 'object').columns
    cat_columns = df.select_dtypes(include = 'object').columns

    if 'Distribusi dari Kolom Numerik' in vizuals:

        if len(num_columns) == 0:
            st.write('Tidak ada kolom numerik dalam data tersebut.')
        else:
            selected_num_cols = functions.sidebar_multiselect_container('Pilih kolom untuk distribusi plots:', num_columns, 'Ditribusi')
            st.subheader('Distribusi dari Kolom Numerik')
            i = 0
            while (i < len(selected_num_cols)):
                c1, c2 = st.columns(2)
                for j in [c1, c2]:

                    if (i >= len(selected_num_cols)):
                        break

                    fig = px.histogram(df, x = selected_num_cols[i])
                    j.plotly_chart(fig, use_container_width = True)
                    i += 1

    if 'Grafik Jumlah Data pada Kolom Kategori' in vizuals:

        if len(cat_columns) == 0:
            st.write('Tidak ada kategori kolom pada data anda.')
        else:
            selected_cat_cols = functions.sidebar_multiselect_container('Pilih kolom-kolom untuk grafik Jumlah Data:', cat_columns, 'Jumlah')
            st.subheader('Grafik Jumlah Data pada Kolom Kategori')
            i = 0
            while (i < len(selected_cat_cols)):
                c1, c2 = st.columns(2)
                for j in [c1, c2]:

                    if (i >= len(selected_cat_cols)):
                        break

                    fig = px.histogram(df, x = selected_cat_cols[i], color_discrete_sequence=['pink'])
                    j.plotly_chart(fig)
                    i += 1

    if 'Box Plots' in vizuals:
        if len(num_columns) == 0:
            st.write('Tidak ada kolom numerik pada data anda.')
        else:
            selected_num_cols = functions.sidebar_multiselect_container('Pilih kolom untuk data boxplots:', num_columns, 'Box')
            st.subheader('Box plots')
            i = 0
            while (i < len(selected_num_cols)):
                c1, c2 = st.columns(2)
                for j in [c1, c2]:
                    
                    if (i >= len(selected_num_cols)):
                        break
                    
                    fig = px.box(df, y = selected_num_cols[i])
                    j.plotly_chart(fig, use_container_width = True)
                    i += 1

    if 'Analisis Outlier' in vizuals:
        st.subheader('Analisis Outlier')
        c1, c2, c3 = st.columns([1, 2, 1])
        c2.dataframe(functions.number_of_outliers(df))

    if 'Varian Target dengan Kolom Kategori' in vizuals:
        
        
        df_1 = df.dropna()
        
        high_cardi_columns = []
        normal_cardi_columns = []

        for i in cat_columns:
            if (df[i].nunique() > df.shape[0] / 10):
                high_cardi_columns.append(i)
            else:
                normal_cardi_columns.append(i)


        if len(normal_cardi_columns) == 0:
            st.write('Tidak ada kolom kategorikal dengan kardinalitas normal dalam data tersebut.')
        else:
        
            st.subheader('Varian Target dengan Kolom Kategori')
            model_type = st.radio('Pilih Tipe Masalah:', ('Regresi', 'Klasifikasi'), key = 'model_type')
            selected_cat_cols = functions.sidebar_multiselect_container('Pilih kolom-kolom untuk grafik dengan Warna Kategori:', normal_cardi_columns, 'Kategori')
            
            if 'Analisis Target' not in vizuals:   
                target_column = st.selectbox("Pilih Target Kolom:", df.columns, index = len(df.columns) - 1)
            
            i = 0
            while (i < len(selected_cat_cols)):
                
                
            
                if model_type == 'Regresi':
                    fig = px.box(df_1, y = target_column, color = selected_cat_cols[i])
                else:
                    fig = px.histogram(df_1, color = selected_cat_cols[i], x = target_column)

                st.plotly_chart(fig, use_container_width = True)
                i += 1

            if high_cardi_columns:
                if len(high_cardi_columns) == 1:
                    st.subheader('Kolom berikut memiliki kardinalitas tinggi, itulah sebabnya boxplotnya tidak digambarkan:')
                else:
                    st.subheader('Kolom-kolom berikut memiliki kardinalitas tinggi, itulah sebabnya boxplotnya tidak digambarkan:')
                for i in high_cardi_columns:
                    st.write(i)
                
                st.write('<p style="font-size:140%">Apakah Anda ingin tetap membuat plotnya??</p>', unsafe_allow_html=True)    
                answer = st.selectbox("", ('Tidak', 'Iya'))

                if answer == 'Iya':
                    for i in high_cardi_columns:
                        fig = px.box(df_1, y = target_column, color = i)
                        st.plotly_chart(fig, use_container_width = True)
