import streamlit as st
from sqlalchemy import create_engine,text

def connect_db(dialect,username,password,host,dbname):
    #------------------------------------------------------------------------------------------------
    # ESERCIZIO 0 - CONNESSIONE AL DATABASE                                                         |
    #------------------------------------------------------------------------------------------------
    # Rimuovere la riga seguente e sostituirla con il codice per connettersi al database.           |
    # Usare la libreria SQLAlchemy.                                                                 |
    # La funzione deve restituire un oggetto di connessione valido.                                 |
    #------------------------------------------------------------------------------------------------
    raise NotImplementedError("Connessione al database non implementata.")

############################### NON MODIFICARE ###############################

# Controllare se la connessione al db è stata effettuata
def check_connection():
    if "connection" not in st.session_state.keys():
        st.session_state["connection"]=False

    if st.sidebar.button("Connettiti al Database"):
        try :
            myconnection=connect_db(dialect="mysql+pymysql",username="root",password="",host="localhost",dbname="hotel")
            st.session_state["connection"]=myconnection
        except Exception as e:
            st.session_state["connection"]=False
            st.sidebar.error(f"Errore nella connessione al DB: {e}")

    if st.session_state["connection"]:
        st.sidebar.badge("Connesso", icon=":material/check:", color="green")
        return True
    else:
        st.sidebar.badge("Non connesso", icon=":material/cancel:", color="red")
        return False

# Eseguire una query sul database
def execute_query(sql):
    conn = st.session_state["connection"]
    return conn.execute(text(sql))