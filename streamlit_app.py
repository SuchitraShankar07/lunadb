import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import date
import pandas as pd


st.set_page_config(page_title="LunaDB UI", layout="wide")

# Inject full-page background GIF
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url('https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcG9kZ2NnbGVkNGRuYnBzemtrd2sydzExcWF4MmYyb3F3enVqa3RqbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/FlodpfQUBSp20/giphy.gif');
        background-size: cover;
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
        background-position: center;
        background-repeat: repeat;
        background-attachment: fixed;
    }
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.7);
        z-index: -1;
        pointer-events: none;
    }
    
    /* Dark theme global styles */
    .stApp {
        color: #e8e8e8;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* All text inputs, text areas, and number inputs */
    input, textarea, [data-baseweb="select"] {
        background-color: rgba(30, 30, 30, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Date inputs */
    [data-baseweb="input"] input {
        background-color: rgba(30, 30, 30, 0.8) !important;
        color: #ffffff !important;
    }
    
    /* Dropdowns/select boxes */
    [data-baseweb="select"] > div {
        background-color: rgba(30, 30, 30, 0.8) !important;
        color: #ffffff !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #1e40af, #2563eb) !important;
    }
    
    /* Form submit buttons */
    .stFormSubmitButton > button {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6) !important;
        color: #ffffff !important;
        border: none !important;
    }
    
    /* Dataframes */
    [data-testid="stDataFrame"] {
        background-color: rgba(20, 20, 20, 0.9) !important;
    }
    
    [data-testid="stDataFrame"] table {
        color: #ffffff !important;
    }
    
    [data-testid="stDataFrame"] th {
        background-color: rgba(30, 58, 138, 0.8) !important;
        color: #ffffff !important;
    }
    
    [data-testid="stDataFrame"] td {
        background-color: rgba(30, 30, 30, 0.8) !important;
        color: #e8e8e8 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(20, 20, 20, 0.6);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #a0a0a0 !important;
        background-color: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        background-color: rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Success/Error/Warning/Info boxes */
    .stSuccess, .stError, .stWarning, .stInfo {
        background-color: rgba(20, 20, 20, 0.8) !important;
        color: #ffffff !important;
    }
    
    /* Expanders */
    [data-testid="stExpander"] {
        background-color: rgba(30, 30, 30, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Sidebar dark theme */
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 10, 0.85) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #e8e8e8 !important;
    }
    
    /* Labels and small text */
    label, .stMarkdown p {
        color: #d0d0d0 !important;
    }
    
    /* Horizontal rules */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)


def connect_db(host, port, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            autocommit=False
        )
        return conn
    except Error as e:
        st.error(f"Connection error: {e}")
        return None


def run_query(conn, query, params=None, fetch=True):
    try:
        cur = conn.cursor()
        cur.execute(query, params or ())
        
        if fetch:
            cols = [c[0] for c in cur.description] if cur.description else []
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=cols) if rows and cols else pd.DataFrame(rows)
            
            # For stored procedures, consume additional result sets
            if query.strip().upper().startswith('CALL'):
                try:
                    while cur.nextset():
                        pass
                except Exception:
                    pass
            
            return df
        else:
            # For stored procedures, consume all result sets
            if query.strip().upper().startswith('CALL'):
                try:
                    while cur.nextset():
                        pass
                except Exception:
                    pass
            
            conn.commit()
            return None
    except Error as e:
        raise
    finally:
        try:
            cur.close()
        except:
            pass


def safe_call(conn, query, params=None):
    try:
        cur = conn.cursor()
        cur.execute(query, params or ())
        
        # For stored procedures, try to fetch results if available
        df = None
        try:
            # Check if there are results to fetch
            if cur.description:
                cols = [c[0] for c in cur.description]
                rows = cur.fetchall()
                if rows and cols:
                    df = pd.DataFrame(rows, columns=cols)
        except Exception:
            # Some procedures don't return results
            df = None
        
        # Consume any additional result sets
        try:
            while cur.nextset():
                pass
        except Exception:
            pass
            
        conn.commit()
        return df
    except Error as e:
        raise
    finally:
        try:
            cur.close()
        except:
            pass


def load_small_list(conn, query):
    try:
        df = run_query(conn, query)
        if df is None or df.empty:
            return []
        return df.iloc[:, 0].tolist()
    except Exception:
        return []


st.title("LunaDB")

with st.sidebar:
    # sidebar CSS to style the connection form
    st.markdown(
        """
        <style>
        /* Sidebar container tweaks */
        [data-testid="stSidebar"] .css-1d391kg {padding-top: 8px;
        background-color: rgba(0,0,0,0.5) !important;
        }
        /* Style inputs and text areas in the sidebar */
        [data-testid="stSidebar"] input, [data-testid="stSidebar"] textarea {
            background: rgba(255,255,255,0.04) !important;
            color: #fff !important;
            border-radius: 6px !important;
            padding: 8px !important;
        }
        /* Style the submit button in the sidebar form */
        [data-testid="stSidebar"] .stButton>button {
            background: linear-gradient(90deg,#246bce,#1f4fb4) !important;
            color: #fff !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 8px 12px !important;
        }
        /* Small helper text */
        [data-testid="stSidebar"] .small-muted {font-size:12px;color:#cbd5e1;margin-top:4px;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Header + helper block using simple HTML for better layout
    st.markdown(
        """
        <div style="padding:10px 6px;border-radius:8px;margin-bottom:8px;">
            <h3 style="margin:0 0 4px 0;color:#fff;">DB connection</h3>
           
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form(key="conn_form"):
        host = st.text_input("Host", value="localhost")
        port = st.text_input("Port", value="3306")
        user = st.text_input("User", value="root")
        password = st.text_input("Password", type="password")
        database = st.text_input("Database", value="lunadb")
        conn_btn = st.form_submit_button("Connect")

if "conn" not in st.session_state:
    st.session_state.conn = None

if conn_btn:
    conn = connect_db(host, port, user, password, database)
    if conn:
        st.session_state.conn = conn
        st.success("Connected to DB")

conn = st.session_state.get("conn")

if not conn:
    st.warning("Please connect to your MySQL database using the sidebar before using the UI.")
    st.stop()


### Load reference data for selection controls
missions = load_small_list(conn, "SELECT mission_id FROM Missions ORDER BY mission_id LIMIT 100")
researchers = load_small_list(conn, "SELECT researcher_id FROM Researchers ORDER BY researcher_id LIMIT 200")
objects = load_small_list(conn, "SELECT object_id FROM Celestial_objects ORDER BY object_id LIMIT 200")


tabs = st.tabs(["Functions", "Procedures", "Trigger-actions", "Raw SQL"])

with tabs[0]:
    st.header("Functions")
    st.subheader("GetMissionDurationYears")
    col1, col2 = st.columns(2)
    with col1:
        mission_choice = st.selectbox("Select mission (optional)", options=["-- none --"] + [str(m) for m in missions])
        launch_date = None
        if mission_choice != "-- none --":
            try:
                dfm = run_query(conn, "SELECT launch_date FROM Missions WHERE mission_id = %s", (int(mission_choice),))
                if not dfm.empty:
                    launch_date = dfm.iloc[0, 0]
            except Exception:
                launch_date = None
        if not launch_date:
            launch_date = st.date_input("Or pick a launch date", value=date(2000, 1, 1))
    with col2:
        if st.button("Compute mission age in years"):
            try:
                # MySQL function call
                df = run_query(conn, "SELECT GetMissionDurationYears(%s) AS years", (launch_date,))
                st.write(df)
            except Error as e:
                st.error(f"Database error: {e}")

    st.markdown("---")
    st.subheader("GetResearcherEmail")
    rcol1, rcol2 = st.columns([1, 2])
    with rcol1:
        rid = st.selectbox("Researcher ID", options=["-- none --"] + [str(r) for r in researchers])
    with rcol2:
        if st.button("Get email for researcher"):
            if rid == "-- none --":
                st.error("Select a researcher id first")
            else:
                try:
                    df = run_query(conn, "SELECT GetResearcherEmail(%s) AS email", (int(rid),))
                    st.write(df)
                except Error as e:
                    st.error(f"Database error: {e}")

    st.markdown("---")
    st.subheader("DiscoveryCountByResearcher")
    did = st.selectbox("Researcher for discovery count", options=["-- none --"] + [str(r) for r in researchers], key="disc_r")
    if st.button("Get discovery count"):
        if did == "-- none --":
            st.error("Select a researcher id first")
        else:
            try:
                df = run_query(conn, "SELECT DiscoveryCountByResearcher(%s) AS total_discoveries", (int(did),))
                st.write(df)
            except Error as e:
                st.error(f"Database error: {e}")

with tabs[1]:
    st.header("Stored Procedures")
    st.subheader("AddDiscovery")
    with st.form(key="add_discovery"):
        d_id = st.number_input("discovery_id", min_value=1, value=500)
        m_id = st.selectbox("mission_id", options=["-- none --"] + [str(m) for m in missions])
        o_id = st.selectbox("object_id", options=["-- none --"] + [str(o) for o in objects])
        r_id = st.selectbox("researcher_id", options=["-- none --"] + [str(r) for r in researchers])
        d_date = st.date_input("discovery_date", value=date.today())
        submit = st.form_submit_button("Call AddDiscovery")
        if submit:
            if "-- none --" in (m_id, o_id, r_id):
                st.error("Select mission, object and researcher IDs")
            else:
                try:
                    safe_call(conn, "CALL AddDiscovery(%s,%s,%s,%s,%s)", (int(d_id), int(m_id), int(o_id), int(r_id), d_date))
                    st.success("AddDiscovery executed. Check Discoveries table for new row.")
                    df = run_query(conn, "SELECT * FROM Discoveries WHERE discovery_id = %s", (int(d_id),))
                    st.dataframe(df)
                except Error as e:
                    st.error(f"Procedure error: {e}")

    st.markdown("---")
    st.subheader("GetObjectReport")
    with st.form(key="get_object_report"):
        obj = st.selectbox("object_id", options=["-- none --"] + [str(o) for o in objects])
        submit3 = st.form_submit_button("Call GetObjectReport")
        if submit3:
            if obj == "-- none --":
                st.error("Select an object id")
            else:
                try:
                    df = safe_call(conn, "CALL GetObjectReport(%s)", (int(obj),))
                    if df is not None and not df.empty:
                        st.dataframe(df)
                    else:
                        st.info("Procedure executed. No rows returned or result could not be parsed.")
                except Error as e:
                    st.error(f"Procedure error: {e}")

with tabs[2]:
    st.header("Trigger-causing actions")
    st.subheader("Insert a researcher (fires SplitFullName)")
    with st.form(key="insert_researcher"):
        irid = st.number_input("researcher_id", min_value=1, value=600)
        ifname = st.text_input("Full name (include title if desired)", value="Dr. Test User")
        iaff = st.text_input("Affiliation", value="TestOrg")
        idob = st.date_input("Date of birth", value=date(1990, 1, 1))
        sub_ir = st.form_submit_button("Insert researcher")
        if sub_ir:
            try:
                run_query(conn, "INSERT INTO Researchers (researcher_id, full_name, affiliation, date_of_birth) VALUES (%s,%s,%s,%s)", (int(irid), ifname, iaff, idob), fetch=False)
                st.success("Inserted researcher; SplitFullName trigger should have populated Full_name.")
                st.dataframe(run_query(conn, "SELECT * FROM Full_name WHERE researcher_id = %s", (int(irid),)))
            except Error as e:
                st.error(f"Insert error (trigger may have blocked it): {e}")

    st.markdown("---")
    st.subheader("Delete a mission (SHOULD be blocked by PreventMissionDelete if mission has existing discoveries)")
    with st.form(key="delete_mission"):
        del_mid = st.selectbox("Mission id to delete", options=["-- none --"] + [str(m) for m in missions])
        del_submit = st.form_submit_button("Delete mission")
        if del_submit:
            if del_mid == "-- none --":
                st.error("Select a mission id")
            else:
                try:
                    run_query(conn, "DELETE FROM Missions WHERE mission_id = %s", (int(del_mid),), fetch=False)
                    st.success("Mission deleted (or deletion executed).")
                except Error as e:
                    st.error(f"Delete blocked or error: {e}")

    st.markdown("---")

with tabs[3]:
    st.header("Raw SQL executor")
    st.markdown("Use this with care. Any query you run will be executed against the connected database.")
    sql = st.text_area("SQL", value="SELECT * FROM Missions LIMIT 10")
    if st.button("Run SQL"):
        try:
            if sql.strip().lower().startswith("select"):
                df = run_query(conn, sql)
                st.dataframe(df)
            else:
                run_query(conn, sql, fetch=False)
                st.success("Statement executed.")
        except Error as e:
            st.error(f"SQL error: {e}")

