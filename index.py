from flask import Flask, render_template_string, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages

# Enhanced HTML template with forms
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Travel Agency Management System</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 1400px; 
            margin: 0 auto; 
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin: -30px -30px 40px -30px;
        }
        .stats { 
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px; 
            margin-bottom: 40px;
        }
        .stat-card { 
            background: white; 
            padding: 25px; 
            border-radius: 10px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            border-left: 5px solid #667eea;
            transition: transform 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .section {
            margin-bottom: 50px;
        }
        .section-title {
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 24px;
        }
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }
        .card { 
            background: #f8f9fa; 
            padding: 25px; 
            border-radius: 10px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        .form-container {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 4px solid #28a745;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        .form-group textarea {
            height: 100px;
            resize: vertical;
        }
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        .btn {
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s ease;
        }
        .btn:hover {
            background: #5a6fd8;
        }
        .btn-success {
            background: #28a745;
        }
        .btn-success:hover {
            background: #218838;
        }
        .nav-tabs {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 2px solid #667eea;
        }
        .nav-tab {
            padding: 12px 25px;
            background: #f8f9fa;
            border: none;
            cursor: pointer;
            margin-right: 5px;
            border-radius: 5px 5px 0 0;
            transition: background 0.3s ease;
        }
        .nav-tab.active {
            background: #667eea;
            color: white;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .alert {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .rating {
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            margin-left: 5px;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }
        .feature {
            background: white;
            padding: 8px;
            border-radius: 8px;
            text-align: center;
            font-size: 12px;
            border: 1px solid #e0e0e0;
        }
        .bookings-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .bookings-table th,
        .bookings-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .bookings-table th {
            background: #667eea;
            color: white;
        }
        .status-confirmed {
            background: #d4edda;
            color: #155724;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
        }
        .no-data {
            text-align: center;
            color: #666;
            font-style: italic;
            padding: 40px;
        }
    </style>
    <script>
        function showTab(tabName) {
            // Hide all tab contents
            var tabContents = document.getElementsByClassName('tab-content');
            for (var i = 0; i < tabContents.length; i++) {
                tabContents[i].classList.remove('active');
            }
            
            // Remove active class from all tabs
            var tabs = document.getElementsByClassName('nav-tab');
            for (var i = 0; i < tabs.length; i++) {
                tabs[i].classList.remove('active');
            }
            
            // Show selected tab and set active
            document.getElementById(tabName).classList.add('active');
            event.currentTarget.classList.add('active');
        }
        
        // Show dashboard by default
        document.addEventListener('DOMContentLoaded', function() {
            showTab('dashboard');
        });
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Luxury Travel Agency Management System</h1>
            <p>Complete Business Dashboard & Analytics</p>
        </div>

        <!-- Navigation Tabs -->
        <div class="nav-tabs">
            <button class="nav-tab active" onclick="showTab('dashboard')">Dashboard</button>
            <button class="nav-tab" onclick="showTab('addCustomer')">Add Customer</button>
            <button class="nav-tab" onclick="showTab('addDestination')">Add Destination</button>
            <button class="nav-tab" onclick="showTab('addPartner')">Add Partner</button>
            <button class="nav-tab" onclick="showTab('createBooking')">Create Booking</button>
        </div>

        <!-- Flash Messages -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <!-- Dashboard Tab -->
        <div id="dashboard" class="tab-content active">
            <!-- Statistics Section -->
            <div class="stats">
                <div class="stat-card">
                    <h3>Total Customers</h3>
                    <p>{{ stats.total_customers }}</p>
                </div>
                <div class="stat-card">
                    <h3>Total Destinations</h3>
                    <p>{{ stats.total_destinations }}</p>
                </div>
                <div class="stat-card">
                    <h3>Total Partners</h3>
                    <p>{{ stats.total_partners }}</p>
                </div>
                <div class="stat-card">
                    <h3>Total Bookings</h3>
                    <p>{{ stats.total_bookings }}</p>
                </div>
                <div class="stat-card">
                    <h3>Total Revenue</h3>
                    <p>${{ "%.2f"|format(stats.total_revenue) }}</p>
                </div>
                <div class="stat-card">
                    <h3>Avg Booking Value</h3>
                    <p>${{ "%.2f"|format(stats.avg_booking_value) }}</p>
                </div>
            </div>

            <!-- Destinations Section -->
            <div class="section">
                <h2 class="section-title">Travel Destinations</h2>
                <div class="card-grid">
                    {% for destination in destinations %}
                    <div class="card">
                        <h3>{{ destination.name }}</h3>
                        <p><strong>Country:</strong> {{ destination.country }}</p>
                        <p><strong>Category:</strong> {{ destination.category }}</p>
                        <p><strong>Price:</strong> ${{ "%.2f"|format(destination.price_per_person) }} per person</p>
                        <p><strong>Duration:</strong> {{ destination.duration_days }} days</p>
                        
                        <div class="feature-grid">
                            <div class="feature">
                                <strong>Luxury</strong><br>
                                {{ '★' * destination.luxury_rating }}
                            </div>
                            <div class="feature">
                                <strong>Adventure</strong><br>
                                Level {{ destination.adventure_level }}
                            </div>
                            <div class="feature">
                                <strong>Safety</strong><br>
                                {{ '★' * destination.safety_rating }}
                            </div>
                            <div class="feature">
                                <strong>Eco</strong><br>
                                {{ '★' * destination.sustainability_score }}
                            </div>
                        </div>
                        
                        <p><strong>Description:</strong> {{ destination.description }}</p>
                        <p><strong>Available:</strong> {{ 'Yes' if destination.available else 'No' }}</p>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Customers Section -->
            <div class="section">
                <h2 class="section-title">Registered Customers</h2>
                <div class="card-grid">
                    {% for customer in customers %}
                    <div class="card">
                        <h3>{{ customer.name }}</h3>
                        <p><strong>Email:</strong> {{ customer.email }}</p>
                        <p><strong>Phone:</strong> {{ customer.phone or 'Not provided' }}</p>
                        <p><strong>Preferences:</strong> {{ customer.preferences or 'No preferences set' }}</p>
                        <p><strong>Loyalty Points:</strong> <span class="rating">{{ customer.loyalty_points }}</span></p>
                        <p><strong>Member Since:</strong> {{ customer.created_date.strftime('%Y-%m-%d') if customer.created_date else 'N/A' }}</p>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Partners Section -->
            <div class="section">
                <h2 class="section-title">Local Partners</h2>
                <div class="card-grid">
                    {% for partner in partners %}
                    <div class="card">
                        <h3>{{ partner.name }}</h3>
                        <p><strong>Service Type:</strong> {{ partner.service_type }}</p>
                        <p><strong>Contact:</strong> {{ partner.contact_email }}</p>
                        <p><strong>Country:</strong> {{ partner.country }}</p>
                        <p><strong>Rating:</strong> 
                            <span class="rating">{{ partner.rating }}/5.0</span>
                            {{ '★' * partner.rating|int }}{{ '☆' * (5 - partner.rating|int) }}
                        </p>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Bookings Section -->
            <div class="section">
                <h2 class="section-title">Booking History</h2>
                {% if bookings %}
                <table class="bookings-table">
                    <thead>
                        <tr>
                            <th>Booking ID</th>
                            <th>Customer</th>
                            <th>Destination</th>
                            <th>Travel Date</th>
                            <th>People</th>
                            <th>Total Price</th>
                            <th>Status</th>
                            <th>Special Requests</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for booking in bookings %}
                        <tr>
                            <td>#{{ booking.id }}</td>
                            <td>{{ booking.customer_name }}</td>
                            <td>{{ booking.destination_name }}</td>
                            <td>{{ booking.travel_date.strftime('%Y-%m-%d') if booking.travel_date else 'N/A' }}</td>
                            <td>{{ booking.number_of_people }}</td>
                            <td>${{ "%.2f"|format(booking.total_price) }}</td>
                            <td><span class="status-confirmed">{{ booking.status }}</span></td>
                            <td>{{ booking.special_requests or 'None' }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <div class="no-data">
                    <p>No bookings found. Create your first booking!</p>
                </div>
                {% endif %}
            </div>
        </div>

        <!-- Add Customer Tab -->
        <div id="addCustomer" class="tab-content">
            <div class="form-container">
                <h2 class="section-title">Add New Customer</h2>
                <form method="POST" action="/add_customer">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="name">Full Name *</label>
                            <input type="text" id="name" name="name" required>
                        </div>
                        <div class="form-group">
                            <label for="email">Email Address *</label>
                            <input type="email" id="email" name="email" required>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="phone">Phone Number</label>
                            <input type="tel" id="phone" name="phone">
                        </div>
                        <div class="form-group">
                            <label for="loyalty_points">Loyalty Points</label>
                            <input type="number" id="loyalty_points" name="loyalty_points" value="0" min="0">
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="preferences">Travel Preferences</label>
                        <textarea id="preferences" name="preferences" placeholder="e.g., luxury, adventure, beach, cultural, sustainable..."></textarea>
                    </div>
                    <button type="submit" class="btn btn-success">Add Customer</button>
                </form>
            </div>
        </div>

        <!-- Add Destination Tab -->
        <div id="addDestination" class="tab-content">
            <div class="form-container">
                <h2 class="section-title">Add New Destination</h2>
                <form method="POST" action="/add_destination">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="dest_name">Destination Name *</label>
                            <input type="text" id="dest_name" name="dest_name" required>
                        </div>
                        <div class="form-group">
                            <label for="country">Country *</label>
                            <input type="text" id="country" name="country" required>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="category">Category *</label>
                            <select id="category" name="category" required>
                                <option value="">Select Category</option>
                                <option value="Luxury">Luxury</option>
                                <option value="Adventure">Adventure</option>
                                <option value="Cultural">Cultural</option>
                                <option value="Beach">Beach</option>
                                <option value="Mountain">Mountain</option>
                                <option value="City">City</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="price">Price Per Person ($) *</label>
                            <input type="number" id="price" name="price" step="0.01" min="0" required>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="duration">Duration (Days) *</label>
                            <input type="number" id="duration" name="duration" min="1" required>
                        </div>
                        <div class="form-group">
                            <label for="available">Available</label>
                            <select id="available" name="available">
                                <option value="1">Yes</option>
                                <option value="0">No</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="luxury_rating">Luxury Rating (1-5)</label>
                            <input type="number" id="luxury_rating" name="luxury_rating" min="1" max="5" value="3">
                        </div>
                        <div class="form-group">
                            <label for="adventure_level">Adventure Level (1-5)</label>
                            <input type="number" id="adventure_level" name="adventure_level" min="1" max="5" value="3">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="safety_rating">Safety Rating (1-5)</label>
                            <input type="number" id="safety_rating" name="safety_rating" min="1" max="5" value="4">
                        </div>
                        <div class="form-group">
                            <label for="sustainability_score">Sustainability Score (1-5)</label>
                            <input type="number" id="sustainability_score" name="sustainability_score" min="1" max="5" value="3">
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="description">Description *</label>
                        <textarea id="description" name="description" required placeholder="Describe the destination, amenities, experiences..."></textarea>
                    </div>
                    <button type="submit" class="btn btn-success">Add Destination</button>
                </form>
            </div>
        </div>

        <!-- Add Partner Tab -->
        <div id="addPartner" class="tab-content">
            <div class="form-container">
                <h2 class="section-title">Add New Partner</h2>
                <form method="POST" action="/add_partner">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="partner_name">Partner Name *</label>
                            <input type="text" id="partner_name" name="partner_name" required>
                        </div>
                        <div class="form-group">
                            <label for="service_type">Service Type *</label>
                            <select id="service_type" name="service_type" required>
                                <option value="">Select Service Type</option>
                                <option value="Accommodation">Accommodation</option>
                                <option value="Adventure Guides">Adventure Guides</option>
                                <option value="Local Tours">Local Tours</option>
                                <option value="Transportation">Transportation</option>
                                <option value="Cultural Guides">Cultural Guides</option>
                                <option value="Restaurant">Restaurant</option>
                                <option value="Spa & Wellness">Spa & Wellness</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="partner_email">Contact Email *</label>
                            <input type="email" id="partner_email" name="partner_email" required>
                        </div>
                        <div class="form-group">
                            <label for="partner_country">Country *</label>
                            <input type="text" id="partner_country" name="partner_country" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="partner_rating">Rating (1-5) *</label>
                        <input type="number" id="partner_rating" name="partner_rating" min="1" max="5" step="0.1" value="4.5" required>
                    </div>
                    <button type="submit" class="btn btn-success">Add Partner</button>
                </form>
            </div>
        </div>

        <!-- Create Booking Tab -->
        <div id="createBooking" class="tab-content">
            <div class="form-container">
                <h2 class="section-title">Create New Booking</h2>
                <form method="POST" action="/create_booking">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="customer_email">Customer Email *</label>
                            <select id="customer_email" name="customer_email" required>
                                <option value="">Select Customer</option>
                                {% for customer in customers %}
                                <option value="{{ customer.email }}">{{ customer.name }} ({{ customer.email }})</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="destination_id">Destination *</label>
                            <select id="destination_id" name="destination_id" required>
                                <option value="">Select Destination</option>
                                {% for destination in destinations %}
                                <option value="{{ destination.id }}">{{ destination.name }} - ${{ "%.2f"|format(destination.price_per_person) }}</option>
                                {% endfor %}
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="travel_date">Travel Date *</label>
                            <input type="date" id="travel_date" name="travel_date" required>
                        </div>
                        <div class="form-group">
                            <label for="number_of_people">Number of People *</label>
                            <input type="number" id="number_of_people" name="number_of_people" min="1" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="special_requests">Special Requests</label>
                        <textarea id="special_requests" name="special_requests" placeholder="Any special requirements, dietary restrictions, preferences..."></textarea>
                    </div>
                    <button type="submit" class="btn btn-success">Create Booking</button>
                </form>
            </div>
        </div>

        <!-- System Info -->
        <div class="section">
            <h2 class="section-title">System Information</h2>
            <div class="card">
                <p><strong>Database:</strong> MySQL - travel_agency</p>
                <p><strong>Total Tables:</strong> 4 (customers, destinations, bookings, partners)</p>
                <p><strong>Server:</strong> Flask Web Server</p>
                <p><strong>Status:</strong> Running Successfully</p>
                <p><strong>Last Updated:</strong> {{ current_time }}</p>
            </div>
        </div>
    </div>
</body>
</html>
'''

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="221652Aditya@#",  # Your password
            database="travel_agency"
        )
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    connection = get_db_connection()
    if not connection:
        return "Database connection failed"
    
    cursor = connection.cursor(dictionary=True)
    
    # Get comprehensive statistics
    stats = {}
    cursor.execute("SELECT COUNT(*) as count FROM customers")
    stats['total_customers'] = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM destinations")
    stats['total_destinations'] = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM partners")
    stats['total_partners'] = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM bookings")
    stats['total_bookings'] = cursor.fetchone()['count']
    
    cursor.execute("SELECT SUM(total_price) as total FROM bookings")
    stats['total_revenue'] = cursor.fetchone()['total'] or 0
    
    cursor.execute("SELECT AVG(total_price) as avg FROM bookings WHERE total_price > 0")
    stats['avg_booking_value'] = cursor.fetchone()['avg'] or 0
    
    # Get all destinations with full details
    cursor.execute("SELECT * FROM destinations")
    destinations = cursor.fetchall()
    
    # Get all customers
    cursor.execute("SELECT * FROM customers ORDER BY created_date DESC")
    customers = cursor.fetchall()
    
    # Get all partners
    cursor.execute("SELECT * FROM partners ORDER BY rating DESC")
    partners = cursor.fetchall()
    
    # Get all bookings with customer and destination names
    cursor.execute('''
        SELECT b.*, c.name as customer_name, d.name as destination_name 
        FROM bookings b 
        LEFT JOIN customers c ON b.customer_id = c.id 
        LEFT JOIN destinations d ON b.destination_id = d.id 
        ORDER BY b.booking_date DESC
    ''')
    bookings = cursor.fetchall()
    
    connection.close()
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return render_template_string(HTML_TEMPLATE, 
                                stats=stats, 
                                destinations=destinations, 
                                customers=customers,
                                partners=partners,
                                bookings=bookings,
                                current_time=current_time)

# Form handlers
@app.route('/add_customer', methods=['POST'])
def add_customer():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        name = request.form['name']
        email = request.form['email']
        phone = request.form.get('phone', '')
        preferences = request.form.get('preferences', '')
        loyalty_points = int(request.form.get('loyalty_points', 0))
        
        cursor.execute('''
            INSERT INTO customers (name, email, phone, preferences, loyalty_points)
            VALUES (%s, %s, %s, %s, %s)
        ''', (name, email, phone, preferences, loyalty_points))
        
        connection.commit()
        connection.close()
        flash('Customer added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding customer: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/add_destination', methods=['POST'])
def add_destination():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        name = request.form['dest_name']
        country = request.form['country']
        category = request.form['category']
        description = request.form['description']
        price_per_person = float(request.form['price'])
        duration_days = int(request.form['duration'])
        luxury_rating = int(request.form['luxury_rating'])
        adventure_level = int(request.form['adventure_level'])
        safety_rating = int(request.form['safety_rating'])
        sustainability_score = int(request.form['sustainability_score'])
        available = bool(int(request.form['available']))
        
        cursor.execute('''
            INSERT INTO destinations (name, country, category, description, price_per_person, 
                                    duration_days, luxury_rating, adventure_level, safety_rating, 
                                    sustainability_score, available)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (name, country, category, description, price_per_person, duration_days,
              luxury_rating, adventure_level, safety_rating, sustainability_score, available))
        
        connection.commit()
        connection.close()
        flash('Destination added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding destination: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/add_partner', methods=['POST'])
def add_partner():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        name = request.form['partner_name']
        service_type = request.form['service_type']
        contact_email = request.form['partner_email']
        country = request.form['partner_country']
        rating = float(request.form['partner_rating'])
        
        cursor.execute('''
            INSERT INTO partners (name, service_type, contact_email, country, rating)
            VALUES (%s, %s, %s, %s, %s)
        ''', (name, service_type, contact_email, country, rating))
        
        connection.commit()
        connection.close()
        flash('Partner added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding partner: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/create_booking', methods=['POST'])
def create_booking():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        customer_email = request.form['customer_email']
        destination_id = int(request.form['destination_id'])
        travel_date = request.form['travel_date']
        number_of_people = int(request.form['number_of_people'])
        special_requests = request.form.get('special_requests', '')
        
        # Get customer ID
        cursor.execute("SELECT id FROM customers WHERE email = %s", (customer_email,))
        customer_result = cursor.fetchone()
        if not customer_result:
            flash('Customer not found!', 'error')
            return redirect(url_for('index'))
        
        customer_id = customer_result[0]
        
        # Get destination price
        cursor.execute("SELECT price_per_person FROM destinations WHERE id = %s", (destination_id,))
        destination_result = cursor.fetchone()
        if not destination_result:
            flash('Destination not found!', 'error')
            return redirect(url_for('index'))
        
        price_per_person = destination_result[0]
        total_price = price_per_person * number_of_people
        
        # Create booking
        cursor.execute('''
            INSERT INTO bookings (customer_id, destination_id, travel_date, number_of_people, total_price, special_requests)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (customer_id, destination_id, travel_date, number_of_people, total_price, special_requests))
        
        connection.commit()
        connection.close()
        flash('Booking created successfully!', 'success')
    except Exception as e:
        flash(f'Error creating booking: {str(e)}', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("Starting Enhanced Travel Agency Web Server with Forms...")
    print("Open your browser and go to: http://localhost:5000")
    print("Now you can add customers, destinations, partners, and create bookings through the web interface!")
    app.run(debug=True, host='0.0.0.0', port=5000)