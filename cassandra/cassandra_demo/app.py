from flask import Flask, render_template, request, redirect, url_for
from cassandra.cluster import Cluster

# Initialize the Flask app
app = Flask(__name__)

# Connect to the Cassandra cluster
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('iut_ds')  # Connect to the keyspace named 'iut_ds'


# Route: Home page - registration form
@app.route('/')
def index():
    return render_template('index.html')


# Route: Handle form submission and register a new user
@app.route('/register', methods=['POST'])
def register():
    # Extract form data
    fname = request.form['first_name']
    lname = request.form['last_name']
    email = request.form['email']

    # Determine the next user_id by finding the current maximum
    rows = session.execute("SELECT MAX(user_id) AS max_id FROM users")
    max_id = rows.one().max_id or 0
    new_id = max_id + 1

    # Insert the new user into the users table
    session.execute("""
        INSERT INTO users (user_id, first_name, last_name, email)
        VALUES (%s, %s, %s, %s)
    """, (new_id, fname, lname, email))

    # Show success message
    return render_template('success.html', name=fname + ' ' + lname)


# Route: Display all registered users
@app.route('/users')
def list_users():
    # Query all users from Cassandra
    rows = session.execute('SELECT * FROM users')

    # Convert result into a list of dictionaries
    users = []
    for row in rows:
        users.append({
            'user_id': row.user_id,
            'first_name': row.first_name,
            'last_name': row.last_name,
            'email': row.email
        })

    # Render the list in an HTML table
    return render_template('users.html', users=users)


# Route: Delete a specific user by user_id
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    session.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    return redirect(url_for('list_users'))


# Route: Delete all users (truncate the table)
@app.route('/delete_all')
def delete_all_users():
    session.execute("TRUNCATE users")
    return redirect(url_for('list_users'))


# Route: Edit a specific user's information
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        # Get updated data from form
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']

        # Update the user record in the database
        session.execute("""
            UPDATE users SET first_name=%s, last_name=%s, email=%s WHERE user_id=%s
        """, (fname, lname, email, user_id))

        # Redirect back to the user list
        return redirect(url_for('list_users'))

    # If GET request: fetch the user data to prefill the form
    row = session.execute("SELECT * FROM users WHERE user_id = %s", (user_id,)).one()
    if row:
        return render_template('edit.html', user=row)
    return redirect(url_for('list_users'))


# Run the Flask app on localhost port 5050
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
