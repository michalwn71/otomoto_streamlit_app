import streamlit as st
# import joblib
import pandas as pd
import pickle
import xgboost as xgb

#Data prep

with open('col_values_dict.pickle', 'rb') as f:
        col_values_dict =  pickle.load(f)

# print(col_values_dict)

# otomoto_data = pd.read_pickle('data\otomoto_data.pickle')


# quit

# #Webpage
st.header("**Predykcja wartości pojazdu na podstawie danych z [OtoMoto.pl](https://www.otomoto.pl/)**")
st.write("Model wytrenowany na podstawie **115853** ogłoszeń")
st.write("Aktualny średni błąd modelu: **8771** [PLN]")
st.write("")



col1, col2, col3 = st.columns(3)

marka = col1.selectbox("Marka samochodu",col_values_dict['Marki'])

model = col2.selectbox("Model samochodu",col_values_dict['Model'])

rok_prod = col3.slider('Rok produkcji', 1950, 2022, 2000)

przebieg = col1.number_input("Aktualny przebieg", step=1, min_value=0)

pojemn_skok = col2.number_input("Pojemność silnika (w cm3)", step=1, min_value=0, max_value=10000)

moc = col3.number_input("Moc silnika (w km)", step=1, min_value=0, max_value=10000)

licz_drzwi = col1.number_input("Liczba drzwi", step=1, min_value=0, max_value=7)

licz_miejsc = col2.number_input("Liczba miejsc", step=1, min_value=0, max_value=10)

paliwo = col3.selectbox("Rodzaj paliwa",col_values_dict['Paliwo'])

naped = col1.selectbox("Rodzaj napędu",col_values_dict['Napęd'])

typ_nadw = col2.selectbox("Typ nadwozia",col_values_dict['Typ nadwozia'])

kolor = col3.selectbox("Kolor",col_values_dict['Kolor'])

oferta_od = col1.selectbox("Oferta od",col_values_dict['Oferta od'])

skrzynia = col2.selectbox("Skrzynia biegów",col_values_dict['Skrzynia'])

stan = col3.selectbox("Stan samochodu",col_values_dict['Stan'])

wypos = st.multiselect(
     'Wyposarzenie dodatkowe',
     col_values_dict['Wyposazenie'])

# st.button('Predykcja')

# Predykcja

with open('data\otomoto_data_one_col.pickle', 'rb') as f:
        otomoto_data_one_col =  pickle.load(f)

df_pred = pd.DataFrame(columns=[x for x in otomoto_data_one_col.columns if x != 'price'])
df_pred.loc[len(df_pred)] = 0

df_input = pd.DataFrame([[marka,model,rok_prod,przebieg,pojemn_skok,moc,licz_drzwi,
                    licz_miejsc,paliwo,naped,typ_nadw,kolor,oferta_od,skrzynia,stan,wypos]], 
                    columns=['marka','model','rok_prod','przebieg','pojemn_skok','moc','licz_drzwi','licz_miejsc','paliwo','naped',
                    'typ_nadw','kolor','oferta_od','skrzynia','stan','wypos'])



input_marka = 'Marka pojazdu_' + df_input['marka'][0]
df_pred.iloc[0][input_marka] = 1

input_model = 'Model pojazdu_' + df_input['model'][0]
df_pred.iloc[0][input_model] = 1

input_rok_prod = df_input['rok_prod'][0]
df_pred.iloc[0]['Rok produkcji'] = input_rok_prod

input_przebieg = df_input['przebieg'][0]
df_pred.iloc[0]['Przebieg'] = input_przebieg

input_pojen_skok = df_input['pojemn_skok'][0]
df_pred.iloc[0]['Pojemność skokowa'] = input_pojen_skok

input_moc = df_input['moc'][0]
df_pred.iloc[0]['Moc'] = input_moc

input_licz_drzwi = df_input['licz_drzwi'][0]
df_pred.iloc[0]['Liczba drzwi'] = input_licz_drzwi

input_licz_miejsc = df_input['licz_miejsc'][0]
df_pred.iloc[0]['Liczba miejsc'] = input_licz_miejsc

input_paliwo = 'Rodzaj paliwa_' + df_input['paliwo'][0]
df_pred.iloc[0][input_paliwo] = 1

input_naped = 'Napęd_' + df_input['naped'][0]
df_pred.iloc[0][input_naped] = 1

input_typ_nadw = 'Typ nadwozia_' + df_input['typ_nadw'][0]
df_pred.iloc[0][input_typ_nadw] = 1

input_kolor = 'Kolor_' + df_input['kolor'][0]
df_pred.iloc[0][input_kolor] = 1

input_oferta_od = 'Oferta od_' + df_input['oferta_od'][0]
df_pred.iloc[0][input_oferta_od] = 1

input_skrzynia = 'Skrzynia biegów_' + df_input['skrzynia'][0]
df_pred.iloc[0][input_skrzynia] = 1

input_stan = 'Stan_' + df_input['stan'][0]
df_pred.iloc[0][input_stan] = 1

input_wypos = df_input['wypos'].iloc[0]
# df_pred.iloc[0][input_kolor] = 1
if len(input_wypos) == 0:
     pass
else:
     for i in input_wypos:
          df_pred[i].iloc[0] = 1

if st.button('Predykcja'):
     # st.write(df_pred[[input_marka, input_model, 'Rok produkcji', 'Przebieg',
     # 'Pojemność skokowa', 'Moc', 'Liczba drzwi', 'Liczba miejsc', input_paliwo, 
     # input_naped, input_typ_nadw, input_kolor, input_oferta_od, input_skrzynia, 
     # input_stan, ]])
     # st.write(df_pred)
     # st.write(len(input_wypos))
     model_xgb = xgb.Booster()
     model_xgb.load_model("models/model_xgboost_ntree.json")

     # st.write(model_xgb.predict(xgb.DMatrix(df_pred.values)))
     preds_xgboost = model_xgb.predict(xgb.DMatrix(df_pred), ntree_limit=100)
     st.subheader("Wg modelu XGBoost, samochód jest wart ok. ")
     st.header('**'+str(int(preds_xgboost[0]))+'**' + ' PLN')

# model_xgb = xgb.Booster()
# model_xgb.load_model("models/model_xgb.txt")

# model_xgb.predict