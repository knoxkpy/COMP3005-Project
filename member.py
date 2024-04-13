import psycopg

def update_profile(conn, member_id):
    print("\nProfile Management")
    print("Leave it blank if you do not wish to change a field.")

    name = input("Enter your new name: ")
    email = input("Enter your new email: ")
    password = input("Enter your new password: ")
    date_of_birth = input("Enter your new date of birth (YYYY-MM-DD): ")
    gender = input("Enter your new gender: ")
    fitness_goals = input("Enter your new fitness goals: ")
    health_metrics = input("Enter your new health metrics (as JSON string, e.g., '{\"weight\": 70, \"height\": 175}, \"achievements\": [{\"title\": \"5K Run\", \"date\": \"2023-01-01\"}, ...]'): ")

    update_fields = []
    params = []

    if name:
        update_fields.append("Name = %s")
        params.append(name)
    if email:
        update_fields.append("Email = %s")
        params.append(email)
    if password:
        update_fields.append("Password = %s")
        params.append(password)
    if date_of_birth:
        update_fields.append("DateOfBirth = %s")
        params.append(date_of_birth)
    if gender:
        update_fields.append("Gender = %s")
        params.append(gender)
    if fitness_goals:
        update_fields.append("FitnessGoals = %s")
        params.append(fitness_goals)
    if health_metrics:
        update_fields.append("HealthMetrics = %s")
        params.append(health_metrics)

    if not update_fields:
        print("No updates made.")
        return

    update_query = "UPDATE Members SET " + ", ".join(update_fields) + " WHERE MemberID = %s;"
    params.append(member_id)

    cursor = conn.cursor()
    try:
        cursor.execute(update_query, tuple(params))
        conn.commit()
        print("Profile updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()


def displayMemberDashboard(conn, member_id):
    cursor = conn.cursor()

    # Fetch member's health metrics
    cursor.execute("SELECT HealthMetrics FROM Members WHERE MemberID = %s", (member_id,))
    health_metrics = cursor.fetchone()
    if health_metrics and health_metrics[0]:
        print("\nHealth Statistics:")
        for key, value in health_metrics[0].items():
            print(f"  {key}: {value}")
    else:
        print("\nYou have NO health statistics available.")

    # Fetch member's booked classes (exercise routines)
    cursor.execute("""
    SELECT Classes.ClassName, Classes.Schedule 
    FROM Bookings
    JOIN Classes ON Bookings.ClassID = Classes.ClassID
    WHERE Bookings.MemberID = %s AND Bookings.ClassID IS NOT NULL
    ORDER BY Classes.Schedule ASC
    """, (member_id,))
    classes = cursor.fetchall()
    if classes:
        print("\nUpcoming Exercise Routines (Group Classes):")
        for class_name, schedule in classes:
            print(f"  {class_name} at {schedule}")
    else:
        print("\nYou have no upcoming group exercise routines.")

    # Fetch personal training sessions
    cursor.execute("""
    SELECT Trainers.Name, Bookings.Date, Bookings.Time
    FROM Bookings
    JOIN Trainers ON Bookings.TrainerID = Trainers.TrainerID
    WHERE Bookings.MemberID = %s AND Bookings.ClassID IS NULL
    ORDER BY Bookings.Date, Bookings.Time ASC
    """, (member_id,))
    personal_trainings = cursor.fetchall()
    if personal_trainings:
        print("\nUpcoming Personal Training Sessions:")
        for trainer_name, date, time in personal_trainings:
            print(f"  Trainer: {trainer_name}, Date: {date}, Time: {time}")
    else:
        print("\nYou have no upcoming personal training sessions.")

    # For fitness achievements, achievements are part of HealthMetrics for simplicity
    # Example: "achievements": [{"title": "5K Run", "date": "2023-01-01"}, ...]
    if health_metrics and health_metrics[0] and "achievements" in health_metrics[0]:
        print("\nFitness Achievements:")
        achievements = health_metrics[0].get('achievements', [])
        for achievement in achievements:
            print(f"  {achievement['title']} on {achievement['date']}")
    else:
        print("\nNo fitness achievements recorded.")


def schedulePersonalTraining(conn, memberId):
    print("\nAvailable Trainers and their available slots:")
    cursor = conn.cursor()
    # Fetch trainers and their available slots
    cursor.execute("""
    SELECT t.TrainerID, t.Name, a.AvailabilityID, a.AvailableFrom, a.AvailableTo 
    FROM Trainers t
    JOIN TrainerAvailability a ON t.TrainerID = a.TrainerID
    WHERE a.Status = 'Available' AND a.AvailableFrom > CURRENT_TIMESTAMP
    ORDER BY t.TrainerID, a.AvailableFrom
    """)
    availabilities = cursor.fetchall()

    if not availabilities:
        print("No trainers are currently available.")
        return

    for trainer_id, name, availability_id, available_from, available_to in availabilities:
        print(f"Trainer ID: {trainer_id}, Name: {name}, Slot ID: {availability_id}, From: {available_from}, To: {available_to}")

    availability_id = input("Select an available slot by Slot ID: ")

    # Fetch the chosen availability slot details
    cursor.execute("""
    SELECT TrainerID, AvailableFrom, AvailableTo
    FROM TrainerAvailability
    WHERE AvailabilityID = %s AND Status = 'Available'
    """, (availability_id,))
    chosen_slot = cursor.fetchone()

    if not chosen_slot:
        print("Invalid Slot ID or slot not available.")
        return

    trainer_id, available_from, available_to = chosen_slot

    # assume the session takes the whole available slot
    date = available_from.date()
    time = available_from.time()

    # Schedule the session by updating the TrainerAvailability status (or you could delete the slot to mark it as booked)
    try:
        cursor.execute("""
        UPDATE TrainerAvailability SET Status = 'Booked' WHERE AvailabilityID = %s
        """, (availability_id,))

        # Insert into Bookings table
        cursor.execute("""
        INSERT INTO Bookings (MemberID, TrainerID, ClassID, Date, Time) 
        VALUES (%s, %s, NULL, %s, %s)
        """, (memberId, trainer_id, date, time))
        conn.commit()
        print("Personal training session scheduled successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()


def joinGroupFitnessClass(conn, memberId):
    print("\nAvailable Fitness Classes:")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ClassID, ClassName, Schedule, Capacity - COALESCE((SELECT COUNT(*) FROM Bookings WHERE ClassID = Classes.ClassID GROUP BY ClassID), 0) AS AvailableSpots
        FROM Classes
        WHERE Schedule > CURRENT_TIMESTAMP
    """)
    classes = cursor.fetchall()

    if not classes:
        print("No available classes.")
        return

    for classID, name, schedule, available_spots in classes:
        print(f"{classID}: {name} at {schedule} - Spots Left: {available_spots}")

    classID = input("Select a class by ID: ")
    chosen_class = next((cls for cls in classes if str(cls[0]) == classID), None)
    if not chosen_class:
        print("Invalid class ID selected.")
        return

    date, time = chosen_class[2].date(), chosen_class[2].time()

    # Check if there are available spots
    if chosen_class[3] <= 0:
        print("Sorry, no spots left for this class.")
        return

    # Check if the member is already enrolled
    cursor.execute("SELECT * FROM Bookings WHERE MemberID = %s AND ClassID = %s", (memberId, classID))
    if cursor.fetchone():
        print("You are already enrolled in this class.")
        return

    # Enroll in the class
    try:
        cursor.execute("INSERT INTO Bookings (MemberID, ClassID, Date, Time) VALUES (%s, %s, %s, %s)", (memberId, classID, date, time))
        conn.commit()
        print("Enrolled in fitness class successfully.")
    except Exception as e:
        conn.rollback()
        print(f"An error occurred while enrolling: {e}")

def checkMemberBills(conn, member_id):
    print("\nFetching your payment...")
    cursor = conn.cursor()
    
    # Retrieve payments made by the member
    cursor.execute("""
        SELECT PaymentID, Amount, PaymentDate, Service 
        FROM Payments 
        WHERE MemberID = %s
        ORDER BY PaymentDate DESC
    """, (member_id,))

    payments = cursor.fetchall()

    if not payments:
        print("You have no payment at this moment.")
    else:
        print("\nYour pending payment(s):")
        for payment in payments:
            payment_id, amount, payment_date, service = payment
            print(f"Payment ID: {payment_id}, Amount: ${amount:.2f}, Date: {payment_date}, Service: {service}")


def showMemberMenu(conn, memberId):
    while True:
        print("\nMember Menu:")
        print("1. Profile Management")
        print("2. Schedule Training Session")
        print("3. View Dashboard")
        print("4. Check your bill")
        print("5. Logout")

        choice = input("Select an option: ")

        if choice == "1":
            update_profile(conn, memberId)
        elif choice == "2":
            while True:
                print("\nSchedule Management")
                print("1. Schedule Personal Training Session")
                print("2. Join Group Fitness Class")
                choice = input("Select an option: ")

                if choice == "1":
                    schedulePersonalTraining(conn, memberId)
                    break
                elif choice == "2":
                    joinGroupFitnessClass(conn, memberId)
                    break
                else:
                    print("Invalid option selected.")
        elif choice == "3":
            displayMemberDashboard(conn, memberId)
        elif choice == '4':
            checkMemberBills(conn, memberId)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid option. Please try again.")
