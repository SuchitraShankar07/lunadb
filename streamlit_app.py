import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import date
import pandas as pd


st.set_page_config(page_title="LunaDB - Functional UI", layout="wide")

# Inject full-page background GIF
st.markdown(
    """
    <style>
    /* Import cosmic fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Space+Grotesk:wght@300;400;600&display=swap');

    :root {
        --font-primary: 'Space Grotesk', sans-serif;
        --font-heading: 'Orbitron', sans-serif;
    }

    /* Base App container and background */
    [data-testid="stAppViewContainer"] {
        background-image: url('https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcG9kZ2NnbGVkNGRuYnBzemtrd2sydzExcWF4MmYyb3F3enVqa3RqbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/FlodpfQUBSp20/giphy.gif');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 20, 0.75);
        z-index: -1;
    }

    /* Font styling — cosmic aesthetic */
    body, .stApp, .stMarkdown, label, input, textarea, select, div, button {
        font-family: var(--font-primary) !important;
        letter-spacing: 0.3px;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: var(--font-heading) !important;
        color: #e0e8ff !important;
        text-shadow: 0 0 10px rgba(100, 180, 255, 0.5);
    }

    /* Headings with neon glow */
    h1 {
        font-size: 2.6rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        background: linear-gradient(90deg, #8ab4f8, #a855f7, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(100, 180, 255, 0.4);
    }

    h2, h3 {
        text-shadow: 0 0 12px rgba(100, 180, 255, 0.3);
    }

    /* Button styling */
    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6, #9333ea) !important;
        border-radius: 8px !important;
        border: none !important;
        color: #f0f8ff !important;
        font-weight: 600;
        text-transform: uppercase;
        box-shadow: 0 0 12px rgba(59, 130, 246, 0.6);
        transition: all 0.3s ease-in-out;
        font-family: var(--font-heading) !important;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background: linear-gradient(90deg, #3b82f6, #6366f1, #ec4899) !important;
        box-shadow: 0 0 20px rgba(147, 51, 234, 0.7);
        transform: scale(1.03);
    }

    /* DataFrames and tables */
    [data-testid="stDataFrame"] table {
        font-family: var(--font-primary) !important;
        color: #e0e0ff !important;
        background-color: rgba(10, 10, 30, 0.8) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    [data-testid="stDataFrame"] th {
        background-color: rgba(60, 60, 100, 0.8) !important;
        text-transform: uppercase;
        font-weight: 600;
    }

    /* Tabs with glowing edge */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(20, 20, 40, 0.6);
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: var(--font-heading) !important;
        color: #b0b0ff !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(100, 100, 255, 0.25) !important;
        border-bottom: 2px solid #a855f7 !important;
        color: #ffffff !important;
    }

    /* Inputs */
    input, textarea, [data-baseweb="select"] {
        background-color: rgba(25, 25, 50, 0.85) !important;
        color: #ffffff !important;
        border: 1px solid rgba(147, 51, 234, 0.3) !important;
        border-radius: 6px !important;
        font-family: var(--font-primary) !important;
    }
    input:focus, textarea:focus {
        outline: none !important;
        box-shadow: 0 0 10px rgba(147, 51, 234, 0.6);
    }

    /* Sidebar cosmic look */
    [data-testid="stSidebar"] {
        background: radial-gradient(circle at top left, rgba(20,20,40,0.95), rgba(10,10,20,0.85)) !important;
        border-right: 1px solid rgba(100,100,255,0.15);
    }
    [data-testid="stSidebar"] * {
        color: #e0e8ff !important;
        font-family: var(--font-heading) !important;
    }

    /* Links and hover effects */
    a {
        color: #a855f7 !important;
        text-decoration: none;
    }
    a:hover {
        color: #f472b6 !important;
    }

    /* Info / Success / Warning boxes */
    .stSuccess, .stError, .stWarning, .stInfo {
        font-family: var(--font-primary) !important;
        border-radius: 10px !important;
        background: rgba(15, 15, 40, 0.8) !important;
        color: #e8e8ff !important;
        box-shadow: 0 0 12px rgba(100, 180, 255, 0.2);
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

# Auto-connect using fixed credentials and provide simple sidebar navigation
DEFAULT_DB = {"host": "localhost", "port": "3306", "user": "root", "password": "tejas123", "database": "lunadb"}

if "conn" not in st.session_state:
    st.session_state.conn = None
    st.session_state.conn_error = None

if st.session_state.conn is None:
    _conn = connect_db(
        DEFAULT_DB["host"], DEFAULT_DB["port"], DEFAULT_DB["user"], DEFAULT_DB["password"], DEFAULT_DB["database"]
    )
    if _conn:
        st.session_state.conn = _conn
    else:
        st.error("Automatic database connection failed. Check MySQL is running and credentials are valid.")
        st.stop()

conn = st.session_state.conn

with st.sidebar:
    st.title("LunaDB")
    st.caption("Connected as root (auto-login)")
    page = st.radio("Navigate", ["Home", "Missions", "Researchers", "Objects", "Discoveries", "Advanced"], index=0)


### Load reference data for selection controls
missions = load_small_list(conn, "SELECT mission_id FROM Missions ORDER BY mission_id LIMIT 200")
researchers = load_small_list(conn, "SELECT researcher_id FROM Researchers ORDER BY researcher_id LIMIT 500")
objects = load_small_list(conn, "SELECT object_id FROM Celestial_objects ORDER BY object_id LIMIT 500")


# Helper to show dataframes nicely
def show_df(df):
    if df is None or df.empty:
        st.info("No rows to display.")
    else:
        try:
            st.dataframe(df, use_container_width=True, hide_index=True)
        except TypeError:
            try:
                st.dataframe(df.style.hide(axis="index"), use_container_width=True)
            except Exception:
                st.dataframe(df, use_container_width=True)


# Pages
if page == "Home":
    st.header("Welcome to LunaDB")
    st.write("Use the sidebar to navigate through the main features of this app.")
    st.markdown(
        """
        - Missions: Browse missions, view details and discovery counts, compute durations, and manage deletions.
        - Researchers: Browse researchers, view details and email, and add new researchers.
        - Objects: Browse celestial objects, get object reports, and view observations.
        - Discoveries: List discoveries with rich joins and add new discovery records.
        - Advanced: Run raw SQL queries (use with care).
        """
    )

elif page == "Missions":
    st.header("Missions")
    # Browse actions stacked vertically
    list_btn = st.button("List first 100 missions", use_container_width=True)
    list_container = st.container()
    if list_btn:
        try:
            df = run_query(conn, "SELECT mission_id, Name AS mission_name, launch_date, agency FROM Missions ORDER BY mission_id LIMIT 100")
            with list_container:
                show_df(df)
        except Error as e:
            st.error(f"Error: {e}")

    mid = st.selectbox("Select mission id", options=["-- none --"] + [str(m) for m in missions])
    details_container = st.container()

    if mid != "-- none --":
        try:
            df = run_query(
                conn,
                """
                SELECT m.mission_id, m.Name AS mission_name, m.launch_date, m.agency,
                       COUNT(d.discovery_id) AS discovery_count
                FROM Missions m
                LEFT JOIN Discoveries d ON m.mission_id = d.mission_id
                WHERE m.mission_id = %s
                GROUP BY m.mission_id
                """,
                (int(mid),),
            )
            with details_container:
                show_df(df)
        except Error as e:
            st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("Utilities")
    # Only keep the specific-date utility and ensure the output appears directly below
    with st.expander("Compute years from a specific date", expanded=False):
        with st.form("mission_years_from_date"):
            ld = st.date_input("Launch date", value=date(2000, 1, 1))
            sub = st.form_submit_button("Compute years", use_container_width=True)
        util_result_container = st.container()
        if sub:
            try:
                df = run_query(conn, "SELECT GetMissionDurationYears(%s) AS years", (ld,))
                with util_result_container:
                    show_df(df)
            except Error as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("Delete mission")
    with st.form("delete_mission_form"):
        del_mid = st.selectbox("Mission id", options=["-- none --"] + [str(m) for m in missions], key="del_m")
        confirm = st.checkbox("I understand this may be blocked")
        submit = st.form_submit_button("Delete mission", use_container_width=True)
        if submit:
            if del_mid == "-- none --":
                st.error("Pick a mission id")
            elif not confirm:
                st.error("Please confirm intent")
            else:
                try:
                    run_query(conn, "DELETE FROM Missions WHERE mission_id = %s", (int(del_mid),), fetch=False)
                    st.success("Delete attempted. Check DB.")
                except Error as e:
                    st.error(f"Delete error: {e}")

elif page == "Researchers":
    st.header("Researchers")
    list_r_container = st.container()
    if st.button("List first 200 researchers", use_container_width=True):
        try:
            df = run_query(conn, "SELECT * FROM Researchers ORDER BY researcher_id LIMIT 200")
            with list_r_container:
                show_df(df)
        except Error as e:
            st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("Details")
    rid = st.selectbox("Researcher id", options=["-- none --"] + [str(r) for r in researchers])
    if rid != "-- none --":
        try:
            df = run_query(
                conn,
                """
                SELECT r.*, CONCAT(e.email_name, '@', e.email_domain) AS email
                FROM Researchers r
                LEFT JOIN Email e ON r.researcher_id = e.researcher_id
                WHERE r.researcher_id = %s
                """,
                (int(rid),),
            )
            show_df(df)
        except Error as e:
            st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("Lookup email")
    email_container = st.container()
    with st.form("get_email_form"):
        rid_email = st.selectbox("Researcher", options=["-- none --"] + [str(r) for r in researchers], key="rid_email")
        sub = st.form_submit_button("Get email", use_container_width=True)
        if sub:
            if rid_email == "-- none --":
                st.error("Select id")
            else:
                try:
                    df = run_query(conn, "SELECT GetResearcherEmail(%s) AS email", (int(rid_email),))
                    with email_container:
                        show_df(df)
                except Error as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("Add researcher")
    insert_r_container = st.container()
    with st.form("insert_researcher_form"):
        irid = st.number_input("researcher_id", min_value=1, value=600)
        ifname = st.text_input("Full name", value="Dr. Test User")
        iaff = st.text_input("Affiliation", value="TestOrg")
        idob = st.date_input("Date of birth", value=date(1990, 1, 1))
        submit = st.form_submit_button("Insert", use_container_width=True)
        if submit:
            try:
                run_query(
                    conn,
                    "INSERT INTO Researchers (researcher_id, full_name, affiliation, date_of_birth) VALUES (%s,%s,%s,%s)",
                    (int(irid), ifname, iaff, idob),
                    fetch=False,
                )
                st.success("Inserted researcher.")
                with insert_r_container:
                    show_df(run_query(conn, "SELECT * FROM Full_name WHERE researcher_id = %s", (int(irid),)))
            except Error as e:
                st.error(f"Insert error: {e}")

elif page == "Objects":
    st.header("Celestial Objects & Observations")
    list_o_container = st.container()
    if st.button("List first 200 objects", use_container_width=True):
        try:
            df = run_query(conn, "SELECT * FROM Celestial_objects ORDER BY object_id LIMIT 200")
            with list_o_container:
                show_df(df)
        except Error as e:
            st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("Object report")
    obj_report_container = st.container()
    with st.form("object_report_form"):
        obj = st.selectbox("object_id", options=["-- none --"] + [str(o) for o in objects])
        submit = st.form_submit_button("Get report", use_container_width=True)
        if submit:
            if obj == "-- none --":
                st.error("Select an object")
            else:
                try:
                    df = safe_call(conn, "CALL GetObjectReport(%s)", (int(obj),))
                    if df is not None and not df.empty:
                        with obj_report_container:
                            show_df(df)
                    else:
                        st.info("No rows returned or not parseable.")
                except Error as e:
                    st.error(f"Procedure error: {e}")

    st.markdown("---")
    st.subheader("Observations for object")
    oid = st.selectbox("Choose object", options=["-- none --"] + [str(o) for o in objects], key="obs_obj")
    obs_container = st.container()
    if st.button("Show observations", use_container_width=True):
        if oid == "-- none --":
            st.error("Select an object")
        else:
            try:
                df = run_query(
                    conn,
                    """
                    SELECT od.observation_id, od.object_id, co.name AS object_name, od.parameter, od.value
                    FROM Observation_data od
                    LEFT JOIN Celestial_objects co ON od.object_id = co.object_id
                    WHERE od.object_id = %s
                    ORDER BY od.observation_id DESC
                    LIMIT 200
                    """,
                    (int(oid),),
                )
                with obs_container:
                    show_df(df)
            except Error as e:
                st.error(f"Error: {e}")

elif page == "Discoveries":
    st.header("Discoveries")
    list_d_container = st.container()
    if st.button("List recent discoveries", use_container_width=True):
        try:
            df = run_query(
                conn,
                """
                SELECT d.discovery_id, d.discovery_date, d.mission_id, m.Name AS mission_name,
                       d.object_id, co.name AS object_name, d.researcher_id, r.full_name
                FROM Discoveries d
                LEFT JOIN Missions m ON d.mission_id = m.mission_id
                LEFT JOIN Celestial_objects co ON d.object_id = co.object_id
                LEFT JOIN Researchers r ON d.researcher_id = r.researcher_id
                ORDER BY d.discovery_date DESC
                LIMIT 200
                """,
            )
            with list_d_container:
                show_df(df)
        except Error as e:
            st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("Add discovery")
    add_disc_container = st.container()
    with st.form("add_discovery_form"):
        d_id = st.number_input("discovery_id", min_value=1, value=500)
        m_id = st.selectbox("mission_id", options=["-- none --"] + [str(m) for m in missions])
        o_id = st.selectbox("object_id", options=["-- none --"] + [str(o) for o in objects])
        r_id = st.selectbox("researcher_id", options=["-- none --"] + [str(r) for r in researchers])
        d_date = st.date_input("discovery_date", value=date.today())
        submit = st.form_submit_button("Insert", use_container_width=True)
        if submit:
            if "-- none --" in (m_id, o_id, r_id):
                st.error("Select mission, object and researcher IDs")
            else:
                try:
                    safe_call(conn, "CALL AddDiscovery(%s,%s,%s,%s,%s)", (int(d_id), int(m_id), int(o_id), int(r_id), d_date))
                    st.success("Discovery added (procedure executed).")
                    with add_disc_container:
                        show_df(run_query(conn, "SELECT * FROM Discoveries WHERE discovery_id = %s", (int(d_id),)))
                except Error as e:
                    st.error(f"Procedure error: {e}")

    st.markdown("---")
    st.subheader("Discovery count by researcher")
    disc_count_container = st.container()
    with st.form("disc_count_form"):
        did = st.selectbox("Researcher", options=["-- none --"] + [str(r) for r in researchers], key="disc_by_r")
        sub = st.form_submit_button("Get count", use_container_width=True)
        if sub:
            if did == "-- none --":
                st.error("Select id")
            else:
                try:
                    df = run_query(conn, "SELECT DiscoveryCountByResearcher(%s) AS total_discoveries", (int(did),))
                    with disc_count_container:
                        show_df(df)
                except Error as e:
                    st.error(f"Error: {e}")
elif page == "Advanced":
    st.header("Advanced")

    st.markdown("---")
    st.subheader("Aggregate Function Utilities")

    with st.expander("Total number of missions"):
        try:
            df = run_query(conn, "SELECT COUNT(*) AS total_missions FROM Missions")
            show_df(df)
        except Error as e:
            st.error(f"Error: {e}")

    with st.expander("Total number of researchers"):
        try:
            df = run_query(conn, "SELECT COUNT(*) AS total_researchers FROM Researchers")
            show_df(df)
        except Error as e:
            st.error(f"Error: {e}")

    with st.expander("Average mass of celestial objects"):
        try:
            df = run_query(conn, "SELECT AVG(mass) AS average_mass FROM Celestial_objects")
            show_df(df)
        except Error as e:
            st.error(f"Error: {e}")


    with st.expander("Maximum distance among celestial objects"):
        try:
            df = run_query(conn, "SELECT MAX(distance) AS farthest_distance FROM Celestial_objects")
            show_df(df)
        except Error as e:
            st.error(f"Error: {e}")

    with st.expander("Discoveries count per mission"):
        try:
            df = run_query(
                conn,
                """
                SELECT m.mission_id, m.Name AS mission_name,
                       COUNT(d.discovery_id) AS total_discoveries
                FROM Missions m
                LEFT JOIN Discoveries d ON m.mission_id = d.mission_id
                GROUP BY m.mission_id, m.Name
                ORDER BY total_discoveries DESC
                """
            )
            show_df(df)
        except Error as e:
            st.error(f"Error: {e}")

    st.markdown("---")
    with st.expander("Raw SQL executor", expanded=True):
        st.markdown("Use with care. Queries will run against the connected DB.")
        with st.form("raw_sql_form"):
            sql = st.text_area("SQL", value="SELECT * FROM Missions LIMIT 10", height=180)
            run = st.form_submit_button("Run", use_container_width=True)
            if run:
                try:
                    if sql.strip().lower().startswith("select"):
                        df = run_query(conn, sql)
                        show_df(df)
                    else:
                        run_query(conn, sql, fetch=False)
                        st.success("Statement executed.")
                except Error as e:
                    st.error(f"SQL error: {e}")

