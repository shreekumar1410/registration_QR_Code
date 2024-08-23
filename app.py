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
    return render_template('index.html')  # Home page with buttons

# Registration page route
@app.route('/register')
def register():
    return render_template('register.html')  # Registration form HTML file

# Registration form submission route
@app.route('/submit', methods=['POST'])
def submit():
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
    user_id = cursor.lastrowid  # Get the ID of the last inserted row
    conn.commit()
    cursor.close()
    conn.close()

    # Generate QR code for the user ID
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(user_id)
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
    if request.method == 'POST':
        user_id = request.form['user_id']

        # Retrieve user data from the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_data:
            return render_template('user_info.html', user_data=user_data)
        else:
            return 'User not found', 404

    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
