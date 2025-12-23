from ast import Name
import math
rad = 1.89
#Function
def calAreaSq(rad):
    return math.pi * rad * rad

print(calAreaSq(rad))

#Class
class emp:
    def __init__(self, name, emp_id, experience, dept):
        self.Name = name
        self.Emp_id = emp_id
        self.Experience = experience
        self.Dept = dept
        print("Employee {} is added".format(self.Emp_id))
    
    def calcSalary(self):
        if self.Experience>5 and self.Dept=="R & D":
            self.Salary = 200000
        else:
            self.Salary = 80000
        
        print("Salary Calculated")
    
    def empdesc(self):
        print("Employee Name: {} from {} department working with us for {} years".format(self.Name, self.Dept, self.Experience))

#Object: attribute and function calling
emp1 = emp("Faiz ", 3490, 6, "R & D")
emp1.calcSalary()
emp1.Salary
emp1.empdesc()

#Inheritance
class subEmp(emp):

    #If wanna add a new attribute to the class from which sub class in inherited from
    def __init__(self, name, emp_id, experience, dept, subsidiary):
        super(subEmp, self).__init__(name,emp_id,experience,dept)
        self.Subsidiary=subsidiary

    def calcSalary(self):
        self.Salary = min(max(1,self.Experience) * 20000,200000)
    
        
emp1_sub = subEmp("tina", 56034, 6, "Marketing", 7568)
emp1_sub.Subsidiary
emp1_sub.calcSalary()
emp1_sub.Salary