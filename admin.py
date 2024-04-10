import psycopg
from datetime import datetime

def showAdminMenu(conn, userId):
    while True:
        print("\nAdmin Menu:")
        print("1. Manage Room Bookings")
        print("2. Monitor Equipment Maintenance")
        print("3. Manage Class Schedules")
        print("4. Billing and Payment Processing")
        print("5. Exit Admin Menu (Logout)")
        choice = input("Choose an option: ")
        if choice == '1':
            manage_room_booking(conn)
        elif choice == '2':
            monitor_equipment_maintenance(conn)
        elif choice == '3':
            update_class_schedule(conn)
        elif choice == '4':
            process_billing_and_payments(conn)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")
        # Implement functionalities
        

def manage_room_booking(conn):
    cursor = conn.cursor()

    while True:
        print("\nRoom Booking Management")
        print("1. View all room bookings")
        print("2. Create a room booking for a class")
        print("3. Cancel an existing room booking")
        print("4. View available rooms")
        print("5. Create a new room")
        print("6. Return to main menu")
        choice = input("Choose an option: ")

        if choice == '1':
            # View all room bookings
            try:
                cursor.execute("""
                    SELECT b.BookingID, c.ClassName, r.RoomName, b.Date, b.Time
                    FROM Bookings b
                    JOIN Classes c ON b.ClassID = c.ClassID
                    JOIN Rooms r ON c.RoomID = r.RoomID
                    ORDER BY b.Date, b.Time;
                """)
                bookings = cursor.fetchall()
                print("\nAll Room Bookings:")
                for booking in bookings:
                    print(f"Booking ID: {booking[0]}, Class Name: {booking[1]}, Room: {booking[2]}, Date: {booking[3]}, Time: {booking[4]}")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()

        elif choice == '2':
            # Create a room booking for a class
            class_id = input("Enter the Class ID to book: ")
            date = input("Enter the booking date (YYYY-MM-DD): ")
            time = input("Enter the booking time (HH:MM:SS): ")

            try:
                cursor.execute("""
                    INSERT INTO Bookings (ClassID, Date, Time)
                    VALUES (%s, %s, %s)
                """, (class_id, date, time))
                conn.commit()
                print("Room booking created successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()

        elif choice == '3':
            # Cancel an existing room booking
            booking_id = input("Enter the Booking ID to cancel: ")

            try:
                cursor.execute("""
                    DELETE FROM Bookings
                    WHERE BookingID = %s;
                """, (booking_id,))
                conn.commit()
                print("Booking cancelled successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()

        elif choice == '4':
            # View available rooms
            try:
                cursor.execute("""
                    SELECT RoomID, RoomName, Capacity 
                    FROM Rooms
                    ORDER BY RoomName;
                """)
                rooms = cursor.fetchall()
                print("\nAvailable Rooms:")
                for room in rooms:
                    print(f"Room ID: {room[0]}, Name: {room[1]}, Capacity: {room[2]}")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()
                
        elif choice == '5':
            # Add a new room
            room_name = input("Enter the new room name: ")
            capacity = input("Enter the room capacity: ")

            try:
                cursor.execute("""
                    INSERT INTO Rooms (RoomName, Capacity)
                    VALUES (%s, %s)
                """, (room_name, capacity))
                conn.commit()
                print("New room added successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()

        elif choice == '6':
            print("Returning to the main menu...")
            break

        else:
            print("Invalid choice. Please try again.")

    cursor.close()


            


        
## DONE
def monitor_equipment_maintenance(conn):
    cursor = conn.cursor()
    
    while True:
        print("\nEquipment Maintenance Management")
        print("1. View equipment status")
        print("2. Update equipment status")
        print("3. Return to main menu")
        choice = input("Choose an option: ")
        
        if choice == "1":
            # SQL query to display equipment status
            try:
                query = "SELECT EquipmentID, EquipmentName, Status FROM Equipment;"
                cursor.execute(query)
                equipments = cursor.fetchall()
                print("\nCurrent Equipment Status:")
                for eq in equipments:
                    print(f"Equipment ID: {eq[0]}, Name: {eq[1]}, Status: {eq[2]}")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()

        elif choice == '2':
            # Update equipment status
            try:
                equipment_id = input("Enter the ID of the equipment to update: ")

                # Check if the equipment ID exists
                cursor.execute("SELECT COUNT(*) FROM Equipment WHERE EquipmentID = %s;", (equipment_id,))
                if cursor.fetchone()[0] == 0:
                    print(f"No equipment found with ID {equipment_id}. Please try again with a valid ID.")
                    continue

                new_status = input("Enter the new status of the equipment: ")

                query = "UPDATE Equipment SET Status = %s WHERE EquipmentID = %s;"
                cursor.execute(query, (new_status, equipment_id))
                conn.commit()
                print("Equipment status updated successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()

        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

    cursor.close()
            


## DONE
def update_class_schedule(conn):
    cursor = conn.cursor()

    while True:
        print("\nClass Schedule Management")
        print("1. View class schedules")
        print("2. Add new class schedule")
        print("3. Update class schedule")
        print("4. Delete class schedule")
        print("5. Return to main menu")
        choice = input("Choose an option: ")

        if choice == '1':
            # View class schedules
            try:
                query = "SELECT ClassID, ClassName, RoomID, TrainerID, Schedule, Capacity FROM Classes;"
                cursor.execute(query)
                classes = cursor.fetchall()
                print("\nCurrent Class Schedules:")
                for cls in classes:
                    print(f"Class ID: {cls[0]}, Name: {cls[1]}, Room ID: {cls[2]}, Trainer ID: {cls[3]}, Schedule: {cls[4]}, Capacity: {cls[5]}")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()

        elif choice == '2':
            # Add a new class schedule
            try:
                class_name = input("Enter the class name: ")
                room_id = input("Enter the room ID: ")
                
                #Fetching the capacity of the room
                cursor.execute("SELECT Capacity FROM Rooms WHERE RoomID = %s;", (room_id,))
                room_capacity_result = cursor.fetchone()
                if room_capacity_result is None:
                    print(f"No room found with ID {room_id}. Please try again with a valid ID.")
                    continue
                room_capacity = room_capacity_result[0]
                
                
                # Fetching and displaying all trainers
                print("\nFetching trainer details...")
                cursor.execute("SELECT * FROM Trainers;")
                trainers = cursor.fetchall()
                print("\nTrainer Details:")
                for trainer in trainers:
                    print(f"Trainer ID: {trainer[0]}, Name: {trainer[1]}, Email: {trainer[2]}, Specialization: {trainer[4]}")
                
                
                trainer_id = input("Enter the trainer ID: ")
                schedule = input("Enter the schedule (YYYY-MM-DD HH:MM:SS): ")
                
                #Input validation for capacity
                while True:
                    capacity = int(input("Enter the capacity: "))
                    if capacity <= room_capacity:
                        break
                    else:
                        print(f"Capacity exceeds the limit of the room (max {room_capacity}). Please enter a valid capacity.")
                        

                query = "INSERT INTO Classes (ClassName, RoomID, TrainerID, Schedule, Capacity) VALUES (%s, %s, %s, %s, %s);"
                cursor.execute(query, (class_name, room_id, trainer_id, schedule, capacity))
                conn.commit()
                print("New class schedule added successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()

        elif choice == '3':
            # Update an existing class schedule
            try:
                class_id = input("Enter the Class ID to update: ")
                # You need to add inputs and logic to update specific class attributes.
                # Example: updating the class schedule.
                new_schedule = input("Enter the new schedule (YYYY-MM-DD HH:MM:SS): ")
                update_query = "UPDATE Classes SET Schedule = %s WHERE ClassID = %s;"
                cursor.execute(update_query, (new_schedule, class_id))
                conn.commit()
                print("Class schedule updated successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()

        elif choice == '4':
            # Delete a class schedule
            try:
                class_id = input("Enter the Class ID to delete: ")
                delete_query = "DELETE FROM Classes WHERE ClassID = %s;"
                cursor.execute(delete_query, (class_id,))
                conn.commit()
                print("Class schedule deleted successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()

        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

    cursor.close()




##DONE
def process_billing_and_payments(conn):
    cursor = conn.cursor()

    while True:
        print("\nBilling and Payment Processing")
        print("1. View all payments")
        print("2. Record a new payment")
        print("3. Delete a payment record")
        print("4. Return to main menu")
        choice = input("Choose an option: ")

        if choice == '1':
            # Display all payment records
            try:
                query = "SELECT PaymentID, MemberID, Amount, PaymentDate, Service FROM Payments;"
                cursor.execute(query)
                payments = cursor.fetchall()
                print("\nPayment Records:")
                for payment in payments:
                    print(f"Payment ID: {payment[0]}, Member ID: {payment[1]}, Amount: {payment[2]}, Date: {payment[3]}, Service: {payment[4]}")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()

        elif choice == '2':
            # Record a new payment
            try:
                # Display all member details
                print("\nFetching member details...")
                cursor.execute("SELECT * FROM Members;")
                members = cursor.fetchall()
                print("\nMember Details:")
                for member in members:
                    print(f"Member ID: {member[0]}, Name: {member[1]}, Email: {member[2]}, Date of Birth: {member[4]}, Gender: {member[5]}, Fitness Goals: {member[6]}, Health Metrics: {member[7]}")
                    
                    
                member_id = input("Enter the Member ID: ")
                # Ensure the amount is numeric
                while True:
                    amount_input = input("Enter the amount (numeric only, no symbols): ")
                    try:
                        amount = float(amount_input)  # Convert to a float
                        break  # Exit the loop if conversion is successful
                    except ValueError:
                        print("Invalid amount. Please enter a numeric value.")
                
                
                payment_date = input("Enter the payment date (YYYY-MM-DD): ")
                service = input("Enter the service for which payment is made: ")

                # Insert new payment
                insert_query = "INSERT INTO Payments (MemberID, Amount, PaymentDate, Service) VALUES (%s, %s, %s, %s);"
                cursor.execute(insert_query, (member_id, amount, payment_date, service))
                conn.commit()
                print("New payment recorded successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()
                
        elif choice == '3':
        # Delete a payment record
            try:
                payment_id = input("Enter the Payment ID to delete: ")
                # Check if the payment ID exists
                cursor.execute("SELECT COUNT(*) FROM Payments WHERE PaymentID = %s;", (payment_id,))
                if cursor.fetchone()[0] == 0:
                    print(f"No payment found with ID {payment_id}. Please try again with a valid ID.")
                    continue

                delete_query = "DELETE FROM Payments WHERE PaymentID = %s;"
                cursor.execute(delete_query, (payment_id,))
                conn.commit()
                print("Payment record deleted successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()

        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

    cursor.close()


