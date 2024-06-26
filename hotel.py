import streamlit as st
import sqlite3
import hashlib
from sqlite3 import Error

# Utility Functions
def create_connection(db_file):
    """Create a database connection to SQLite database"""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        return None

def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def hash_password(password):
    """Hash a password for storing"""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(conn, username, password):
    """Insert a new user into the users table"""
    sql = ''' INSERT INTO users(username, password) VALUES(?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (username, hash_password(password)))
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(e)
        return None

def authenticate_user(conn, username, password):
    """Authenticate user login"""
    sql = ''' SELECT * FROM users WHERE username = ? AND password = ? '''
    cur = conn.cursor()
    cur.execute(sql, (username, hash_password(password)))
    user = cur.fetchone()
    return user

def add_hotel(conn, name, address, rating, contact):
    """Insert a new hotel into the hotels table"""
    sql = ''' INSERT INTO hotels(name, address, rating, contact) VALUES(?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (name, address, rating, contact))
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(e)
        return None

def view_hotels(conn):
    """Query all rows in the hotels table"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM hotels")
    rows = cur.fetchall()
    return rows

def add_room(conn, number, room_type, rate, status, hotel_id):
    """Insert a new room into the rooms table"""
    sql = ''' INSERT INTO rooms(number, room_type, rate, status, hotel_id) VALUES(?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (number, room_type, rate, status, hotel_id))
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(e)
        return None

def view_rooms(conn, hotel_id):
    """Query all rooms for a specific hotel"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM rooms WHERE hotel_id=?", (hotel_id,))
    rows = cur.fetchall()
    return rows

def add_guest(conn, name, address, contact):
    """Insert a new guest into the guests table"""
    sql = ''' INSERT INTO guests(name, address, contact) VALUES(?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (name, address, contact))
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(e)
        return None

def view_guests(conn):
    """Query all rows in the guests table"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM guests")
    rows = cur.fetchall()
    return rows

def add_reservation(conn, guest_id, room_number, checkin_date, checkout_date, status):
    """Insert a new reservation into the reservations table"""
    sql = ''' INSERT INTO reservations(guest_id, room_number, checkin_date, checkout_date, status) VALUES(?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (guest_id, room_number, checkin_date, checkout_date, status))
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(e)

def view_reservations(conn):
    """Query all rows in the reservations table"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM reservations")
    rows = cur.fetchall()
    return rows

# Service types and their fixed costs
service_types = {
    "Room Service": 50.0,
    "Laundry": 30.0,
    "Food & Beverage": 100.0,
    "Spa": 150.0
}

def add_service(conn, reservation_id, service_type):
    """Insert a new service into the services table"""
    try:
        charge = service_types.get(service_type)
        if charge is None:
            raise ValueError("Invalid service type")
        sql = ''' INSERT INTO services(reservation_id, type, charge) VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (reservation_id, service_type, charge))
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(e)
        return None

def view_services(conn, reservation_id):
    """Query all services for a specific reservation"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM services WHERE reservation_id=?", (reservation_id,))
        rows = cur.fetchall()
        services = []
        for row in rows:
            service = {
                "ID": row[0],
                "Reservation ID": row[1],
                "Type": row[2],
                "Charge": row[3]
            }
            services.append(service)
        return services
    except Error as e:
        print(e)
        return None

def add_staff(conn, name, position, contact):
    """Insert a new staff member into the staff table"""
    sql = ''' INSERT INTO staff(name, position, contact) VALUES(?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (name, position, contact))
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(e)
        return None

def view_staff(conn):
    """Query all rows in the staff table"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM staff")
    rows = cur.fetchall()
    return rows

# Database connection and table creation
database = "hotel_management.db"
conn = create_connection(database)

sql_create_hotels_table = """ CREATE TABLE IF NOT EXISTS hotels (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                address TEXT NOT NULL,
                                rating REAL,
                                contact TEXT NOT NULL
                            ); """

sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT UNIQUE NOT NULL,
                                password TEXT NOT NULL
                            ); """

sql_create_rooms_table = """ CREATE TABLE IF NOT EXISTS rooms (
                                number INTEGER PRIMARY KEY,
                                room_type TEXT NOT NULL,
                                rate REAL NOT NULL,
                                status TEXT NOT NULL,
                                hotel_id INTEGER NOT NULL,
                                FOREIGN KEY (hotel_id) REFERENCES hotels (id)
                            ); """

sql_create_guests_table = """ CREATE TABLE IF NOT EXISTS guests (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                address TEXT NOT NULL,
                                contact TEXT NOT NULL
                            ); """

sql_create_reservations_table = """ CREATE TABLE IF NOT EXISTS reservations (
                                        id INTEGER PRIMARY KEY,
                                        guest_id INTEGER NOT NULL,
                                        room_number INTEGER NOT NULL,
                                        checkin_date TEXT NOT NULL,
                                        checkout_date TEXT NOT NULL,
                                        status TEXT NOT NULL,
                                        FOREIGN KEY (guest_id) REFERENCES guests (id),
                                        FOREIGN KEY (room_number) REFERENCES rooms (number)
                                    ); """

sql_create_services_table = """ CREATE TABLE IF NOT EXISTS services (
                                    id INTEGER PRIMARY KEY,
                                    reservation_id INTEGER NOT NULL,
                                    type TEXT NOT NULL,
                                    charge REAL NOT NULL,
                                    FOREIGN KEY (reservation_id) REFERENCES reservations (id)
                                ); """

sql_create_staff_table = """ CREATE TABLE IF NOT EXISTS staff (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                position TEXT NOT NULL,
                                contact TEXT NOT NULL
                            ); """

if conn is not None:
    create_table(conn, sql_create_hotels_table)
    create_table(conn, sql_create_users_table)
    create_table(conn, sql_create_rooms_table)
    create_table(conn, sql_create_guests_table)
    create_table(conn, sql_create_reservations_table)
    create_table(conn, sql_create_services_table)
    create_table(conn, sql_create_staff_table)
else:
    print("Error! Cannot create the database connection.")

# Main Application
def main():
    st.title("Hotel Management System")

    # Initialize session state variables
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'user' not in st.session_state:
        st.session_state['user'] = None

    # User Authentication
    auth_conn = create_connection(database)
    if auth_conn is None:
        st.error("Error: Unable to connect to database.")
        return

    # Sidebar for Sign-in and Login
    st.sidebar.subheader("Authentication")
    if st.session_state['logged_in']:
        st.sidebar.write(f"Logged in as: {st.session_state['user']}")
        if st.sidebar.button("Log Out"):
            st.session_state['logged_in'] = False
            st.session_state['user'] = None
            st.experimental_rerun()
    else:
        auth_choice = st.sidebar.selectbox("Choose", ["Sign In", "Log In"], key="auth_choice")
        if auth_choice == "Sign In":
            st.subheader("Create a New Account")
            new_username = st.text_input("Username", key="new_username")
            new_password = st.text_input("Password", type='password', key="new_password")
            if st.button("Sign In"):
                if new_username and new_password:
                    user_id = add_user(auth_conn, new_username, new_password)
                    if user_id:
                        st.success(f"Account created successfully with ID: {user_id}")
                    else:
                        st.error("Error: Username already exists or other error.")
                else:
                    st.error("Please fill in all fields.")
        elif auth_choice == "Log In":
            st.subheader("Log In to Your Account")
            username = st.text_input("Username", key="username")
            password = st.text_input("Password", type='password', key="password")
            if st.button("Log In"):
                if username and password:
                    user = authenticate_user(auth_conn, username, password)
                    if user:
                        st.session_state['logged_in'] = True
                        st.session_state['user'] = username
                        st.success("Logged in successfully")
                        st.experimental_rerun()
                    else:
                        st.error("Error: Invalid username or password.")
                else:
                    st.error("Please fill in all fields.")

    if st.session_state['logged_in']:
        app(conn)

def app(conn):
    # Sidebar for app navigation
    st.sidebar.subheader("Options")
    menu = ["Home", "Hotels", "Rooms", "Guests", "Reservations", "Services", "Staff"]
    choice = st.sidebar.selectbox("Menu", menu, key="menu")

    if choice == "Home":
        st.subheader("Welcome to the Hotel Management System")
    elif choice == "Hotels":
        st.subheader("Hotels Management")

        # Add Hotel
        st.subheader("Add a New Hotel")
        name = st.text_input("Hotel Name")
        address = st.text_input("Hotel Address")
        rating = st.number_input("Hotel Rating", min_value=0.0, max_value=5.0, step=0.1)
        contact = st.text_input("Hotel Contact")
        if st.button("Add Hotel"):
            if name and address and contact:
                hotel_id = add_hotel(conn, name, address, rating, contact)
                if hotel_id:
                    st.success(f"Hotel added successfully with ID: {hotel_id}")
                else:
                    st.error("Error: Unable to add hotel.")
            else:
                st.error("Please fill in all the fields.")

        # View Hotels
        st.subheader("View Hotels")
        hotels = view_hotels(conn)
        if hotels:
            st.write("All Hotels:")
            st.table(hotels)
        else:
            st.info("No hotels available.")

    elif choice == "Rooms":
        st.subheader("Rooms Management")

        # Add Room
        st.subheader("Add a New Room")
        number = st.number_input("Room Number", min_value=1, step=1)
        room_type = st.text_input("Room Type")
        rate = st.number_input("Room Rate", min_value=0.0, step=0.1)
        status = st.selectbox("Room Status", ["Available", "Occupied", "Under Maintenance"])
        hotel_id = st.number_input("Hotel ID", min_value=1, step=1)
        if st.button("Add Room"):
            if number and room_type and rate and status and hotel_id:
                room_id = add_room(conn, number, room_type, rate, status, hotel_id)
                if room_id:
                    st.success(f"Room added successfully with ID: {room_id}")
                else:
                    st.error("Error: Unable to add room.")
            else:
                st.error("Please fill in all the fields.")

        # View Rooms
        st.subheader("View Rooms")
        hotel_id = st.number_input("Hotel ID for Rooms", min_value=1, step=1, key="view_rooms_hotel_id")
        if st.button("View Rooms"):
            rooms = view_rooms(conn, hotel_id)
            if rooms:
                st.write("Rooms for Hotel ID:", hotel_id)
                st.table(rooms)
            else:
                st.info("No rooms available for this hotel.")

    elif choice == "Guests":
        st.subheader("Guests Management")

        # Add Guest
        st.subheader("Add a New Guest")
        guest_name = st.text_input("Guest Name")
        guest_address = st.text_input("Guest Address")
        guest_contact = st.text_input("Guest Contact")
        if st.button("Add Guest"):
            if guest_name and guest_address and guest_contact:
                guest_id = add_guest(conn, guest_name, guest_address, guest_contact)
                if guest_id:
                    st.success(f"Guest added successfully with ID: {guest_id}")
                else:
                    st.error("Error: Unable to add guest.")
            else:
                st.error("Please fill in all the fields.")

        # View Guests
        st.subheader("View Guests")
        guests = view_guests(conn)
        if guests:
            st.write("All Guests:")
            st.table(guests)
        else:
            st.info("No guests available.")

    elif choice == "Reservations":
        st.subheader("Reservations Management")

        # Add Reservation
        st.subheader("Add a New Reservation")
        guest_id = st.number_input("Guest ID", min_value=1, step=1)
        room_number = st.number_input("Room Number", min_value=1, step=1)
        checkin_date = st.date_input("Check-in Date")
        checkout_date = st.date_input("Check-out Date")
        status = st.selectbox("Reservation Status", ["Booked", "Checked-in", "Checked-out"])
        if st.button("Add Reservation"):
            if guest_id and room_number and checkin_date and checkout_date and status:
                # Convert date objects to string in YYYY-MM-DD format
                checkin_date_str = checkin_date.strftime('%Y-%m-%d')
                checkout_date_str = checkout_date.strftime('%Y-%m-%d')
                reservation_id = add_reservation(conn, guest_id, room_number, checkin_date_str, checkout_date_str, status)
                if reservation_id:
                    st.success(f"Reservation added successfully with ID: {reservation_id}")
                else:
                    st.error("Error: Unable to add reservation.")
            else:
                st.error("Please fill in all the fields.")

        # View Reservations
        st.subheader("View Reservations")
        reservations = view_reservations(conn)
        if reservations:
            st.write("All Reservations:")
            st.table(reservations)
        else:
            st.info("No reservations available.")

    elif choice == "Services":
        st.subheader("Services Management")

        # Add Service
        st.subheader("Add a New Service")
        reservation_id = st.number_input("Reservation ID", min_value=1, step=1)
        service_type = st.selectbox("Service Type", list(service_types.keys()))
        if st.button("Add Service"):
            if reservation_id and service_type:
                service_id = add_service(conn, reservation_id, service_type)
                if service_id:
                    st.success(f"Service added successfully with ID: {service_id}")
                else:
                    st.error("Error: Unable to add service.")
            else:
                st.error("Please fill in all the fields.")

        # View Services
        st.subheader("View Services")
        reservation_id = st.number_input("Reservation ID for Services", min_value=1, step=1, key="view_services_reservation_id")
        if st.button("View Services"):
            services = view_services(conn, reservation_id)
            if services:
                st.write("Services for Reservation ID:", reservation_id)
                st.table(services)
            else:
                st.info("No services available for this reservation.")

    elif choice == "Staff":
        st.subheader("Staff Management")

        # Add Staff
        st.subheader("Add a New Staff Member")
        staff_name = st.text_input("Staff Name")
        staff_position = st.text_input("Staff Position")
        staff_contact = st.text_input("Staff Contact")
        if st.button("Add Staff"):
            if staff_name and staff_position and staff_contact:
                staff_id = add_staff(conn, staff_name, staff_position, staff_contact)
                if staff_id:
                    st.success(f"Staff added successfully with ID: {staff_id}")
                else:
                    st.error("Error: Unable to add staff.")
            else:
                st.error("Please fill in all the fields.")

        # View Staff
        st.subheader("View Staff")
        staff = view_staff(conn)
        if staff:
            st.write("All Staff:")
            st.table(staff)
        else:
            st.info("No staff available.")

if __name__ == "__main__":
    main()
