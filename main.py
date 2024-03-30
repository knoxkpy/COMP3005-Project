import admin
import member
import trainer
import sys
import psycopg

def connectToDataBase():
    dbname = "Health and Fitness Club Management"
    user = "postgres"
    #use your own password here for the database. its 
    password = "postgres"
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
        Name VARCHAR(255) NOT NULL,
        Email VARCHAR(255) UNIQUE NOT NULL,
        Password VARCHAR(255) NOT NULL,
        DateOfBirth DATE NOT NULL,
        Gender VARCHAR(50),
        FitnessGoals TEXT,
        HealthMetrics JSONB
    );

    CREATE TABLE IF NOT EXISTS Trainers (
        TrainerID SERIAL PRIMARY KEY,
        Name VARCHAR(255) NOT NULL,
        Specialization VARCHAR(255)
    );

    CREATE TABLE IF NOT EXISTS Admin (
        AdminID SERIAL PRIMARY KEY,
        Username VARCHAR(255) UNIQUE NOT NULL,
        Password VARCHAR(255) NOT NULL
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

def registration() -> bool:
    print("\nWelcome to account registration.")

    while True:
        try:
            regType = int(input("which type of account you want to register?\n1. Member 2. Trainer\n3. Admin\n*For trainer and admin registration, you need to have the invite code."))
        except:
            print("Please enter a valid input!\n")

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
        print("3. Manage Room Booking")
        print("4. Exit")
        
        while True:
            try:
                userInput = int(input('Your selection: '))
                break
            except ValueError as error:
                print(f'Error exists: {error}\nPlease try again!')

        if userInput == 1:
            regis = registration()
            
            if regis == False:
                print("Registration Failed. Please try again!\n")
            else:
                print("Registration completed. You can now login to your account!\n")
        elif userInput == 2:
            break
            pass
        elif userInput == 3:
            ## Testing the monitor_equipment_maintenance function in admin.py
            admin.monitor_equipment_maintenance(conn)
        elif userInput == 4:
            print("Exiting the system...")
            sys.exit()
        else:
            print("Please enter a valid option!\n")
       

main()