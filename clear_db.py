import os
import shutil
import sqlite3

def clear_database():
    print("--- Cleaning Database ---")
    db_path = "database.db"
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Disable foreign keys temporarily to avoid deletion order issues
            cursor.execute("PRAGMA foreign_keys = OFF;")
            
            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                print(f"Clearing table: {table_name}")
                cursor.execute(f"DELETE FROM {table_name};")
            
            conn.commit()
            conn.close()
            print("Database cleared successfully.")
        except Exception as e:
            print(f"Error clearing database: {e}")
    else:
        print("Database file not found.")

def clear_projects():
    print("\n--- Cleaning Projects Folder ---")
    projects_dir = "projects"
    if os.path.exists(projects_dir):
        try:
            for item in os.listdir(projects_dir):
                item_path = os.path.join(projects_dir, item)
                if os.path.isdir(item_path):
                    print(f"Deleting project folder: {item}")
                    shutil.rmtree(item_path)
                elif item.endswith(".zip"):
                    print(f"Deleting zip file: {item}")
                    os.remove(item_path)
            print("Projects folder cleaned.")
        except Exception as e:
            print(f"Error cleaning projects folder: {e}")
    else:
        print("Projects directory not found.")

if __name__ == "__main__":
    confirm = input("This will delete ALL users, projects, and chat history. Are you sure? (y/n): ")
    if confirm.lower() == 'y':
        clear_database()
        clear_projects()
        print("\nReset complete.")
    else:
        print("Reset cancelled.")
