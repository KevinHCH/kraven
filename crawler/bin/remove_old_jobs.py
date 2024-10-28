
import sqlite3
import datetime

def adapt_datetime(dt):
    return dt.isoformat()
sqlite3.register_adapter(datetime.datetime, adapt_datetime)

DATABASE_PATH = '/data/jobs.db'

def remove_old_jobs():

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    

    two_weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=2)
    
    cursor.execute("""
        DELETE FROM jobs
        WHERE created_at < ?
    """, (two_weeks_ago,))
    rows_deleted = cursor.rowcount

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Old job posts removed successfully. Number of records deleted: {rows_deleted}")


if __name__ == '__main__':
    remove_old_jobs()
