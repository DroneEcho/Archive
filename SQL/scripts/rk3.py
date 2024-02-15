from peewee import *
from datetime import *
from req import *

con = PostgresqlDatabase(
    database='postgres',
    user='postgres',
    password='123',
    host='127.0.0.1', 
    port="5432"
)

class BaseModel(Model):
    class Meta:
        database = con


class Employee(BaseModel):
    id = IntegerField(column_name='id')
    fio = CharField(column_name='fio')
    date_of_birth = DateField(column_name='date_of_birth')
    department = CharField(column_name='department')

    class Meta:
        table_name = 'employee'

class EmployeeAttendance(BaseModel):
    id = IntegerField(column_name='id')
    employee_id = ForeignKeyField(Employee, backref='employee_id')
    data = DateField(column_name='date')
    day_of_week =  CharField(column_name='day_of_week')
    time = TimeField(column_name='time')
    type = IntegerField(column_name='type')	

    class Meta:
        table_name = 'employee_attendance'

def Task1():
    global con

    cur = con.cursor()

    cur.execute(FirstQ)
    print("Запрос 1:\n")
    rows = cur.fetchall()
    for row in rows:
        print(*row)

    cur.execute(SecondQ)
    print("\nЗапрос 2:\n")
    rows = cur.fetchall()
    for row in rows:
        print(*row)

    cur.execute(ThirdQ)
    print("\nЗапрос 3:\n")
    rows = cur.fetchall()
    for row in rows:
        print(*row)

    cur.close()

def Task2():
    global con

    cur = con.cursor()
    #SELECT *
    #FROM employee
    #WHERE department = 'Бухгалтерия' AND date_of_birth =
    #(SELECT MIN(date_of_birth)
    #FROM employee
    #WHERE department = 'Бухгалтерия'
    #);
    print("1. Найти самого старшего сотрудника бухгалтерии")
    query = Employee.select(Employee.id).where(Employee.department == 'Бухгалтерия').where(Employee.date_of_birth == (Employee.select(min(Employee.date_of_birth)).where(Employee.department == 'Бухгалтерия')))
    for q in query.dicts().execute():
        print(q)

    #SELECT DISTINCT department
    #FROM employee e JOIN employee_attendance ea on e.id = ea.employee_id
    #WHERE date = '2023-11-15' AND type = 1 AND time > '09:00:00'
    print("3. все отделы в кот есть сотрудники, опоздавшие в определенную дату")
    query = Employee.select(Employee.department).join(EmployeeAttendance).where(EmployeeAttendance.date > '2023-11-15').where(EmployeeAttendance.type==1).where(EmployeeAttendance.date > '09:00:00')
    for q in query.dicts().execute():
        print(q)

    cur.close()
	

def main():
	Task1()
	Task2()

	con.close()

if __name__ == "__main__":
	main()