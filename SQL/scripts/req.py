FirstQ = """
SELECT *
FROM employee
WHERE department = 'Бухгалтерия' AND date_of_birth =
(SELECT MIN(date_of_birth)
FROM employee
WHERE department = 'Бухгалтерия'
)
"""

SecondQ = """
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

"""

ThirdQ = """
SELECT DISTINCT department
FROM employee e JOIN employee_attendance ea on e.id = ea.employee_id
WHERE date = '2023-11-15' AND type = 1 AND time > '09:00:00'
"""