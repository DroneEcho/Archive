DROP FUNCTION  IF EXISTS Calculate_age;

CREATE FUNCTION  Calculate_age(DOB DATE)
RETURNS int
AS $$
    from datetime import date
    RETURN date.today().year - int(DOB.split("-")[0])
$$ LANGUAGE plpython3u;


SELECT Title, Calculate_age(Year)
FROM Art;

----------------------------------------------------

CREATE OR REPLACE FUNCTION  avg_price_of_museum(Cur_place TEXT)
RETURNS int
AS $$
    rq = plpy.execute("SELECT * FROM ART")
    price_full = 0
    price_count = 0
    for Art in rq:
        if Art["Current_place"] = Cur_place:
            price_count += 1
            price_full += Art["Price"]
    if price_count == 0:
        RETURN 'None'
    RETURN price_full / price_count
$$ LANGUAGE plpython3u;


SELECT Title, Calculate_age(Year)
FROM Art;


----------------------------------------------


CREATE OR REPLACE FUNCTION GetAllArtFromMuseum(Id INT) 
RETURNS TABLE(MuseumId INT,
	            ArtId INT,
	            StartDate DATE,
	            EndDate DATE,
	            Hall INT,
                Title TEXT
                ) AS $$
    
    rq = plpy.execute(f"\ {Id}
    SELECT Museum_Storage_History.*, t1.Title from Museum_Storage_History \
        LEFT JOIN (SELECT * FROM Museum GROUP by Museum.Id) as t \
            on Museum_Storage_History.MuseumId = t.id \
            LEFT JOIN (SELECT Art.Id, Art.Title, Art.Year, Art.Art_type FROM Art GROUP by Art.Id) as t1 \
            on Museum_Storage_History.ArtId = t1.id")
    return rq
$$ LANGUAGE plpython3u;

SELECT *
FROM GetAllArtFromMuseum(0);



---------------------------------------------


DROP PROCEDURE IF EXISTS ChangePrice;

CREATE PROCEDURE ChangePrice(diff INT) AS $$
    plpy.execute(f"UPDATE Art \ 
    SET Price = Price + {diff}")
$$ LANGUAGE plpython3u;



SELECT * 
FROM Art
LIMIT 10;

CALL ChangePrice(-10);

SELECT * 
FROM Art
LIMIT 10;

------------------------------------------------

CREATE OR REPLACE FUNCTION RemoveEmpty() 
RETURNS TRIGGER AS $$
BEGIN
    IF TD["new"]["Title"]='' OR TD["new"]["Title"] OR TD["new"]["Title"] IN plpy.execute("SELECT Title FROM Art"):
        DELETE FROM Art
        WHERE Id=NEW.Id;
    RETURN NULL;
END;
$$ LANGUAGE plpython3u;

CREATE OR REPLACE TRIGGER check_insert
    BEFORE INSERT ON Art
    FOR EACH ROW
    EXECUTE FUNCTION RemoveEmpty();

INSERT INTO Art (Title, Year, Price, Current_place, Art_type) 
VALUES ('Awoo', '01-01-2023', 200, 'Luvr', 'Book')
