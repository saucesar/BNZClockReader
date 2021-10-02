from _imports import *

class Employee:

    table = 'employees'
    attributes = ('name','pis','created_at','updated_at')

    def __init__(self, id, name, pis, created_at, updated_at) -> None:
        self.id = id
        self.name = name
        self.pis = pis
        self.created_at = created_at
        self.updated_at = updated_at
    
    @staticmethod
    def create_table_sql():
        return '''
                CREATE TABLE IF NOT EXISTS employees 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(255) NOT NULL, pis VARCHAR(11) UNIQUE NOT NULL,
                 created_at DATETIME, updated_at DATETIME)
               '''

    @staticmethod
    def create(name, pis):
        db = Connection()
        db.create_table(Employee.create_table_sql())
        created_at = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        db.insert(Employee.table, str(Employee.attributes), (name, pis, created_at, created_at))
        db.close()
    
    @staticmethod
    def all():
        db = Connection()
        results = db.select("SELECT * FROM "+Employee.table)
        db.close()
        employees = []
        for row in results:
            employees.append(Employee(row[0], row[1], row[2], row[3], row[4]))
        return employees
    
    def __str__(self) -> str:
        return "ID: "+str(self.id)+" NAME: "+self.name+" PIS: "+self.pis+" CREATED_AT: "+self.created_at+" UPDATED_AT: "+self.updated_at

if __name__ == "__main__":
    #Employee.create('Sau Cesar', '11122233344')
    for e in Employee.all():
        print(e)