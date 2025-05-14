import streamlit as st
from utils.connection import *
import pandas as pd

def main():
    st.title("💸 :blue[Prenotazioni]")
    if check_connection():
        #------------------------------------------------------------------------------------------------
        # ESERCIZIO 3 - COSTI DELLE PRENOTAZIONI                                                        |
        #------------------------------------------------------------------------------------------------
        # Per ciascun mese dell'anno 2023, visualizzare il codice ed il costo medio giornaliero della   |
        # stanza con il costo medio giornaliero più alto. Ordinare i risultati per mese, in ordine      |
        # crescente.                                                                                    |
        #                                                                                               |
        # NOTA                                                                                          |
        # Per permettere la corretta visualizzazione del grafico, il risultato deve contenere           |
        # obbligatoriamente dei campi chiamati "Mese" e "MediaGiornaliera".                             |
        #                                                                                               |
        # SUGGERIMENTI                                                                                  |
        # - Per estrarre giorno, mese e anno dalle date, è possibile utilizzare le funzioni DAY(Data),  |
        # MONTH(Data) e YEAR(Data) di MySQL.                                                            |
        # - Per calcolare la differenza tra due date, è possibile utilizzare la funzione                |
        # DATEDIFF(Data1, Data2) di MySQL.                                                              |
        #------------------------------------------------------------------------------------------------
        result=execute_query("""
            WITH COSTI_MENSILI AS ( 
                SELECT STANZA_CodS, MONTH(DataInizio) AS Mese, 
                        Costo/(DATEDIFF(DataFine, DataInizio)) AS CostoGiornaliero 
                FROM PRENOTAZIONE
                WHERE YEAR(DataInizio) = 2023
            ), 
            COSTI_MENSILI_RAGGRUPPATI AS ( 
                SELECT Mese, STANZA_CodS, AVG(CostoGiornaliero) AS MediaGiornaliera 
                FROM COSTI_MENSILI 
                GROUP BY Mese, STANZA_CodS
            ), 
            COSTI_MENSILI_MAX AS ( 
                SELECT Mese, MAX(MediaGiornaliera) AS MediaGiornalieraMax 
                FROM COSTI_MENSILI_RAGGRUPPATI
                GROUP BY Mese 
            )
            SELECT CMR.Mese, CMR.STANZA_CodS, CMR.MediaGiornaliera
            FROM COSTI_MENSILI_RAGGRUPPATI CMR, COSTI_MENSILI_MAX CMM
            WHERE CMR.Mese = CMM.Mese AND CMR.MediaGiornaliera = CMM.MediaGiornalieraMax
            ORDER BY CMR.Mese ASC
        """)
        
        #################################################
        # Mostrare i risultati - NON MODIFICARE
        if result is not None:
            df=pd.DataFrame(result)
            st.dataframe(df)
            if "Mese" in df.columns and "MediaGiornaliera" in df.columns:
                st.line_chart(df,x="Mese",y="MediaGiornaliera")
            else:
                st.error("Per visualizzare il grafico, il risultato deve contenere i campi 'Mese' e 'MediaGiornaliera'.")
        else:
            st.error("Query SQL non implementata.")
        #################################################
    else:
        st.error("Connessione al database non effettuata.")

if __name__ == "__main__":
    main()