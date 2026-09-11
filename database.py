
import sqlite3


DATABASE = "history.db"


def get_connection():

    conn = sqlite3.connect(
        DATABASE
    )

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    # Chat history table
    cursor.execute("""

    CREATE TABLE IF NOT EXISTS chat_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        message TEXT,

        response TEXT,

        created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP

    )

    """)


    # Code analysis history table
    cursor.execute("""

    CREATE TABLE IF NOT EXISTS analysis_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        code TEXT,

        language TEXT,

        issues TEXT,

        fixed_code TEXT,

        explanation TEXT,

        created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP

    )

    """)


    conn.commit()

    conn.close()


# =======================
# SAVE CHAT
# =======================

def save_chat(
    message,
    response
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """

        INSERT INTO chat_history(

        message,
        response

        )

        VALUES (?,?)

        """,

        (
            message,
            response
        )
    )

    conn.commit()

    conn.close()


# =======================
# SAVE ANALYSIS
# =======================

def save_analysis(

    code,
    language,
    issues,
    fixed_code,
    explanation

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """

        INSERT INTO analysis_history(

        code,
        language,
        issues,
        fixed_code,
        explanation

        )

        VALUES (?,?,?,?,?)

        """,

        (

            code,

            language,

            issues,

            fixed_code,

            explanation
        )
    )

    conn.commit()

    conn.close()


# =======================
# GET CHAT HISTORY
# =======================

def get_chat_history():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM chat_history

    ORDER BY id DESC

    LIMIT 20

    """)

    data = cursor.fetchall()

    conn.close()

    return data