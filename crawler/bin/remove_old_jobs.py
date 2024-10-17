
import sqlite3
import datetime


DATABASE_PATH = '/data/jobs.db'

def remove_old_jobs():

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    

    two_weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=2)
    
    cursor.execute("""
        DELETE FROM jobs
        WHERE created_at < ?
    """, (two_weeks_ago,))

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    print("Old job posts removed successfully.")

if __name__ == '__main__':
    remove_old_jobs()
