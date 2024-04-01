import psycopg
import json

def update_profile(conn, member_id):
    print("\nProfile Management")
    print("Leave it blank if you do not wish to change a field.")

    name = input("Enter your new name: ")
    email = input("Enter your new email: ")
    password = input("Enter your new password: ")
    date_of_birth = input("Enter your new date of birth (YYYY-MM-DD): ")
    gender = input("Enter your new gender: ")
    fitness_goals = input("Enter your new fitness goals: ")
    health_metrics = input("Enter your new health metrics (as JSON string, e.g., '{\"weight\": 70, \"height\": 175}'): ")

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
    WHERE Bookings.MemberID = %s
    ORDER BY Classes.Schedule ASC
    """, (member_id,))
    classes = cursor.fetchall()
    if classes:
        print("\nUpcoming Exercise Routines:")
        for class_name, schedule in classes:
            print(f"  {class_name} at {schedule}")
    else:
        print("\nYou have No upcoming exercise routines.")

    # For fitness achievements, achievements are part of HealthMetrics for simplicity
    # Example: "achievements": [{"title": "5K Run", "date": "2023-01-01"}, ...]
    if health_metrics and health_metrics[0] and "achievements" in health_metrics[0]:
        print("\nFitness Achievements:")
        for achievement in health_metrics[0]["achievements"]:
            print(f"  {achievement['title']} on {achievement['date']}")
    else:
        print("\nNo fitness achievements recorded.")


def showMemberMenu(conn, memberId):
    while True:
        print("\nMember Menu:")
        print("1. Profile Management")
        print("2. Schedule Training Session")
        print("3. View Dashboard")
        print("4. Logout")

        choice = input("Select an option: ")

        if choice == "1":
            update_profile(conn, memberId)
        elif choice == "2":
            # Implement schedule training session functionality
            pass
        elif choice == "3":
            displayMemberDashboard(conn, memberId)
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid option. Please try again.")
