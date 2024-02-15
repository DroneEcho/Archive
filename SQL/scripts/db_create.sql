DROP TABLE IF EXISTS Art, Author, Art_owner,
Museum, Museum_Storage_History, Vandalism_Case, 
Author_and_art, Owner_and_art, Expertise;

CREATE TABLE Art (
    Id INT PRIMARY KEY,
    Title TEXT NOT NULL, 
    Year DATE, 
    Price INT CHECK (Price > 0),
	Current_place TEXT,
	Art_type TEXT
);

CREATE TABLE Author (
    Id INT PRIMARY KEY,
    FullName TEXT NOT NULL,
    Birthday DATE,
    Country TEXT  NOT NULL
);

CREATE TABLE Author_and_art (
    AuthorId INT REFERENCES Author(Id),
	PaintingId INT REFERENCES Art(Id)
);

CREATE TABLE Art_owner (
    Id INT PRIMARY KEY,
    FullName TEXT NOT NULL,
	PricePaid INT CHECK (PricePaid > 0),
	PurchaceDate DATE
);

CREATE TABLE Owner_and_art (
    OwnerId INT REFERENCES Art_owner(Id),
	PaintingId INT REFERENCES Art(Id)
);

CREATE TABLE Museum (
    Id INT PRIMARY KEY,
	Address TEXT NOT NULL
);

CREATE TABLE Museum_Storage_History (
    MuseumId INT REFERENCES Museum(Id),
	ArtId INT REFERENCES Art(Id),
	StartDate DATE,
	EndDate DATE,
	Hall INT
);


CREATE TABLE Vandalism_Case (
    Museum INT REFERENCES Museum(Id),
	ArtId INT  REFERENCES Art(Id),
	AcidentDate DATE,
	DamageType TEXT,
	FullName TEXT NOT NULL
);

CREATE TABLE Expertise (
    ArtId INT REFERENCES Art(Id),
    Date_check DATE,
    Validation_p TEXT
);