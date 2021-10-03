from _imports import *

class Employee(Model):
    id = PrimaryKeyColumn()
    name = StringColumn()
    pis = StringColumn(max_length=11, unique=True)

    def __str__(self) -> str:
        return "ID: "+str(self.id)+" NAME: "+self.name+" PIS: "+self.pis+" CREATED_AT: "+self.created_at+" UPDATED_AT: "+self.updated_at

if __name__ == "__main__":
    #Employee.create('Sau Cesar', '11122233344')
    for e in Employee.all():
        print(e)