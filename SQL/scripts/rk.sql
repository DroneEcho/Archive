CREATE TABLE IF NOT EXISTS Drivers 
(
	DriverId INT PRIMARY KEY,
    DriverLicense INT,
    FIO TEXT,
    Phone TEXT
);



CREATE TABLE IF NOT EXISTS Cars 
(
	CarId INT PRIMARY KEY,
    Model INT,
    Colour TEXT,
    Year Int,
    Regdate DATE
);



CREATE TABLE IF NOT EXISTS Fines 
(
	FineId INT PRIMARY KEY,
    FineType Text,
    Amount int,
    FineDate DATE
);


--многие ко многим
CREATE TABLE IF NOT EXISTS Drivers_and_cars
(
    Did INT REFERENCES Drivers(DriverId),
    Cid INT REFERENCES Cars(CarId)
);



--у Driver много Fines, но у fines 1 driver
CREATE TABLE IF NOT EXISTS Drivers_and_fines
(
    Did INT REFERENCES Drivers(DriverId),
    Fid INT REFERENCES Fines(FineId)
);

INSERT INTO Drivers VALUES
 (1, 123, 'Anton A.', '79161152666'),
 (2, 321, 'Pavel A.', '79163333333'),
 (3, 567, 'Lev S.', '79164356666'),
 (4, 345, 'Ronin M.', '79167465866'),
 (5, 789, 'gen A.', '79161878966'),
 (6, 456, 'fdhy B.', '79546452666'),
 (7, 324, 'Lova G.', '79161156566'),
 (8, 887, 'Geni R.', '79364768906'),
 (9, 890, 'bfsgh A.', '45475552666'),
 (10, 234, 'Beji L.', '79161156466');

INSERT INTO Cars VALUES
 (1, 1, 'Red', 2001, '01-05-2001'),
 (2, 8, 'blue', 1997, '01-01-2001'),
 (3, 4, 'Yellow', 2003,'05-05-2001'),
 (4, 23, 'Red', 1945, '12-05-2000'),
 (5, 89, 'Black', 1975, '01-12-2003'),
 (6, 257, 'Yellow', 2012, '02-04-2013'),
 (7, 987, 'White', 2013, '01-05-2014'),
 (8, 809, 'Red', 2012, '08-05-20013'),
 (9, 124, 'Yellow', 1990, '01-05-2001'),
 (10, 245, 'Black', 1989, '07-08-2012');

INSERT INTO Fines VALUES
 (1, 'Speeding', 200, '03-05-2007'),
 (2, 'red light', 100, '03-05-2007'),
 (3, 'crash', 550, '04-08-2012'),
 (4, 'belt is not on', 20, '03-05-2007'),
 (5, 'Speeding', 140, '04-08-2012'),
 (6, 'red light', 55, '09-02-2013'),
 (7, 'crash', 720, '09-02-2013'),
 (8, 'belt is not on', 20, '03-05-2007'),
 (9, 'red light', 130, '09-02-2013'),
 (10, 'Speeding', 240, '04-08-2012');
INSERT INTO Drivers_and_fines VALUES
    (1, 1),
    (1,2),
    (2, 3),
    (3, 4),
    (4, 5),
    (4, 6),
    (4, 7),
    (5, 8),
    (6, 9),
    (7, 10);

INSERT INTO Drivers_and_cars VALUES
 (1, 1),
 (1, 2),
 (2, 1),
 (3, 2),
 (4, 3),
 (4, 5),
 (5, 4),
 (5, 5),
 (6, 6),
 (7, 7),
 (8, 8),
 (9, 9),
 (10, 10),
 (10, 8);

-- вывести всех водителей у которых лицензия больше 500 
 SELECT * FROM Drivers WHERE EXISTS(SELECT Drivers.DriverLicense WHERE Drivers.DriverLicense > 500);


--вставить связь в траблицу Drivers_and_fines с (Did - max число больше 200 из Drivers и fid = 1 )
INSERT INTO Drivers_and_fines (Did, Fid) 
SELECT ( SELECT MAX(DriverId)  
 FROM Drivers 
 WHERE  DriverLicense>200), 
1;

SELECT AVG(DriverLicense), FIO
From ( Select DriverLicense, FIO FROM Drivers WHERE  DriverLicense > 100 ) as better_than_100



CREATE OR REPLACE Procedure GetIndexes(schem text, tab text)
AS '
DECLARE
    elem RECORD;
BEGIN
    FOR elem IN
        SELECT * FROM pg_indexes WHERE schemaname = schem AND tablename = tab
    LOOP
        RAISE INFO ''Elem:%'', elem;
    END LOOP;
END;
' LANGUAGE plpgsql;

call GetIndexes ('public', 'Drivers')