import streamlit as st
import pandas as pd
from datetime import datetime

# Inicializace databáze (pokud neexistuje, vytvoří se prázdný DataFrame)
if "matches" not in st.session_state:
    st.session_state.matches = pd.DataFrame(columns=["Datum", "Domácí tým", "Hostující tým", "Skóre domácí", "Skóre hosté"])

st.title("NHL Záznam Zápasů")

# Formulář pro zadání zápasu
st.header("Přidat nový zápas")
date = st.date_input("Datum zápasu", datetime.today())
home_team = st.text_input("Domácí tým")
away_team = st.text_input("Hostující tým")
home_score = st.number_input("Skóre domácího týmu", min_value=0, step=1)
away_score = st.number_input("Skóre hostujícího týmu", min_value=0, step=1)

if st.button("Uložit zápas"):
    new_match = pd.DataFrame({
        "Datum": [date],
        "Domácí tým": [home_team],
        "Hostující tým": [away_team],
        "Skóre domácí": [home_score],
        "Skóre hosté": [away_score]
    })
    st.session_state.matches = pd.concat([st.session_state.matches, new_match], ignore_index=True)
    st.success("Zápas byl uložen!")

# Zobrazení uložených zápasů
st.header("Historie zápasů")
st.dataframe(st.session_state.matches)

# Výběr týmů pro porovnání
st.header("Porovnání dvou týmů")
team1 = st.selectbox("Vyberte první tým", st.session_state.matches["Domácí tým"].unique())
team2 = st.selectbox("Vyberte druhý tým", st.session_state.matches["Hostující tým"].unique())

if st.button("Vyhodnotit"):
    subset = st.session_state.matches[((st.session_state.matches["Domácí tým"] == team1) & (st.session_state.matches["Hostující tým"] == team2)) |
                                      ((st.session_state.matches["Domácí tým"] == team2) & (st.session_state.matches["Hostující tým"] == team1))]
    
    st.write(f"Celkový počet vzájemných zápasů: {len(subset)}")
    st.dataframe(subset)
