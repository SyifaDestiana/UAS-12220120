 #Import DataFrame yang Dibutuhkan
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import streamlit as st


#Tampilan Configurasi  
st.set_page_config(page_title='UAS Syifa Destiana 12220120', page_icon=':computer:')
# Tittle Streamlit
header = '<p style="font-family:Oswald; color:Black; font-size: 50px; text-align=:center">Aplikasi Perhitungan Produksi Minyak Suatu Negara</p>'
st.markdown(header, unsafe_allow_html=True)

# Header
subheader = '<p style="font-family:Nanum Pen Script; color:Black; font-size: 15px; text-align=:center">Created by Syifa Destiana 12220120</p>'
st.markdown(subheader, unsafe_allow_html=True)

#Import Data yang ada
file = open("kode_negara_lengkap.json")
filejson= json.load(file)
dataj= pd.DataFrame.from_dict(filejson, orient='columns')
datacsv = pd.read_csv("C:/Users/Syifa Destiana/Documents/KULIAH/Prokom/produksi_minyak_mentah.csv")


json_file = open("C:/Users/Syifa Destiana/Documents/KULIAH/Prokom/kode_negara_lengkap.json")
json_data = json_file.read()
data_json = json.loads(json_data)

#Membuat list kode negara dan organisasi dari csv :
negara =[]
for i in list(datacsv['kode_negara']):
    if i not in negara:
        negara.append(i)

#Mencari list organisasi
organisasi = []
for i in negara:
    if i not in list(dataj['alpha-3']):
        organisasi.append(i)

#Menghapus/menghilangkan organisasi dari datacsv
for i in organisasi:
    datacsv = datacsv[datacsv.kode_negara!=i]
    if i in negara:
              negara.remove(i)

#Permasalahan A
X = st.text_input("Masukkan Nama Negara : ")

##Untuk Menuliskan Nama Negara Secara Lengkap(Bukan Kode)
isFound = False
i=0
codeX = ""
while not isFound and i < len(dataj):
    if data_json[i].get('name') == X:
        isFound = True
        codeX = data_json[i].get('alpha-3')
    i += 1


## Mengambil semua data negara yang diinput oleh user
data_a= datacsv.loc[datacsv['kode_negara'] == codeX]

##Memunculkan Grafik

grafik1=plt.subplot
data_a.plot(kind='line',x='tahun', y='produksi')
plt.title ("Produksi Minyak Negara {}".format(X), y=1.08) #Judul Grafik
grafik1=plt.show() #Memunculkan Grafik
st.pyplot(grafik1)

#Permasalahan B


tahun =[]
for i in list(datacsv['tahun']):
    if i not in tahun:
        tahun.append(i)


cola, colb = st.columns(2) #Tampilan Streamlit dengan 2 kolom
with cola:
    T=st.selectbox("Masukkan Tahun:", tahun)

T= int(T)

with colb:
    B=st.number_input("Masukkan Banyak Negara:", min_value= 1, key="B")

B= int(B)   

data_b= datacsv.loc[datacsv['tahun'] == T]
data_b= data_b.sort_values(['produksi'], ascending=False)#Mengurutkan Jumlah Produksi dari yang Terbesar

df1 = data_b[:B] #data b sampai ke B/banyak negara yang diinput(slicing)

##Buat Grafik Menggunakan Bar 

grafik2=plt.subplot
df1.plot(kind = "bar", x = 'kode_negara', y='produksi',stacked = True)
plt.title ("Top {} Negara Produksi Minyak Terbesar Pada Tahun {}". format(B,T), size=15, y=1.09)#Judul Grafik
grafik2=plt.show()
st.pyplot(grafik2)


#Permasalahan C
C = st.number_input("Masukkan Banyak Negara:", min_value= 1)
C=int(C)
listc=[] #list kosong untuk diisi negara
listkumulatif= [] #list kosong untuk diisi jumlah kumulatif produksi suatu negara

##looping untuk mendeteksi negara yang akan dihitung kumulatifnya
for i in list(datacsv['kode_negara']): 
    if i not in listc:
        listc.append(i)
        
##Looping penjumlahan kumulatif produksi untuk negara tertentu
for i in listc:
    data_c = datacsv.loc[datacsv['kode_negara'] == i, 'produksi'].sum()
    listkumulatif.append(data_c)

##Membuat list dari data_k dari 2 list(listc,listkumulatif) dan menyatukannya menggunakan zip
data_k = pd.DataFrame(list(zip(listc, listkumulatif)), columns=['kode_negara', 'kumulatif'])
data_k= data_k.sort_values(['kumulatif'], ascending=[0])#Mengurutkan Jumlah Produksi dari yang Terbesar
data_kumulatif = data_k[:C]

##Buat Grafik Menggunakan Bar Chart
grafik3=plt.subplot
data_kumulatif.plot(kind = "bar", x = 'kode_negara', y='kumulatif',stacked = True)
plt.title ("Top {} Negara dengan Jumlah Produksi Terbesar".format(C) , size=15, y=1.12) #Judul Grafik
grafik3=plt.show()
st.pyplot(grafik3)


#Permasalahan D

## kriteria 1 : informasi nama lengkap negara, kode negara, region, dan sub-region
##dengan jumlah produksi terbesar pada tahun T dan keseluruhan tahun

##Jumlah produksi terbesar pada tahun T
nama_negara = ""
region =""
subregion=""
jumlah_produksi = data_b[:1].iloc[0]['produksi']
kode_negara = data_b[:1].iloc[0]['kode_negara']


for i in range(len(dataj)):
    if list (dataj['alpha-3'])[i] == kode_negara :
             nama_negara=list(dataj['name'])[i]
             region=list(dataj['region'])[i]
             subregion=list(dataj['sub-region'])[i]


col1, col2 = st.columns(2)#Tampilan Streamlit dengan 2 kolom
with col1:
    st.markdown("## Negara dengan Jumlah Produksi Minyak Terbesar Pada Tahun {}".format(T)) 
    st.text("{}\n {}\n {}\n {}\n {}\n".format(jumlah_produksi,kode_negara,nama_negara,region,subregion))

## Jumlah Produksi Terbesar pada keseluruhan tahun T
nama_negara = ""
region =""
subregion=""
total_produksi = data_k[:1].iloc[0]['kumulatif']
kode_negara = data_k[:1].iloc[0]['kode_negara']

for i in range(len(dataj)):
    if list (dataj['alpha-3'])[i] == kode_negara :
             nama_negara=list(dataj['name'])[i]
             region=list(dataj['region'])[i]
             subregion=list(dataj['sub-region'])[i]


with col2:
   st.markdown("## Negara dengan  Jumlah Produksi Minyak Terbesar ")           
   st.text("{}\n {}\n {}\n {}\n {}\n".format(total_produksi,kode_negara,nama_negara,region,subregion))



##Kriteria 2 :nama lengkap negara,kode negara, region, dan sub-region dengan jumlah produksi terkecil (tidak sama dengan nol)
##pada tahun T dan keseluruhan tahun.

#Jumlah Produksi Terkecil pada Tahun T
dfterkecil = data_b[data_b.produksi != 0]
dfterkecil = dfterkecil.sort_values(by=['produksi'], ascending=True)

jumlah_produksi = dfterkecil[:1].iloc[0]['produksi']
kode_negara = dfterkecil[:1].iloc[0]['kode_negara']
nama_negara = ""
region_negara = ""
subregion_negara = ""

for i in range(len(dataj)):
    if list(dataj['alpha-3'])[i] == kode_negara:
        nama_negara = list(dataj['name'])[i]
        region_negara = list(dataj['region'])[i]
        subregion_negara = list(dataj['sub-region'])[i]
col3, col4 = st.columns(2)#Tampilan Streamlit dengan 2 kolom
with col3:
   st.markdown("## Negara dengan Jumlah Produksi Minyak Terkecil pada Tahun {}".format(T))#Judul Kriteria         
   st.text("{}\n {}\n {}\n {}\n {}\n".format(jumlah_produksi,kode_negara,nama_negara,region,subregion))
#Jumlah Produksi Terkecil pada keseluruhan tahun 
datakmin=data_k[data_k.kumulatif != 0]
datakmin=datakmin.sort_values(by=['kumulatif'], ascending=True)

nama_negara = ""
region =""
subregion=""
jumlah_produksi = datakmin[:1].iloc[0]['kumulatif']
kode_negara = datakmin[:1].iloc[0]['kode_negara']

for i in range(len(dataj)):
    if list (dataj['alpha-3'])[i] == kode_negara :
             nama_negara=list(dataj['name'])[i]
             region=list(dataj['region'])[i]
             subregion=list(dataj['sub-region'])[i]


with col4:
    st.markdown("## Negara dengan  Jumlah Produksi Minyak Terkecil ")#Judul Kriteria          
    st.text("{}\n {}\n {}\n {}\n {}\n".format(jumlah_produksi,kode_negara,nama_negara,region,subregion))

##Kriteria 3 : nama lengkap negara, kode negara, region, dan
##sub-region dengan jumlah produksi sama dengan nol pada tahun T dan keseluruhan tahun

#Produksi nol pada tahun T
dataproduksinol=data_b[data_b['produksi'] == 0]

produksinol=[]
regionnol=[]
subregionnol=[]

for i in range(len(dataproduksinol)):
    for j in range(len(dataj)):
        if list(dataproduksinol['kode_negara'])[i] == list(dataj['alpha-3'])[j]:
            produksinol.append(list(dataj['name'])[j])
            regionnol.append(list(dataj['region'])[j])
            subregionnol.append(list(dataj['sub-region'])[j])

dataproduksinol['negara']=produksinol
dataproduksinol['region']=regionnol
dataproduksinol['sub-region']=subregionnol

st.markdown("## Tabel Negara dengan  Jumlah Produksi Minyak Nol Pada Tahun {}".format(T))#Judul Tabel
st.dataframe(dataproduksinol)

#Produksi nol pada keseluruhan tahun 
datakumulatifnol=data_k[data_k.kumulatif ==0]
kumulatifproduksinol=[]
kumulatifregionnol=[]
kumulatifsubregionnol=[]

for i in range(len(datakumulatifnol)):
    for j in range(len(dataj)):
        if list(datakumulatifnol['kode_negara'])[i] == list(dataj['alpha-3'])[j]:
            kumulatifproduksinol.append(list(dataj['name'])[j])
            kumulatifregionnol.append(list(dataj['region'])[j])
            kumulatifsubregionnol.append(list(dataj['sub-region'])[j])

datakumulatifnol['negara']=kumulatifproduksinol
datakumulatifnol['region']=kumulatifregionnol
datakumulatifnol['sub-region']=kumulatifsubregionnol

st.markdown("## Tabel Negara dengan  Jumlah Produksi Minyak Nol Pada Keseluruhan Tahun") #Judul Tabel
st.table(datakumulatifnol)

st.set_option('deprecation.showPyplotGlobalUse', False)
