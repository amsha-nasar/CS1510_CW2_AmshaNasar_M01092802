#daataa should be protected 
#what actions u can do on certain data 
#functions u can apply to data make up encapsulated objecct/class
#double underscore to make data private eg __init__.py
"access modifiers, public,private,protected"
#class doesny occupy memeoryy / no allocation
#actual onbject takes memory
#created using class name and round brackets 
"use object.attribute to assign vales to attributes"

'''
check if new incidents are being added/deleted propely to database or not
add UML diagram 
ReadMe,technical report,code comments 
OOP very important 
class names should be nouns and singular(not plural)
"""
each table is one class
what relationships can u establish
make relation between users and cyber- created by and username are linked 
username becomes foreign key in cyber table 
establish relationship
"""
clone repository?? before starting oop?
how to git commit with api key 
with OOP you can get 90 or 100 with proper documenation
'''
import string

class Student:
    def __init__(self,id,name,age,mark):   #constructor to initalse values 
       self.__id=id
       self.__name=name
       self.__age=age
       self.__mark=mark

    def __init__(self,id,name,age,mark):   #constructor to initalse values 
       self.__id=900
       self.__name="amy"
       self.__age=age
       self.__mark=90

    
    def __str__(self):
        return f"Student info, {self.name},{self.name}"

    def get_name(self):
        return self.name
    def get_age(self):
        return self.age
    def get_passed(self):
        if self.mark>50:
            return "passed"

    
    
    
std1=Student(13,'amsha',18,80)
print(std1,"obj created",std1.name)
std2=Student(10,"hasan",12,90)
print(std2,"obj created")
print(std2)
d=std1.get_name()
print(d)

print(std2.get_passed())
   
"Inheritance"
class Animal:
    def __init__(self,name,age):
        self.__name=name


    




     

