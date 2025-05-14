import streamlit as st
from utils.connection import *
import pandas as pd

############################### NON MODIFICARE ###############################

def main():
    st.title("🛎 :blue[Stanze]")
    if check_connection():
        #------------------------------------------------------------------------------------------------
        # ESERCIZIO 2 - FILTRO DELLE STANZE                                                             |
        #------------------------------------------------------------------------------------------------
        # Selezionare il codice, il piano, la superficie, ed il tipo delle stanze che soddisfano i      |
        # filtri selezionati dall'utente.                                                               |
        #                                                                                               |
        # NOTA                                                                                          |
        # Per permettere il funzionamento dell'interfaccia, non modificare il nome delle colonne        |
        # restituite dalla query.                                                                       |
        #                                                                                               |
        # SUGGERIMENTO                                                                                  |
        # Costruire le condizioni di WHERE in modo incrementale, aggiungendole man mano alla query SQL. |
        #------------------------------------------------------------------------------------------------
        with st.expander("Filtri", expanded=True):
            col1,col2,_=st.columns(3)

            # tipo è una stringa che contiene un valore tra "Singola","Doppia","Tripla","Tutte".
            # Suggerimento: attenzione alle maiuscole/minuscole!
            tipo=col1.radio("Tipo di stanza",["Singola","Doppia","Tripla","Tutte"], index=3)

            # optional contine una *lista* di stringhe che rappresentano gli optional selezionati dall'utente.
            optional=col2.multiselect("Optional:", get_list("OPTIONAL_Optional","HAS_OPTIONAL"))
            
            # cucina è una booleana che indica se l'utente vuole visualizzare solo le stanze con cucina.
            cucina=col2.checkbox("Voglio la cucina",value=False)

        query = f"""
            SELECT DISTINCT CodS,Piano,Superficie,Type
            FROM STANZA
                LEFT JOIN HAS_OPTIONAL ON STANZA.CodS=HAS_OPTIONAL.STANZA_CodS
                LEFT JOIN HAS_SPAZI ON STANZA.CodS=HAS_SPAZI.STANZA_CodS
        """

        # Utilizzare la clausola WHERE per la prima condizione, AND per le successive (se presenti)
        clausola = "WHERE"

        # Filtro sul tipo
        if tipo != "Tutte":
            query += f" {clausola} STANZA.Type='{tipo.lower()}'"
            clausola = "AND"

        # Filtro sugli optional
        group_by = ""
        if len(optional) > 0:
            optional_sql = ",".join(f"'{o}'" for o in optional)
            query += f" {clausola} HAS_OPTIONAL.OPTIONAL_Optional IN ({optional_sql})"
            clausola = "AND"

            # Vogliamo che le stanze mostrate contengano *tutti* gli optional richiesti dall'utente.
            if len(optional) > 1:
                group_by = f"GROUP BY CodS,Piano,Superficie,Type HAVING COUNT(*) = {len(optional)}"

        # Filtro sulla cucina
        if cucina:
            query += f" {clausola} HAS_SPAZI.SPAZI_Spazi='cucina'"

        query += group_by

        result=execute_query(query)
        
        #################################################
        # Mostrare i risultati - NON MODIFICARE
        df=pd.DataFrame(result or [])
        if len(df.columns) > 0:
            if len(df) > 0:
                for index,row in df.iterrows():
                    show_room(row["CodS"],row["Piano"],row["Superficie"],row["Type"])
            else:
                st.warning("Nessuna stanza trovata.")
        #################################################
    else:
        st.error("Connessione al database non effettuata.")

############################### NON MODIFICARE ###############################

def get_list(attributo,tabella):
    query=f"SELECT DISTINCT {attributo} FROM {tabella}"
    result=execute_query(query)
    result_list=[]
    for row in result.mappings():
        result_list.append(row[attributo])
    return result_list

def first_upper(string):
    return string[0].upper()+string[1:]

def show_room(cod,piano,superficie,tipo):
    st.subheader(f":green[Stanza #{cod}]")
    
    col1,col2,col3=st.columns(3)
    col1.write(f"**Tipo**: {first_upper(tipo)}")
    col1.write(f"**Piano**: {piano}")
    col1.write(f"**Superficie**: {superficie} m²")

    col2.write("**Spazi**:")
    spazi=execute_query(f"SELECT DISTINCT SPAZI_Spazi FROM HAS_SPAZI WHERE STANZA_CodS='{cod}'").all()
    if len(spazi) > 0:
        for row in spazi:
            col2.write(f"- {first_upper(row[0])}")
    else:
        col2.write("*Nessuno spazio.*")

    col3.write("**Optional**:")
    optional=execute_query(f"SELECT DISTINCT OPTIONAL_Optional FROM HAS_OPTIONAL WHERE STANZA_CodS='{cod}'").all()
    if len(optional) > 0:
        for row in optional:
            col3.write(f"- {first_upper(row[0])}")
    else:
        col3.write("*Nessun optional.*")

    st.divider()

if __name__ == "__main__":
    main()