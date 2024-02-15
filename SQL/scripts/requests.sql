-- Запросы
--1. Инструкция SELECT, использующая предикат сравнения.
SELECT *
FROM Art
WHERE price > 200000;

--2. Инструкция SELECT, использующая предикат BETWEEN
SELECT art.title, art.Year
FROM Art
WHERE Year BETWEEN '1960-01-01' AND '1961-01-01';

--3. Инструкция SELECT, использующая предикат LIKE. 
SELECT *
FROM Vandalism_Case
WHERE DamageType LIKE 'arson';

--4. Инструкция SELECT, использующая предикат IN с вложенным подзапросом
SELECT *
FROM Author_and_art
Where PaintingId IN (SELECT Id FROM Art WHERE Art_type = 'Book')

--5. Инструкция SELECT, использующая предикат EXISTS с вложенным подзапросом. 
SELECT FullName, DamageType
FROM Vandalism_Case
WHERE EXISTS (SELECT ArtId FROM Vandalism_Case LEFT OUTER JOIN art
    ON art.Id = Vandalism_Case.ArtId 
    WHERE art.Art_type = 'Book')

--6. Инструкция SELECT, использующая предикат сравнения с квантором.
SELECT Art.Id, Art.Title, Art.Price 
FROM Art 
WHERE Art.Price > ALL ( SELECT Art.Price  FROM Art WHERE Id = 25 )

--7. Инструкция SELECT, использующая агрегатные функции в выражениях столбцов.
SELECT AVG(Transportations), SpecialArt
From (SELECT Id,
    Select Title FROM Art WHERE Type =  as SpecialArt  
    FROM Museum
    GROUP BY Id
    ) AS TotalBooks    

--8. Инструкция SELECT, использующая скалярные подзапросы в выражениях
--столбцов.
SELECT * from Vandalism_Case WHERE ArtId = ( SELECT Art.Id from Art WHERE Art.ID = 25)


--9. Инструкция SELECT, использующая простое выражение CASE. 
SELECT  MuseumId, ArtId, StartDate, Hall,
    CASE Hall
    WHEN 2 Then 'Hall 2'
    WHEN 17 Then 'Hall 3'
    When 12 Then 'Hall 1'
    Else 'return to storage'
    END AS Transportation
From Museum_Storage_History

--10. Инструкция SELECT, использующая поисковое выражение CASE.
SELECT MuseumId, ArtId, StartDate, Hall,
    CASE
    WHEN Hall > 10 AND Hall < 15 Then 'Hall 2'
    Else 'return to storage'
    END AS Transportation
From Museum_Storage_History

--11. Создание новой временной локальной таблицы из результирующего набора
--данных инструкции SELECT. 
SELECT FullName,
    Birthday,
    Country INTO TEMPORARY Darryltown_Authors 
    FROM Author
    WHERE Country = 'Darryltown' 

--12. Инструкция SELECT, использующая вложенные коррелированные
--подзапросы в качестве производных таблиц в предложении FROM. 
SELECT *
    FROM Art LEFT JOIN (SELECT FullName FROM Author
    GROUP by Id)

SELECT 'By units' AS Criteria, ProductName as 'Best Selling' 
FROM Products P JOIN ( SELECT TOP 1 ProductID, SUM(Quantity) AS SQ 
 FROM [Order Details] 
 GROUP BY productID 
 ORDER BY SQ DESC ) AS OD ON OD.ProductID = P.ProductID 
UNION 
SELECT 'By revenue' AS Criteria, ProductName as 'Best Selling' 
FROM Products P JOIN ( SELECT TOP 1 ProductID, 
 SUM(UnitPrice*Quantity*(1-Discount)) AS SR 
 FROM [Order Details] 
 GROUP BY ProductID 
 ORDER BY SR DESC) AS OD ON OD.ProductID = P.ProductID 
--13. Инструкция SELECT, использующая вложенные подзапросы с уровнем
--вложенности 3. 
 Select *
 From Art
 WHERE Price = ( Select PricePaid from Art_owner 
 HAVING Id = (Select OwnerId 
 FROM Owner_And_Art 
 HAVING PaintingId > 500) ) 
--14. Инструкция SELECT, консолидирующая данные с помощью предложения
--GROUP BY, но без предложения HAVING. 
-- Для каждого заказанного продукта категории 1 получить его цену, среднюю цену, 
--минимальную цену и название продукта
SELECT P.ProductID, P.UnitPrice, P.ProductName 
 AVG(OD.UnitPrice) AS AvgPrice, 
 MIN(OD.UnitPrice) AS MinPrice, 
FROM Products P LEFT OUTER JOIN [Order Details] OD ON OD.ProductID = P.ProductID 
WHERE CategoryID = 1 
GROUP BY P.productID, P.UnitPrice, P.ProductName 
--15. Инструкция SELECT, консолидирующая данные с помощью предложения
--GROUP BY и предложения HAVING. 
-- Получить список категорий продуктов, средняя цена которых больше общей средней цены
--продуктов
SELECT CategoryID, AVG(UnitPrice) AS 'Average Price' 
FROM Products P 
GROUP BY CategoryID 
HAVING AVG(UnitPrice) > ( SELECT AVG(UnitPrice) AS MPrice 
 FROM Products) 


--16. Однострочная инструкция INSERT, выполняющая вставку в таблицу одной
--строки значений. 
INSERT INTO Vandalism_Case (Museum, ArtId, AcidentDate, DamageType, FullName) 
VALUES ('Pushkinsky', 1, '01-01-2001', 'arson', 'Alice Turner') 
--17. Многострочная инструкция INSERT, выполняющая вставку в таблицу
--результирующего набора данных вложенного подзапроса. 
INSERT INTO Vandalism_Case (Museum, ArtId, AcidentDate, DamageType, FullName) 
SELECT ( SELECT MAX(Id) 
 FROM Art 
 WHERE CustomerID = 'ALFKI' ), 
 ProductID, UnitPrice, 10, 0.1 
FROM Products 
WHERE ProductName = 'Tofu'




--18. Простая инструкция UPDATE. 
UPDATE Art 
SET Title = 'Im new!'
WHERE ProductID = 2 
--19. Инструкция UPDATE со скалярным подзапросом в предложении SET. 
UPDATE Art 
SET Price = ( SELECT AVG(Price) 
 FROM Art 
 WHERE ProductID = 37 ) 
WHERE ProductID = 37 
--20. Простая инструкция DELETE. 
DELETE Art
WHERE Current_place IS NULL 

--21. Инструкция DELETE с вложенным коррелированным подзапросом в
--предложении WHERE. 
-- Пример для базы данных AdventureWorks 
DELETE FROM Art
WHERE EXISTS ( Select Art.Price WHERE Art.Price < 100);

--22. Инструкция SELECT, использующая простое обобщенное табличное
--выражение
-- Пример для базы данных SPJ 
WITH Treas(Musid, Coun) AS (
    SELECT MuseumId, COUNT(*) As Total
	FROM Museum_Storage_History
    GROUP BY MuseumId
)
SELECT * FROM Treas;

--23. Инструкция SELECT, использующая рекурсивное обобщенное табличное
--выражение.
-- Создание таблицы. 
CREATE TABLE dbo.Proves ( 
 Id int NOT NULL, 
 paintingId int NULL, 
 LastName nvarchar(40) NOT NULL,
 Proof nvarchar(30) NOT NULL, 
); 
-- Заполнение таблицы значениями. 
INSERT INTO dbo.Proves 
VALUES (1, 23 , N'Ghotic', N'') ;
-- Определение ОТВ
WITH DirectReports (ManagerID, EmployeeID, Title, DeptID, Level) AS 
( 
 -- Определение закрепленного элемента
 SELECT e.ManagerID, e.EmployeeID, e.Title, e.DeptID, 0 AS Level 
 FROM dbo.MyEmployees AS e 
 WHERE ManagerID IS NULL 
 UNION ALL 
 -- Определение рекурсивного элемента
 SELECT e.ManagerID, e.EmployeeID, e.Title, e.DeptID, Level + 1 
 FROM dbo.MyEmployees AS e INNER JOIN DirectReports AS d 
 ON e.ManagerID = d.EmployeeID 
) 
-- Инструкция, использующая ОТВ
SELECT ManagerID, EmployeeID, Title, DeptID, Level 
FROM DirectReports; 


--24. Оконные функции. Использование конструкций MIN/MAX/AVG OVER() 
-- Для каждой заданной группы продукта вывести среднее значение цены
Select *,
    MAX(Price) OVER (PARTITION BY Current_place) as ml
    From Art;

--25. Оконные фнкции для устранения дублей
--Придумать запрос, в результате которого в данных появляются полные дубли. 
--Устранить дублирующиеся строки с использованием функции ROW_NUMBER()

Select Current_place,
    MAX(Price) OVER (PARTITION BY Current_place) as ml,
    ROW_NUMBER() OVER (PARTITION BY Current_place)
    From Art

WHERE Art.Id IN ( Select Id
                FROM (Select Id,
                        ROW_NUMBER() OVER w as rnum
                        From Art 
                        WINDOW w As (
                            PARTITION BY Current_place 
                            ORDER BY Id
                        )) t
                        Where t.rnum = 1);