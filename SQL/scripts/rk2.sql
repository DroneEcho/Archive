
CREATE TABLE IF NOT EXISTS Worker
{
    Id INT PRIMARY KEY,
    IdO INT REFERENCES Otdel(Id),
    W_Status TEXT,
    FIO TEXT,
    Pay INT 
};

CREATE TABLE IF NOT EXISTS Otdel
{
    Id INT PRIMARY KEY,
    OName TEXT,
    Phone TEXT,
    Main_W int REFERENCES Worker(Id)
};

CREATE TABLE IF NOT EXISTS Medicament
{
    Id INT PRIMARY KEY,
    MName TEXT,
    Instruct TEXT,
    Pay INT
};

CREATE TABLE IF NOT EXISTS Medicament_and_worker
{
    IdM INT REFERENCES Medicament(Id),
    IdW INT REFERENCES Worker(Id)
};

INSERT INTO Worker VALUES
(1, 'Anton', 2001, 2, '79161152666'),
;

--имя сотрудников и людей в их отделе (отдел 3)
Select FIO,COUNT(IdO) FROM Worker
GROUP by IdO
HAVING (Worker.IdO == 3)

