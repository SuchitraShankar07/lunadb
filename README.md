# LunaDB

LunaDB is a small educational relational database project created as coursework for a Database Management Systems class. It models space missions, celestial objects, researchers and observations and includes a set of stored functions, procedures and triggers that demonstrate common DB concepts (functions, triggers, SIGNAL/exception handling and stored procedures).

This repository contains SQL schema and sample data along with a small optional Streamlit-based UI that can be used to exercise the stored routines.

Contents
--------
- `create.sql` — DDL for tables used in the project (Missions, Celestial_objects, Researchers, Observation_data, Email, Full_name, Discoveries, ...).
- `insert.sql` — Sample data inserts to populate the database for testing and demo.
- `operations.sql` — Definitions for functions, triggers and stored procedures used in the exercises:
	- Functions: `GetMissionDurationYears`, `GetResearcherEmail`, `DiscoveryCountByResearcher`.
	- Triggers: `SplitFullName`, `PreventMissionDelete`, `LogObservationUpdate` (note: logging behavior may be adjusted depending on your schema).
	- Procedures: `AddDiscovery`, `RegisterResearcher`, `GetObjectReport`.
- `streamlit_app.py` — Single-file Streamlit UI (optional) that connects to a running MySQL instance and calls the above routines.
- `tests/op_tests.sql` — A set of example queries and operations that exercise the functions/procedures/triggers.

Quick start — create the database and load sample data
-----------------------------------------------------
1. Create the database and tables, and populate sample data. From the repository root:

```bash
mysql -u <user> -p < create.sql
mysql -u <user> -p lunadb < insert.sql
```

2. Install the stored routines (functions/procedures/triggers):

```bash
mysql -u <user> -p lunadb < operations.sql
```

If you prefer, run the three files inside a MySQL client session (use `SOURCE create.sql; SOURCE insert.sql; SOURCE operations.sql;`).

Notes about schema mismatches
-----------------------------
- The `Email` table in `create.sql` is defined with columns `email_name` and `email_domain`. Earlier versions of the stored procedures referenced `username`/`domain`. The repository `operations.sql` has been updated to use `email_name`/`email_domain` to match the DDL. If you modified the DDL you may need to adjust `operations.sql` accordingly.
- The trigger `LogObservationUpdate` used to insert into an `Observation_Log` table that is not present in `create.sql`; if you want persistent logs, create that table or revert the trigger to insert into it.

Running the optional Streamlit UI
--------------------------------
The `streamlit_app.py` file is an optional convenience UI to call functions and procedures and to perform actions that will fire triggers. It is not required for the project and all functionality is available via SQL.

Dependencies (if you want to run the UI):

```bash
python3 -m pip install streamlit mysql-connector-python pandas
```

Start the UI from the repository root:

```bash
streamlit run streamlit_app.py
```

When the UI opens, supply your MySQL connection details in the sidebar (host, port, user, password, database). The UI expects the `lunadb` database to exist and the SQL from the files above to be applied.

Testing
-------
- You can run the `tests/op_tests.sql` file against the `lunadb` database to exercise typical operations and view expected results. For example:

```bash
mysql -u <user> -p lunadb < tests/op_tests.sql
```

Development notes
-----------------
- This project is educational/demonstration-focused. The stored routines demonstrate error handling (SIGNAL), duplicate-checking, and use of triggers to maintain derived data (e.g., `Full_name`).
- Keep the DDL and the routines in sync: if you change column names in the tables, update `operations.sql` to match.

Contact / Credits
-----------------
This repo was prepared as part of a DBMS course assignment. If you need help running the project or want enhancements (additional tests, a Docker compose file, or a packaged demo), open an issue or ask for help.
