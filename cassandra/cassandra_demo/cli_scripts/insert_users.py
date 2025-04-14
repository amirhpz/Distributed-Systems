from cassandra.cluster import Cluster

# Connect to Cassandra (localhost)
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('iut_ds')  # our keyspace

# Insert data
session.execute("""
    INSERT INTO users (user_id, first_name, last_name, email)
    VALUES (%s, %s, %s, %s)
""", (3, 'Reza', 'Karimi', 'reza@example.com'))

# Select and print all users
rows = session.execute('SELECT * FROM users')
for row in rows:
    print(f"{row.user_id}: {row.first_name} {row.last_name} - {row.email}")

# Close the connection
cluster.shutdown()
