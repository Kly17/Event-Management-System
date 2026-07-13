from database import Database

db = Database()

db.import_json_data()

db.close()

print("\nMigration Completed Successfully!")