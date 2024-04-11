-- Insert a new member
INSERT INTO Members (Name, Email, Password, DateOfBirth, Gender, FitnessGoals, HealthMetrics) 
VALUES ('John Doe', 'johndoe@example.com', 'password123', '1990-01-01', 'Male', 'Improve strength', '{"weight": 70, "height": 175}');

-- Insert a new trainer
INSERT INTO Trainers (Name, Email, Password, Specialization) 
VALUES ('Alice Smith', 'alicesmith@example.com', 'password123', 'Fitness Training');

-- Insert a new admin
INSERT INTO Admin (Username, Email, Password)
VALUES ('adminUser', 'admin@example.com', 'adminPassword');

-- Insert availability
INSERT INTO TrainerAvailability (TrainerID, AvailableFrom, AvailableTo, Status) 
VALUES (1, '2024-01-01 09:00:00', '2024-01-01 12:00:00', 'Available');

-- Insert a room
INSERT INTO Rooms (RoomName, Capacity) 
VALUES ('Yoga Room', 15);

-- Insert equipment
INSERT INTO Equipment (EquipmentName, Status) 
VALUES ('Treadmill', 'Available');

-- Insert a class
INSERT INTO Classes (ClassName, RoomID, TrainerID, Schedule, Capacity) 
VALUES ('Morning Yoga', 1, 1, '2024-01-10 07:00:00', 10);

-- Insert a booking
INSERT INTO Bookings (MemberID, TrainerID, ClassID, Date, Time) 
VALUES (1, 1, 1, '2024-01-10', '07:00:00');

-- Insert a payment
INSERT INTO Payments (MemberID, Amount, PaymentDate, Service) 
VALUES (1, 100.00, '2024-01-15', 'Yoga Class');