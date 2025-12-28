from app import app, db
from sqlalchemy import text

def create_notification_table():
    """Create notification table if not exists"""
    
    sql_query = """
    CREATE TABLE IF NOT EXISTS notification (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title VARCHAR(255) NOT NULL,
        message TEXT NOT NULL,
        type VARCHAR(50) DEFAULT 'info',
        is_read BOOLEAN DEFAULT FALSE,
        link VARCHAR(500),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_notification_user
            FOREIGN KEY(user_id) 
            REFERENCES public."user"(id)
            ON DELETE CASCADE
    );
    
    -- Create indexes for better performance
    CREATE INDEX IF NOT EXISTS idx_notification_user_id ON notification(user_id);
    CREATE INDEX IF NOT EXISTS idx_notification_is_read ON notification(is_read);
    CREATE INDEX IF NOT EXISTS idx_notification_created_at ON notification(created_at DESC);
    """
    
    try:
        with app.app_context():
            # Execute the SQL
            db.session.execute(text(sql_query))
            db.session.commit()
            print("✅ Tabel notification berhasil dibuat!")
            print("✅ Indexes berhasil dibuat!")
            
            # Verify table creation
            result = db.session.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_schema = 'public' 
                AND table_name = 'notification'
                ORDER BY ordinal_position
            """))
            
            print("\n📊 Struktur Tabel Notification:")
            print("-" * 50)
            for row in result:
                nullable = "NULL" if row[2] == 'YES' else "NOT NULL"
                print(f"  {row[0]:<20} {row[1]:<20} {nullable}")
            
            # Check foreign key
            fk_result = db.session.execute(text("""
                SELECT
                    tc.constraint_name,
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
                AND tc.table_name = 'notification'
            """))
            
            print("\n🔗 Foreign Keys:")
            print("-" * 50)
            for row in fk_result:
                print(f"  {row[0]}: {row[1]} -> {row[2]}.{row[3]}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        db.session.rollback()

if __name__ == '__main__':
    create_notification_table()