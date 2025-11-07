import mysql.connector
from mysql.connector import Error

def setup_database():
    try:
        # Connect to MySQL server without specifying database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="221652Aditya@#"  # Change this to your MySQL password
        )
        
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS travel_agency")
        cursor.execute("USE travel_agency")
        print("Database 'travel_agency' created successfully")
        
        # Create customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                phone VARCHAR(20),
                preferences TEXT,
                loyalty_points INT DEFAULT 0,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("Table 'customers' created successfully")
        
        # Create destinations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS destinations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                country VARCHAR(100) NOT NULL,
                category VARCHAR(50) NOT NULL,
                description TEXT,
                price_per_person DECIMAL(10,2) NOT NULL,
                duration_days INT NOT NULL,
                luxury_rating INT DEFAULT 1,
                adventure_level INT DEFAULT 1,
                safety_rating INT DEFAULT 5,
                sustainability_score INT DEFAULT 3,
                available BOOLEAN DEFAULT TRUE
            )
        ''')
        print("Table 'destinations' created successfully")
        
        # Create bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                destination_id INT,
                booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                travel_date DATE NOT NULL,
                number_of_people INT NOT NULL,
                total_price DECIMAL(10,2) NOT NULL,
                status VARCHAR(50) DEFAULT 'confirmed',
                special_requests TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
                FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE
            )
        ''')
        print("Table 'bookings' created successfully")
        
        # Create partners table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS partners (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                service_type VARCHAR(100) NOT NULL,
                contact_email VARCHAR(255),
                country VARCHAR(100),
                rating DECIMAL(3,2) DEFAULT 5.0
            )
        ''')
        print("Table 'partners' created successfully")
        
        # Insert sample data
        insert_sample_data(cursor)
        
        connection.commit()
        print("All tables created and sample data inserted successfully!")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def insert_sample_data(cursor):
    # Insert sample destinations
    destinations = [
        ('Maldives Luxury Resort', 'Maldives', 'Luxury', 
         'Private overwater bungalows with personal butler service', 4500.00, 7, 5, 1, 5, 4, True),
        
        ('Swiss Alps Adventure', 'Switzerland', 'Adventure', 
         'Guided mountain climbing and skiing with safety experts', 2800.00, 5, 4, 5, 4, 5, True),
        
        ('Kyoto Cultural Journey', 'Japan', 'Cultural', 
         'Traditional tea ceremonies and temple visits', 2200.00, 6, 4, 2, 5, 5, True),
        
        ('Safari Kenya', 'Kenya', 'Adventure', 
         'Wildlife safari with eco-friendly lodges', 3200.00, 8, 3, 4, 4, 5, True),
        
        ('Paris Luxury Tour', 'France', 'Luxury', 
         '5-star hotels with private guided tours', 3800.00, 5, 5, 1, 5, 3, True)
    ]
    
    cursor.executemany('''
        INSERT IGNORE INTO destinations (name, country, category, description, price_per_person, 
                        duration_days, luxury_rating, adventure_level, safety_rating, sustainability_score, available)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', destinations)
    print("Sample destinations inserted")
    
    # Insert sample partners
    partners = [
        ('Alpine Guides Co.', 'Adventure Guides', 'contact@alpineguides.com', 'Switzerland', 4.8),
        ('Luxury Stays Inc.', 'Accommodation', 'info@luxurystays.com', 'Global', 4.9),
        ('Eco Travel Kenya', 'Local Tours', 'hello@ecotravelkenya.com', 'Kenya', 4.7),
        ('Japanese Culture Experts', 'Cultural Guides', 'tours@japaneseculture.com', 'Japan', 4.9)
    ]
    
    cursor.executemany('''
        INSERT IGNORE INTO partners (name, service_type, contact_email, country, rating)
        VALUES (%s, %s, %s, %s, %s)
    ''', partners)
    print("Sample partners inserted")
    
    # Insert a sample customer
    cursor.execute('''
        INSERT IGNORE INTO customers (name, email, phone, preferences, loyalty_points)
        VALUES (%s, %s, %s, %s, %s)
    ''', ('John Doe', 'john.doe@example.com', '+1234567890', 'luxury, adventure', 50))
    print("Sample customer inserted")

if __name__ == "__main__":
    setup_database()