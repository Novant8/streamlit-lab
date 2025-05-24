import streamlit as st
from utils.connection import *
import pandas as pd

def main():
    st.title("🏢 :blue[Agenzie]")
    col1,col2,col3=st.columns(3)
    if check_connection():
        
        #------------------------------------------------------------------------------------------------
        # ESERCIZIO 1.1 - METRICHE SULLE AGENZIE                                                        |
        #------------------------------------------------------------------------------------------------
        # Sostituire i valori None nelle variabili seguenti con i risultati delle query SQL richieste.  |
        # Per eseguire una query, usare la funzione execute_query(sql).                                 |
        # Esempio: execute_query("SELECT * FROM AGENZIA")                                               |
        #------------------------------------------------------------------------------------------------

        # Query 1 - Contare il numero totale di agenzie.
        agenzieN=None
        
        # Query 2 - Contare il numero di città in cui sono presenti agenzie.
        agenzieCity=None
        
        # Query 3 - Selezionare la città con il maggior numero di agenzie.
        city=None
        
        #################################################
        # Mostrare i risultati - NON MODIFICARE
        col1.metric("Numero di Agenzie",agenzieN.scalar() if agenzieN else "N/A")
        col2.metric("Numero di Città",agenzieCity.scalar() if agenzieN else "N/A")
        col3.metric("Città con più agenzie",city.scalar() if agenzieN else "N/A")
        #################################################

        #------------------------------------------------------------------------------------------------
        # ESERCIZIO 1.2 - FILTRO DELLE AGENZIE PER CITTÀ                                                |
        #------------------------------------------------------------------------------------------------
        # Modificare la query seguente in modo che soddisfi il filtro dell'utente salvato in cityName.  |
        # Se cityName è vuota, mostrare tutte le agenzie.                                               |
        #------------------------------------------------------------------------------------------------

        # La variabile cityName è una stringa che contiene il nome della città.
        cityName=st.text_input("Filtra per città")

        query = f"""
            SELECT CodA, Citta_Indirizzo, CONCAT(Via_Indirizzo,' ',Numero_Indirizzo) AS Indirizzo
            FROM AGENZIA
        """
        cityInfo=execute_query(query)
        
        #################################################
        # Mostrare i risultati - NON MODIFICARE
        df_info=pd.DataFrame(cityInfo or [])
        st.dataframe(df_info,use_container_width=True)
        #################################################
    else:
        st.error("Connessione al database non effettuata.")

if __name__ == "__main__":
    main()
    