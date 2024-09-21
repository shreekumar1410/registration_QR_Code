from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import qrcode

app = Flask(__name__)

# MySQL Database connection details
db_config = {
    'user': 'root',
    'password': '#Shree1410',
    'host': 'localhost',
    'database': 'user_registration'
}

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Registration page route
@app.route('/register')
def register():
    return render_template('register.html')

# Registration form submission route
@app.route('/submit', methods=['POST'])
def submit():
    # Extract form data
    username = request.form['username']
    phone = request.form['phone']
    email = request.form['email']
    occupation = request.form['occupation']
    state = request.form['state']
    city = request.form['city']

    # Connect to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insert user data into the database
    cursor.execute('''
        INSERT INTO users (username, phone, email, occupation, state, city)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (username, phone, email, occupation, state, city))
    user_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()

    # Generate QR code with the URL for the print page
    print_url = url_for('print_qr', user_id=user_id, _external=True)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(print_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_filename = f'static/QR_code/qr_{user_id}.png'
    img.save(img_filename)

    # Redirect to a page showing the QR code and user ID
    return redirect(url_for('success', user_id=user_id))

# Success page route
@app.route('/success/<int:user_id>')
def success(user_id):
    return render_template('success.html', user_id=user_id)

# Search page route
@app.route('/search', methods=['GET', 'POST'])
def search():
    user_data = None  # Initialize user_data as None
    
    if request.method == 'POST':  # Only perform search on POST request
        user_id = request.form['user_id']
        if user_id:  # Ensure user_id is not empty
            # Retrieve user data from the MySQL database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()
    
    return render_template('search.html', user_data=user_data)


# Edit page route
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    if request.method == 'POST':
        # Update the user data in the database
        username = request.form['username']
        phone = request.form['phone']
        email = request.form['email']
        occupation = request.form['occupation']
        state = request.form['state']
        city = request.form['city']

        cursor.execute('''
            UPDATE users SET username=%s, phone=%s, email=%s, occupation=%s, state=%s, city=%s WHERE id=%s
        ''', (username, phone, email, occupation, state, city, user_id))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('search'))

    # Retrieve the existing user data
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('edit.html', user_data=user_data)

# Print QR code page route
@app.route('/print_qr/<int:user_id>')
def print_qr(user_id):
    return render_template('print_qr.html', user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)
