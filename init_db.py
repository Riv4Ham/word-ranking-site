import sqlite3

# Load your dictionary.txt
with open("data/dictionary.txt", "r") as f:
    words = [line.strip() for line in f if line.strip()]

# Connect to SQLite and create the table
conn = sqlite3.connect("words.db")
c = conn.cursor()

# Create the table if it doesn't exist
c.execute("""
    CREATE TABLE IF NOT EXISTS words (
        word TEXT PRIMARY KEY,
        score INTEGER DEFAULT 0
    )
""")

# Insert words into the table, skip duplicates
for word in words:
    c.execute("INSERT OR IGNORE INTO words (word, score) VALUES (?, 0)", (word,))

conn.commit()
conn.close()

print("✅ Database initialized with", len(words), "words.")
