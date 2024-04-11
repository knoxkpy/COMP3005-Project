-- Create Members table
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

-- Create Trainers table
CREATE TABLE IF NOT EXISTS Trainers (
    TrainerID SERIAL PRIMARY KEY,
    Name VARCHAR(255) UNIQUE NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Specialization VARCHAR(255)
);

-- Create Admin table
CREATE TABLE IF NOT EXISTS Admin (
    AdminID SERIAL PRIMARY KEY,
    Username VARCHAR(255) UNIQUE NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL
);

-- Create TrainerAvailability table
CREATE TABLE IF NOT EXISTS TrainerAvailability (
    AvailabilityID SERIAL PRIMARY KEY,
    TrainerID INT REFERENCES Trainers(TrainerID),
    AvailableFrom TIMESTAMP NOT NULL,
    AvailableTo TIMESTAMP NOT NULL,
    Status VARCHAR(50) DEFAULT 'Available' NOT NULL
);

-- Create Rooms table
CREATE TABLE IF NOT EXISTS Rooms (
    RoomID SERIAL PRIMARY KEY,
    RoomName VARCHAR(255) NOT NULL,
    Capacity INT
);

-- Create Equipment table
CREATE TABLE IF NOT EXISTS Equipment (
    EquipmentID SERIAL PRIMARY KEY,
    EquipmentName VARCHAR(255) NOT NULL,
    Status VARCHAR(50) NOT NULL
);

-- Create Classes table
CREATE TABLE IF NOT EXISTS Classes (
    ClassID SERIAL PRIMARY KEY,
    ClassName VARCHAR(255) NOT NULL,
    RoomID INT REFERENCES Rooms(RoomID),
    TrainerID INT REFERENCES Trainers(TrainerID),
    Schedule TIMESTAMP NOT NULL,
    Capacity INT
);

-- Create Bookings table
CREATE TABLE IF NOT EXISTS Bookings (
    BookingID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    TrainerID INT REFERENCES Trainers(TrainerID),
    ClassID INT REFERENCES Classes(ClassID),
    Date DATE NOT NULL,
    Time TIME NOT NULL
);

-- Create Payments table
CREATE TABLE IF NOT EXISTS Payments (
    PaymentID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    Amount DECIMAL(10, 2) NOT NULL,
    PaymentDate DATE NOT NULL,
    Service VARCHAR(255) NOT NULL
);
