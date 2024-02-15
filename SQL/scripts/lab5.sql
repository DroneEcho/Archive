
-- 1. Из таблиц базы данных, созданной в первой
-- лабораторной работе, извлечь данные в JSON.
-- Функция row_to_json - Возвращает кортеж в виде объекта JSON.
SELECT row_to_json(art_j) result FROM art art_j;


-- 2. Выполнить загрузку и сохранение JSON файла в таблицу.
-- Созданная таблица после всех манипуляций должна соответствовать таблице
-- базы данных, созданной в первой лабораторной работе.

CREATE TABLE IF NOT EXISTS Art_copy (
    Id INT PRIMARY KEY,
    Title TEXT NOT NULL, 
    Year DATE, 
    Price INT CHECK (Price > 0),
	Current_place TEXT,
	Art_type TEXT
);
CREATE TABLE IF NOT EXISTS Art_json (
    data_j JSON
);
-- Копируем данные из таблицы users в файл users.json
-- (В начале нужно поставить \COPY).
copy Art_json FROM 'C:/Users/Public/art.json';

SELECT * FROM Art_json;


-- Данный запрос преобразует данные из строки в формате json
-- В табличное предстваление. Т.е. разворачивает объект из json в табличную строку.
SELECT * FROM Art_json, json_populate_record(null::Art_copy, data_j);

SELECT * FROM Art_json, json_populate_record(CAST(null AS Art_copy ), data_j);



INSERT INTO Art_copy
SELECT id, Title, Year, Price, Current_place, Art_type
FROM Art_json, json_populate_record(null::Art_copy, data_j);

SELECT * FROM Art_copy;


--Создать таблицу, в которой будет атрибут(-ы) с типом JSON, или
--добавить атрибут с типом JSON к уже существующей таблице. 
--Заполнить атрибут правдоподобными данными с помощью команд INSERT 
--или UPDATE.

-- Вставляем в Art_json json строку.
-- json_object - формирует объект JSON.
INSERT INTO Art_json
SELECT * FROM json_object('{id, title, year, price, current_place, art_type}', '{1001, "i am new json entry", "1973-05-24", 22, "Museum of Modern Art","Picture"}');
--{"id":0,"title":"Yes natural.","year":"1973-05-24","price":288523,"current_place":"Museum of Modern Art","art_type":"Picture"}


-- 4. Выполнить следующие действия:
-- 1. Извлечь XML/JSON фрагмент из XML/JSON документа
CREATE TABLE IF NOT EXISTS json_art_id_name
(
    id INT,
    Title TEXT
);

SELECT * FROM Art_json, json_populate_record(null::json_art_id_name, data_j);

-- Получаем id и имена всех искусств
-- У кроторых Title начинается с буквы 'A'
SELECT id, Title
FROM Art_json, json_populate_record(null::json_art_id_name, data_j)
WHERE Title LIKE 'A%';

-- Оператор -> возвращает поле объекта JSON как JSON.
-- -> - выдаёт поле объекта JSON по ключу.
SELECT * FROM Art_json;

SELECT data_j->'id' AS id, data_j->'title' AS Title
FROM Art_json;



-- 2. Извлечь значения конкретных узлов или атрибутов XML/JSON документа
CREATE TABLE inventory(doc jsonb);
DROP TABLE inventory;
-- Тип исскуства: Graphics Picture
INSERT INTO inventory VALUES ('{"id":0, "art_type": {"primary":"Graphics", "secondary":"Picture"}}');
INSERT INTO inventory VALUES ('{"id":1, "art_type": {"primary":"Statue", "secondary":"Painting"}}');

SELECT * FROM inventory;

-- Извлекаем тип у пользователей.
SELECT doc->'id' AS id, doc->'art_type'->'primary' AS primary_art
FROM inventory;

-- 3. Выполнить проверку существования узла или атрибута
-- Проверка вхождения — важная особенность типа jsonb, не имеющая аналога для типа json.
-- Эта проверка определяет, входит ли один документ jsonb в другой.
-- В данном примере проверятся существование инвенторя у пользователя с id=u_id.
CREATE OR REPLACE FUNCTION check_inventory(u_id jsonb)
RETURNS VARCHAR AS '
    SELECT CASE
               WHEN count.cnt > 0
                   THEN ''true''
               ELSE ''false''
               END AS comment
    FROM (
             SELECT COUNT(doc -> ''id'') cnt
             FROM inventory
             WHERE doc -> ''id'' @> u_id
         ) AS count;
' LANGUAGE sql;

SELECT * FROM inventory;

SELECT check_inventory('1');

-- 4. Изменить JSON документ

INSERT INTO inventory VALUES ('{"id":3, "art_type": {"primary":"ancient paint", "secondary":"none"}}');

SELECT * FROM inventory;
-- Особенность конкатенации json заключается в перезаписывании.
SELECT doc || '{"id": 5}'::jsonb
FROM inventory;

-- Перезаписываем значение json поля.
UPDATE inventory
SET doc = doc || '{"id": 5}'::jsonb
WHERE (doc->'id')::INT = 3;

SELECT * FROM inventory;

-- 5. Разделить JSON документ на несколько строк по узлам
CREATE TABLE IF NOT EXISTS expertise_j(doc JSON);

--экспертиза вещей внутри музея
DROP TABLe expertise_j;
INSERT INTO expertise_j VALUES ('[{"art_id": 1, "expertise": "True"}, {"art_id": 2, "expertise": "True"}, {"art_id": 3, "expertise": "False"}]');

SELECT * FROM expertise_j;

-- jsonb_array_elements - Разворачивает массив JSON в набор значений JSON.
SELECT jsonb_array_elements(doc::jsonb)
FROM expertise_j;
