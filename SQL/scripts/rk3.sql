
--задание 1

CREATE TABLE IF NOT EXISTS employee (
    id INT PRIMARY KEY,
    fio VARCHAR(32),
    date_of_birth DATE,
    department VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS employee_attendance(
    id INT PRIMARY KEY,
    employee_id INT REFERENCES employee(id),
    date DATE DEFAULT CURRENT_DATE,
    day_of_week VARCHAR,
    time TIME DEFAULT CURRENT_TIME,
    type INT
);

INSERT INTO employee (id, fio, date_of_birth, department) 
VALUES (1,'Иванов', '25-09-1990', 'ИТ'), (2,'Петров', '12-11-1987', 'Бухгалтерия'),
(3,'Иванов1', '25-09-1990', 'ИТ'), (4,'Петров1', '12-11-1987', 'Бухгалтерия'),
(5,'Old', '12-11-1930', 'Бухгалтерия') 

INSERT INTO employee_attendance (id, employee_id, date, day_of_week, time, type) 
VALUES (1, 1,'19-12-2023', 'Вторник', '9:00', 1),
        (2, 1,'19-12-2023', 'Вторник', '9:20', 2),
        (3, 1,'19-12-2023', 'Вторник', '9:25', 1),
        (4, 2,'19-12-2023', 'Вторник', '9:05', 1),
        (5, 3,'19-12-2023', 'Вторник', '9:00', 2),
		(6, 3,'19-12-2023', 'Вторник', '9:00', 2),
		(7, 3,'19-12-2023', 'Вторник', '9:00', 2),
		(8, 3,'19-12-2023', 'Вторник', '9:00', 2),
        (9, 4,'19-12-2023', 'Вторник', '9:20', 2),
        (11, 5,'19-12-2023', 'Вторник', '9:05', 2)


--Написать скалярную функцию, возвращающую количество сотрудников
--в возрасте до 52, выходивших не более 3х раз

--учитываются только те сотрудники, что выходили хотя бы 1 раз
CREATE OR REPLACE FUNCTION EmployeeFind() RETURNS INTEGER
AS
$$
    SELECT COUNT(*)
    FROM employee_attendance ea JOIN employee e on ea.employee_id = e.id
    WHERE type = 2 AND date_part('year', age(date_of_birth)) < 52
    GROUP BY employee_id, date
    HAVING COUNT(*) < 4;
$$LANGUAGE SQL;

SELECT * FROM EmployeeFind();

--1 Первый запрос (SQL)
--Найти самого старшего в бухгалтерии
SELECT *
FROM employee
WHERE department = 'Бухгалтерия' AND date_of_birth =
(SELECT MIN(date_of_birth)
FROM employee
WHERE department = 'Бухгалтерия'
);
--2 Второй запрос (SQL)
--Найти сотрудников которые отсутствовали в общей сложности больше 20 мин
--отсутствие во время перерывов от работы
select DISTINCT employee_id
from employee join
	(
	select employee_id, date, time, 
			type, 
			lag(time) over (partition by employee_id, date order by time) as prev_time, 
			time-lag(time) over (partition by employee_id, date order by time) as tmp_dur
		from employee_attendance r 
		order by employee_id, date, time
		) as small_durations
on employee.id = small_durations.employee_id
where small_durations.date = '19-12-2023'
and small_durations.tmp_dur > '00:20:00'
group by small_durations.employee_id
HAVING count(small_durations.employee_id) > 1

--3 все отделы в кот есть сотрудники, опоздавшие в определенную дату
SELECT DISTINCT department
FROM employee e JOIN employee_attendance ea on e.id = ea.employee_id
WHERE date = '19-12-2023' AND type = 1 AND time > '09:00:00';
