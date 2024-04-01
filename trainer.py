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


def showTrainerMenu(conn, trainerID):
    while True:
        print("\nTrainer Menu:")
        print("1. Schedule Management")
        print("2. Member Profile Viewing")
        print("3. Logout")
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
            pass
        elif userInput == "3":
            print("Logging out...")
            break
        else:
            print("Please enter a valid input...")
