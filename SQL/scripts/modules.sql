DROP FUNCTION  IF EXISTS Calculate_age;

CREATE FUNCTION  Calculate_age(DOB DATE)
RETURNS int
AS $$
BEGIN
    RETURN DATE_PART('year', CURRENT_DATE) - DATE_PART('year', DOB);
END;
$$ LANGUAGE plpgsql;


SELECT Title, Calculate_age(Year)
FROM Art;

---------------------

DROP FUNCTION IF EXISTS GetAllArtFromMuseum;

CREATE FUNCTION GetAllArtFromMuseum(Id INT) 
RETURNS TABLE(MuseumId INT,
	            ArtId INT,
	            StartDate DATE,
	            EndDate DATE,
	            Hall INT,
                Title TEXT
                ) AS $$
BEGIN 
    RETURN QUERY (
        SELECT Museum_Storage_History.*, t1.Title from Museum_Storage_History 
        LEFT JOIN (SELECT * FROM Museum GROUP by Museum.Id) as t
            on Museum_Storage_History.MuseumId = t.id
            LEFT JOIN (SELECT Art.Id, Art.Title, Art.Year, Art.Art_type FROM Art GROUP by Art.Id) as t1
            on Museum_Storage_History.ArtId = t1.id
    );
END;
$$ LANGUAGE plpgsql;

SELECT *
FROM GetAllArtFromMuseum(0);

----------------------------

DROP FUNCTION IF EXISTS GetSearchedArts;

CREATE FUNCTION GetSearchedArts(_museumIds int ARRAY) 
RETURNS SETOF Art AS $$
DECLARE 
    rec Art;
    flag BOOLEAN;
    i INT;
BEGIN
    FOR rec IN (SELECT * FROM Art WHERE Art_type = 'Book') LOOP
        flag := TRUE;

        FOR i IN 0..array_length(_museumIds, 1) LOOP
            IF rec.Id NOT IN (SELECT ArtId FROM GetAllArtFromMuseum(_museumIds[i])) THEN
                flag := FALSE;
            END IF;
        END LOOP;

        IF flag THEN
            RETURN NEXT rec;
        END IF;
    END LOOP; 
    RETURN;
END;
$$ LANGUAGE plpgsql;


SELECT *
FROM GetSearchedArts(ARRAY[0]);
------------------------------

DROP FUNCTION IF EXISTS ContactAuthor;

CREATE FUNCTION ContactAuthor(AuthorId INT) 
RETURNS TABLE(ArtId INT) AS $$
BEGIN
    RETURN QUERY EXECUTE '
        WITH RECURSIVE cte(ContactAuthor) AS (
            SELECT Id AS ContactAuthor
            FROM Art
            WHERE Id IN (SELECT AuthorId 
                                FROM Author_and_art 
                                WHERE PaintingId = $1)

            UNION

            SELECT * 
            FROM (
                WITH cte_inner AS (
                    SELECT * FROM cte
                )
                SELECT PaintingId
                FROM Author_and_art
                WHERE AuthorId IN (SELECT AuthorId
                                    FROM Author JOIN cte_inner ON ContactAuthor=PaintingId)
            ) t
        )
        SELECT * FROM cte;
    ' USING AuthorId;
END;
$$ LANGUAGE plpgsql;



SELECT *
FROM ContactAuthor(6);

-----------------

DROP PROCEDURE IF EXISTS ChangePrice;

CREATE PROCEDURE ChangePrice(diff INT) AS $$
BEGIN 
    UPDATE Art 
    SET Price = Price + diff;
END;
$$ LANGUAGE plpgsql;



SELECT * 
FROM Art
LIMIT 10;

CALL ChangePrice(-10);

SELECT * 
FROM Art
LIMIT 10;

----------------- 

DROP PROCEDURE IF EXISTS ContactAuthors;

CREATE PROCEDURE ContactAuthors(directorId INT) AS $$
     WITH RECURSIVE cte(ContactAuthor) AS (
            SELECT Id AS ContactAuthor
            FROM Art
            WHERE Id IN (SELECT AuthorId 
                                FROM Author_and_art 
                                WHERE PaintingId = $1)

            UNION

            SELECT * 
            FROM (
                WITH cte_inner AS (
                    SELECT * FROM cte
                )
                SELECT PaintingId
                FROM Author_and_art
                WHERE AuthorId IN (SELECT AuthorId
                                    FROM Author JOIN cte_inner ON ContactAuthor=PaintingId)
            ) t
    )
    SELECT * 
    INTO TEMP TABLE ContactAuthors
    FROM cte;
$$ LANGUAGE SQL;



CALL ContactAuthors(0);

SELECT * 
FROM ContactAuthors;

-----------------

DROP PROCEDURE IF EXISTS DateDiff;

CREATE PROCEDURE DateDiff(ArtId1 INT, ArtId2 INT, INOUT res INT) AS $$
DECLARE 
    curs CURSOR (id1 INT, id2 INT) FOR SELECT date_part('year', Year) 
                                FROM Art
                                WHERE Id=id1 OR Id=id2;
    Year1 INT;
    Year2 INT;
BEGIN
    OPEN curs(ArtId1, ArtId2);
    FETCH curs INTO Year1;
    FETCH curs INTO Year2;
    CLOSE curs;
    res := ABS(Year1 - Year2);
END;
$$ LANGUAGE plpgsql;


DO $$
DECLARE 
    res INT;
BEGIN
    CALL DateDiff(0, 1, res);
    RAISE info '% years difference', res;
END;
$$

-----------------
CREATE EXTENSION IF NOT EXISTS dblink;
DROP PROCEDURE IF EXISTS GetIndexInfo;

CREATE PROCEDURE GetIndexInfo(dbname text, tname text, INOUT res refcursor) AS $$
DECLARE
    rec RECORD;
BEGIN
    OPEN res FOR
    SELECT *
    FROM dblink(format('dbname=%s user=postgres', dbname), 
                format('
                SELECT *  
                FROM pg_indexes
                WHERE tablename=''%s''
                ', tname))
    AS T(schemaname NAME, tablename NAME, indexname NAME, tablespace NAME, indexdef TEXT);
	
    LOOP
        FETCH res INTO rec;
        IF NOT FOUND THEN
		EXIT; END IF;

        raise notice '%', rec;
    END LOOP;
    
END;
$$ LANGUAGE plpgsql;


BEGIN;
    CALL GetIndexInfo('art_station', 'art', 'result');
    FETCH all IN "result";
    CLOSE "result";
COMMIT;

-----------------

CREATE OR REPLACE FUNCTION RemoveEmpty() 
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.Title='' OR NEW.Title=NULL OR NEW.Title IN (SELECT Title 
                                                        FROM Art)
    THEN
        DELETE FROM Art
        WHERE Id=NEW.Id;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER check_insert
    BEFORE INSERT ON Art
    FOR EACH ROW
    EXECUTE FUNCTION RemoveEmpty();

INSERT INTO Art (Title, Year, Price, Current_place, Art_type) 
VALUES ('Awoo', '01-01-2023', 200, 'Luvr', 'Book')

------------------------------

CREATE VIEW ArtView AS SELECT * FROM Art;

CREATE OR REPLACE FUNCTION DeleteCascade() 
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.Id IN (SELECT Id 
                    FROM Art)
    THEN
        DELETE FROM Author_and_art
        WHERE PaintingId = OLD.Id;

        DELETE FROM Owner_and_art
        WHERE PaintingId = OLD.Id;
        
        DELETE FROM Museum_Storage_History
        WHERE ArtId = OLD.Id;

        DELETE FROM Vandalism_Case
        WHERE ArtId = OLD.Id;

        DELETE FROM Expertise
        WHERE ArtId = OLD.Id;
    END IF;
    raise notice 'cascade delete trigger';
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER check_delete
    INSTEAD OF DELETE ON ArtView
    FOR EACH ROW
    EXECUTE FUNCTION DeleteCascade();


DELETE from artview * WHERE Id = 0


----------------------

--выведет инф о тех авторах у кот разница между работами не больше года

--temp table author Aid art aId year

DROP FUNCTION IF EXISTS CloseAuthors;

--CREATE TYPE temp_type AS (PaintingId INT, Title TEXT, Year DATE, AuthorId INT, FullName TEXT);
CREATE FUNCTION CloseAuthors() 
RETURNS SETOF temp_type AS $$
DECLARE
    rec temp_type;
    rec2 temp_type;
    res INT;
    flag BOOLEAN;
BEGIN
	CREATE TEMP TABLE IF NOT EXISTS temp_table AS
			SELECT t.Id as PaintingId, t.Title, t.Year, t2.Id as AuthorId, t2.FullName FROM Author_and_art
			LEFT JOIN (SELECT Id, Title, Year FROM Art) as t
			on Author_and_art.PaintingId = t.Id
			LEFT JOIN (SELECT Id, FullName FROM Author) as t2
			on Author_and_art.AuthorId = t2.Id;
    FOR rec IN (SELECT * FROM temp_table) LOOP
        flag := False;

        FOR rec2 IN (SELECT * FROM temp_table) LOOP
            
            if rec.AuthorId != rec2.AuthorId THEN
                CALL DateDiff(rec.PaintingId, rec2.PaintingId, res);
                IF  res = 0  THEN
                    flag := TRUE;
                    RETURN NEXT rec2;
					DELETE FROM temp_table WHERE rec2.PaintingId = PaintingId;
                END IF;
            END IF;
        END LOOP;

        IF flag THEN
            RETURN NEXT rec;
			
        END IF;
		DELETE FROM temp_table WHERE rec.PaintingId = PaintingId;
    END LOOP;
	DROP TABLE IF EXISTS temp_table CASCADE;
    RETURN;
END;
$$ LANGUAGE plpgsql;



SELECT *
FROM CloseAuthors();