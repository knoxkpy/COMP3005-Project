import admin
import member
import trainer
import sys
import psycopg

def connectToDataBase():
    dbname = "Health and Fitness Club Management"
    user = "postgres"
    #use your own password here for the database. its 
    password = "232189499"
    host = "localhost"
    port = "5432"

    try:
        conn = psycopg.connect(dbname = dbname, user = user, password = password, host = host, port=port)
        print("Connecting to the database...")
        return conn
    except psycopg.OperationalError as e:
        print(f"Error: {e}")
        print("Cannot connect to database")
        return False

def createTable(conn):
    cursor = conn.cursor()

    ##ddl statement
    createTableSql = '''
    CREATE TABLE IF NOT EXISTS Members (
        MemberID SERIAL PRIMARY KEY,
        Name VARCHAR(255) UNIQUE NOT NULL,
        Email VARCHAR(255) UNIQUE NOT NULL,
        Password VARCHAR(255) NOT NULL,
        DateOfBirth DATE NOT NULL,
        Gender VARCHAR(50),
        FitnessGoals TEXT,
        HealthMetrics JSONB
    );

    CREATE TABLE IF NOT EXISTS Trainers (
        TrainerID SERIAL PRIMARY KEY,
        Name VARCHAR(255) UNIQUE NOT NULL,
        Email VARCHAR(255) UNIQUE NOT NULL,
        Password VARCHAR(255) NOT NULL,
        Specialization VARCHAR(255)
    );

    CREATE TABLE IF NOT EXISTS Admin (
        AdminID SERIAL PRIMARY KEY,
        Username VARCHAR(255) UNIQUE NOT NULL,
        Email VARCHAR(255) UNIQUE NOT NULL,
        Password VARCHAR(255) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS TrainerAvailability (
        AvailabilityID SERIAL PRIMARY KEY,
        TrainerID INT REFERENCES Trainers(TrainerID),
        AvailableFrom TIMESTAMP NOT NULL,
        AvailableTo TIMESTAMP NOT NULL,
        Status VARCHAR(50) DEFAULT 'Available' NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Rooms (
        RoomID SERIAL PRIMARY KEY,
        RoomName VARCHAR(255) NOT NULL,
        Capacity INT
    );

    CREATE TABLE IF NOT EXISTS Equipment (
        EquipmentID SERIAL PRIMARY KEY,
        EquipmentName VARCHAR(255) NOT NULL,
        Status VARCHAR(50) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Classes (
        ClassID SERIAL PRIMARY KEY,
        ClassName VARCHAR(255) NOT NULL,
        RoomID INT REFERENCES Rooms(RoomID),
        TrainerID INT REFERENCES Trainers(TrainerID),
        Schedule TIMESTAMP NOT NULL,
        Capacity INT
    );

    CREATE TABLE IF NOT EXISTS Bookings (
        BookingID SERIAL PRIMARY KEY,
        MemberID INT REFERENCES Members(MemberID),
        TrainerID INT REFERENCES Trainers(TrainerID),
        ClassID INT REFERENCES Classes(ClassID),
        Date DATE NOT NULL,
        Time TIME NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Payments (
        PaymentID SERIAL PRIMARY KEY,
        MemberID INT REFERENCES Members(MemberID),
        Amount DECIMAL(10, 2) NOT NULL,
        PaymentDate DATE NOT NULL,
        Service VARCHAR(255) NOT NULL
    );
    '''

    try:
        cursor.execute(createTableSql)
        conn.commit()
        print("Table created successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()

def registration(conn):
    print("\nWelcome to account registration.")

    # Definitation for the invitation code for trainers and admins (assuming that for staff they need the special code to register.)
    inviteCodeTrainer = 'TRAINER2024'
    inviteCodeAdmin = 'ADMIN2024'

    try:
        regType = int(input("Which type of account do you want to register?\n1. Member\n2. Trainer\n3. Admin\n*For trainer and admin registration, you need to have the invite code: "))
        
        if regType not in [1, 2, 3]:
            print("Please enter a valid option (1, 2, or 3)!")
            return False

        name = input("Enter your username: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        if regType == 1:  # Member registration
            date_of_birth = input("Enter your date of birth (YYYY-MM-DD): ")
            gender = input("Enter your gender: ")
            fitness_goals = input("Enter your fitness goals: ")
            health_metrics = input("Enter your initial health metrics (as JSON string, e.g., '{\"weight\": 70, \"height\": 175}'): ")

            cursor = conn.cursor()
            cursor.execute("INSERT INTO Members (Name, Email, Password, DateOfBirth, Gender, FitnessGoals, HealthMetrics) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (name, email, password, date_of_birth, gender, fitness_goals, health_metrics))
            conn.commit()
            print("Member registration completed successfully.")
        elif regType in [2, 3]:  # Trainer or Admin registration
            inviteCode = input("Enter your invite code: ")
            correctInviteCode = inviteCodeTrainer if regType == 2 else inviteCodeAdmin
            
            if inviteCode != correctInviteCode:
                print("Invalid invite code.")
                return False

            if regType == 2:  # Trainer
                specialization = input("Enter your specialization: ")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Trainers (Name, Email, Password, Specialization) VALUES (%s, %s, %s, %s)",
                               (name, email, password, specialization))
                conn.commit()
                print("Trainer registration completed successfully.")
            elif regType == 3:  # Admin
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Admin (Username, Email, Password) VALUES (%s, %s, %s)",
                               (name, email, password))
                conn.commit()
                print("Admin registration completed successfully.")

    except Exception as e:
        print(f"An error occurred during registration: {e}")
        conn.rollback()
        return False

    return True


def login(conn):
    print("\nLogin to your account.")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor = conn.cursor()

    # Check in each table for a match and retrieve the ID as well.
    cursor.execute("""
        SELECT 'Members', MemberID FROM Members WHERE Name = %s AND Password = %s
        UNION
        SELECT 'Trainer', TrainerID FROM Trainers WHERE Name = %s AND Password = %s
        UNION
        SELECT 'Admin', AdminID FROM Admin WHERE Username = %s AND Password = %s
    """, (username, password, username, password, username, password))
    result = cursor.fetchone()

    if result:
        role, user_id = result
        print(f"Login successful. You are logged in as a {role}.")
        return role, user_id
    else:
        print("Login failed. Please check your credentials.")
        return None, None


def main():
    conn = connectToDataBase()
    if (conn == False):
        sys.exit()

    ##'using IF NOT EXIST" preventing duplicating the table
    createTable(conn)

    while True:
        print("\nWelcome to the Health and Fitness Club Management System. Please select what you want to do.")
        print("1. Register an account")
        print("2. Login")
        print("3. Exit")
        
        while True:
            try:
                userInput = int(input('Your selection: '))
                break
            except ValueError as error:
                print(f'Error exists: {error}\nPlease try again!')

        if userInput == 1:
            regis = registration(conn)
            
            if regis == False:
                print("Registration Failed. Please try again!\n")
            else:
                print("Registration completed. You can now login to your account!\n")
        elif userInput == 2:
            role, userId = login(conn)
            if role == "Members":
                member.showMemberMenu(conn, userId)
            elif role == "Trainer":
                trainer.showTrainerMenu(conn, userId)
            elif role == "Admin":
                admin.showAdminMenu(conn, userId)
        elif userInput == 3:
            print("Exiting the system...")
            sys.exit()
        else:
            print("Please enter a valid option!\n")
       

main()