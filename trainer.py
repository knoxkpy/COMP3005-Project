import psycopg

def addTrainerAvailability(conn, trainerID):
    print("\nSet your availability:")
    available_from = input("Enter start datetime (YYYY-MM-DD HH:MM): ")
    available_to = input("Enter end datetime (YYYY-MM-DD HH:MM): ")
    # Convert input to TIMESTAMP if needed and validate the inputs

    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO TrainerAvailability (TrainerID, AvailableFrom, AvailableTo)
            VALUES (%s, %s, %s)
        """, (trainerID, available_from, available_to))
        conn.commit()
        print("Availability added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()

def viewTrainerAvailability(conn, trainerID):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT AvailabilityID, AvailableFrom, AvailableTo, Status 
        FROM TrainerAvailability 
        WHERE TrainerID = %s ORDER BY AvailableFrom
    """, (trainerID,))
    availabilities = cursor.fetchall()

    if not availabilities:
        print("You have no scheduled availabilities.")
        return
    
    print("\nYour current availability:")
    for availability in availabilities:
        print(f"ID: {availability[0]}, From: {availability[1]}, To: {availability[2]}, Status: {availability[3]}")


def removeTrainerAvailability(conn, trainerID):
    viewTrainerAvailability(conn, trainerID)
    
    availability_id = input("Enter the ID of the availability slot you wish to remove: ")

    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM TrainerAvailability 
            WHERE AvailabilityID = %s AND TrainerID = %s AND (AvailableFrom > CURRENT_TIMESTAMP OR Status = 'Available')
        """, (availability_id, trainerID))
        
        if cursor.rowcount == 0:
            print("No matching availability found, or it cannot be removed.")
        else:
            conn.commit()
            print("Availability removed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        
        
def viewAssignedMemberProfiles(conn, trainerID):
    cursor = conn.cursor()
    try:
        query = """
        SELECT 
            m.MemberID, 
            m.Name, 
            m.Email, 
            m.DateOfBirth, 
            m.Gender, 
            m.FitnessGoals, 
            m.HealthMetrics, 
            COALESCE(c.ClassName, 'Personal Training Session') AS SessionType,
            b.Date, 
            b.Time
        FROM 
            Members m
        JOIN 
            Bookings b ON m.MemberID = b.MemberID
        LEFT JOIN 
            Classes c ON b.ClassID = c.ClassID AND b.TrainerID = c.TrainerID
        WHERE 
            b.TrainerID = %s
        ORDER BY 
            b.Date, b.Time;
        """
        cursor.execute(query, (trainerID,))
        members = cursor.fetchall()
        
        if not members:
            print("No members are currently assigned to your classes or personal training sessions.")
            return

        print("\nMember Details for Your Classes and Personal Training Sessions:")
        for member in members:
            print(f"ID: {member[0]}, Name: {member[1]}, Email: {member[2]}, Date of Birth: {member[3]}, Gender: {member[4]}, Fitness Goals: {member[5]}, Health Metrics: {member[6]}, Session Type: {member[7]} on {member[8]} at {member[9]}")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()

        
def searchMemberProfileByName(conn, trainerID):
    search_name = input("Enter the member's name to search: ")

    cursor = conn.cursor()
    try:
        query = """
        SELECT DISTINCT m.MemberID, m.Name, m.Email, m.DateOfBirth, m.Gender, m.FitnessGoals, m.HealthMetrics
        FROM Members m
        INNER JOIN Bookings b ON m.MemberID = b.MemberID
        INNER JOIN Classes c ON b.ClassID = c.ClassID
        WHERE c.TrainerID = %s AND m.Name ILIKE %s;
        """
        search_pattern = f'%{search_name}%'
        cursor.execute(query, (trainerID, search_pattern))
        members = cursor.fetchall()

        if not members:
            print("No members found with the given name.")
            return

        print("\nSearch Results:")
        for member in members:
            print(f"ID: {member[0]}, Name: {member[1]}, Email: {member[2]}, Date of Birth: {member[3]}, Gender: {member[4]}, Fitness Goals: {member[5]}")
            print("Health Metrics:")
            if member[6]:
                for key, value in member[6].items():
                    print(f"  {key}: {value}")
            else:
                print("  No health metrics available.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()


def showTrainerMenu(conn, trainerID):
    while True:
        print("\nTrainer Menu:")
        print("1. Schedule Management")
        print("2. Member Profile Viewing")
        print("3. Search Member Profile by Name")
        print("4. Logout")
        # Implement functionalities

        userInput = input('Please enter your option: ')

        if userInput == "1":
            print('\nYou can check all your schedule here:')
            print("1. Add your availability.")
            print("2. View your current availability")
            print("3. View and remove your current availability.")
            print('4. Back to main menu.')
            
            choice = input('Please enter your choice: ')

            if choice == '1':
                addTrainerAvailability(conn, trainerID)
            elif choice == '2':
                viewTrainerAvailability(conn, trainerID)
            elif choice == '3':
                removeTrainerAvailability(conn, trainerID)
            elif choice == '4':
                continue
            else:
                print("Please enter a valid input.")
        elif userInput == "2":
            viewAssignedMemberProfiles(conn, trainerID)
        elif userInput == "3":
            searchMemberProfileByName(conn, trainerID)    
        elif userInput == "4":
            print("Logging out...")
            break
        else:
            print("Please enter a valid input...")
