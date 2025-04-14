from cassandra.cluster import Cluster
import pandas as pd

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('iut_ds')

# Execute SELECT query to fetch all users
rows = session.execute('SELECT * FROM users')

# Convert the result rows into a list of dictionaries
data = []
for row in rows:
    data.append({
        'user_id': row.user_id,
        'first_name': row.first_name,
        'last_name': row.last_name,
        'email': row.email
    })

# Create and display a Pandas DataFrame
df = pd.DataFrame(data)
print(df)

# Close the Cassandra connection
cluster.shutdown()