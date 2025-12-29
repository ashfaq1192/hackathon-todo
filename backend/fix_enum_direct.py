"""
Direct database fix for priority enum case mismatch.
Run this script directly with: python fix_enum_direct.py
"""

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable not set")
    exit(1)

print("=" * 70)
print("Running priority enum case fix migration...")
print("=" * 70)

try:
    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    cursor = conn.cursor()

    # Step 1: Convert to VARCHAR
    print("Step 1: Converting priority column to VARCHAR...")
    cursor.execute("ALTER TABLE tasks ALTER COLUMN priority TYPE VARCHAR(10);")
    conn.commit()
    print("✓ Converted to VARCHAR")

    # Step 2: Update values to lowercase
    print("Step 2: Converting all priority values to lowercase...")
    cursor.execute("""
        UPDATE tasks SET priority = LOWER(priority)
        WHERE priority IN ('LOW', 'MEDIUM', 'HIGH');
    """)
    rows_updated = cursor.rowcount
    conn.commit()
    print(f"✓ Updated {rows_updated} rows to lowercase")

    # Step 3: Drop old ENUM
    print("Step 3: Dropping old taskpriority ENUM type...")
    cursor.execute("DROP TYPE IF EXISTS taskpriority CASCADE;")
    conn.commit()
    print("✓ Dropped old ENUM type")

    # Step 4: Create new ENUM
    print("Step 4: Creating new taskpriority ENUM with lowercase values...")
    cursor.execute("CREATE TYPE taskpriority AS ENUM ('low', 'medium', 'high');")
    conn.commit()
    print("✓ Created new ENUM type")

    # Step 5: Drop default
    print("Step 5: Dropping default constraint...")
    cursor.execute("ALTER TABLE tasks ALTER COLUMN priority DROP DEFAULT;")
    conn.commit()
    print("✓ Dropped default constraint")

    # Step 6: Convert back to ENUM
    print("Step 6: Converting priority column back to ENUM...")
    cursor.execute("""
        ALTER TABLE tasks ALTER COLUMN priority TYPE taskpriority
        USING priority::taskpriority;
    """)
    conn.commit()
    print("✓ Converted back to ENUM")

    # Step 7: Restore default
    print("Step 7: Restoring default value...")
    cursor.execute("ALTER TABLE tasks ALTER COLUMN priority SET DEFAULT 'medium'::taskpriority;")
    conn.commit()
    print("✓ Restored default value")

    # Verify
    print("\nVerifying ENUM values...")
    cursor.execute("""
        SELECT e.enumlabel
        FROM pg_type t
        JOIN pg_enum e ON t.oid = e.enumtypid
        WHERE t.typname = 'taskpriority'
        ORDER BY e.enumsortorder;
    """)
    enum_values = [row[0] for row in cursor.fetchall()]
    print(f"✓ ENUM values are now: {enum_values}")

    cursor.close()
    conn.close()

    print("=" * 70)
    print("✅ Migration completed successfully!")
    print("=" * 70)

except Exception as e:
    print(f"\n❌ Migration failed: {e}")
    if conn:
        conn.rollback()
        conn.close()
    exit(1)
