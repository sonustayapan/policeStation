from pickle import TRUE
from django.db import models
from django.db.models.fields import CharField
from django.utils import timezone
from django.db.models.fields import AutoField

# Create your models here.
gender_choice = (
    ('m', 'Male'),
    ('f', 'Female'),
)

select_category = (
    ('Report', 'Report'),
    ('Feedback', 'Feedback'),
)

select_appliction_type = (
    ('RTI', 'RTI'),
    (' Passport|PCC|IC|GEP', 'Passport|PCC|IC|GEP'),
    ('Diplomite|Offical|Application', 'Diplomite|Offical|Application'),
    ('Appeal Application', 'Appeal Application '),
)

class Role(models.Model):
    Role = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'Role'

    def __str__(self):
        return self.Role
        
class Master(models.Model):
    Role = models.ForeignKey(Role, on_delete=models.CASCADE)
    Email = models.EmailField(max_length=50, unique=True)
    Password = models.CharField(max_length=50)
    IsActive = models.BooleanField(default=False)
    DateCreated = models.DateTimeField(auto_now_add=True)
    DateUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Master'

    def __str__(self):
        return self.Email


state = {
    'Bihar': ['hhh','ggg'],
    'Jharkhand': [],
    'Odisha': [],
    'West Bangal': [],
    'Gujrat': [],
    'Haryana': [],
    'Panjab': [],
    

}
state_choices = []
for t in state.keys():
    state_choices.append( (t, t.capitalize()) )

state_choices = tuple(state_choices)

City = {
    'Patna': [],
    'Chhapra': [],
    'Hagipur': [],
    'Siwan': [],
    'Mairwa': [],
    'Aara': [],
    'Gopalganj': [],
    

}
city_choices = []
for ct in City.keys():
    city_choices.append( (ct, ct.capitalize()) )

city_choices = tuple(city_choices)

police_station = {
    'Ganghimadan': [],
    'Danapur': [],
    'Gayghat': [],
    'Baudha calony': [],
    'Boring Road': [],
    'Bally Road': [],
    'Kankadbag': [],
    

}
station_choices = []
for ps in police_station.keys():
    station_choices.append((ps, ps.capitalize()))

station_choices = tuple(station_choices)

    
         
class Complaint(models.Model):
    Master = models.ForeignKey(Master,null=True, blank=True, on_delete=models.CASCADE)
    FullName = models.CharField(max_length=20,blank=True, default="")
    FatherName = models.CharField(max_length=20, default="")
    Address = models.CharField(max_length=200, default="")
    Country = models.CharField(max_length=20, default="")
    State = models.CharField(max_length=20, choices=state_choices)
    City = models.CharField(max_length=20, choices=city_choices)
    PoliceStation = models.CharField(max_length=20, choices=station_choices)
    Pin_Code = models.CharField(max_length=10, default="")
    House_No = models.CharField(max_length=10, default="")
    Discription = models.CharField(max_length=1000, default="")
    Gender = models.CharField(max_length=15, choices=gender_choice)
  

    def __str__(self):
        return self.FullName 


        

class Citizen(models.Model):
    Master = models.ForeignKey(Master,on_delete=models.CASCADE)
    FullName = models.CharField(max_length=50, default='')
    Mobile = models.CharField(max_length=10, default='')
    Gender = models.CharField(max_length=50, choices=gender_choice)
    Address = models.TextField(max_length=50, default='')
    Country = models.CharField(max_length=20, default='')
    State = models.CharField(max_length=20, default='')
    City = models.CharField(max_length=20, default='')
    Pincode = models.CharField(max_length=6, default='')

    IsActive = models.BooleanField(default=False)  

    class Meta:
        db_table = 'Citizen'

    def __str__(self):
        return 'No Details' if not self.FullName else self.FullName
   

class Department(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE) 
    FullName = models.CharField(max_length=30, default="")
    Address = models.CharField(max_length=200, default="")
    Country = models.CharField(max_length=20, default="")
    State = models.CharField(max_length=20, choices=state_choices)
    City = models.CharField(max_length=20, choices=city_choices)
    Pin_Code = models.CharField(max_length=10, default="")
    House_No = models.CharField(max_length=10, default="")
    Discription = models.CharField(max_length=1000, default="")
    Gender = models.CharField(max_length=15, choices=gender_choice)


    class Meta:
        db_table = 'department'

    def __str__(self):
        return 'No Details' if not self.FullName else self.FullName



 
class E_fir(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    FullName = models.CharField(max_length=20, default="")
    CriminalName = models.CharField(max_length=20, default="")
    Address = models.CharField(max_length=200, default="")
    State = models.CharField(max_length=20, default="")
    City = models.CharField(max_length=20, default="")
    PoliceStation = models.CharField(max_length=20, default="")
    House_No = models.CharField(max_length=10, default="")
    E_fir = models.CharField(max_length=1000, default="")
    Gender = models.CharField(max_length=15, choices=gender_choice)

    class Meta:
        db_table = 'e_fir'

    def __str__(self):
        return self.FullName



class Lost_Parson(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    FullName = models.CharField(max_length=20, default="")
    FatherName = models.CharField(max_length=20, default="")
    Address = models.CharField(max_length=200, default="")
    State = models.CharField(max_length=20, default="")
    City = models.CharField(max_length=20, default="")
    PoliceStation = models.CharField(max_length=20, default="")
    Identification_Mark = models.CharField(max_length=10, default="")
    Identity_Card = models.CharField(max_length=10, default="")
    Date = models.DateField(auto_created=True, null=True)
    Gender = models.CharField(max_length=15, choices=gender_choice)
    Discription = models.CharField(max_length=500, default="")


    class Meta:
        db_table = 'lost_parson'

class Passport_Status(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    FullName = models.CharField(max_length=20, default="")
    Dob = models.DateField(auto_created=True, null=True)
    City = models.CharField(max_length=200, default="")
    Select_Appliction_Type = models.CharField(max_length=30, choices = select_appliction_type)
    

    class Meta:
        db_table = 'passport_status'

class Accident(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    FullName = models.CharField(max_length=20, default="")
    Adhar_No = models.CharField(max_length=12, default="")
    Address = models.CharField(max_length=200, default="")
    City = models.CharField(max_length=20, default="")
    PoliceStation = models.CharField(max_length=20, default="")
    Age = models.CharField(max_length=12, default="")
    Car_No = models.CharField(max_length=10, default="")
    Accident_Car = models.CharField(max_length=10, default="") 
    Discription = models.CharField(max_length=1000, default="")
    Gender = models.CharField(max_length=15, choices=gender_choice)

    class Meta:
        db_table = 'accident'

class Police_Varification(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    FullName = models.CharField(max_length=20, default="")
    FatherName = models.CharField(max_length=20, default="")
    Address = models.CharField(max_length=200, default="")
    City = models.CharField(max_length=20, default="")
    PoliceStation = models.CharField(max_length=20, default="")
    Pin_Code = models.CharField(max_length=12, default="")
    House_No = models.CharField(max_length=10, default="")
    Discription = models.CharField(max_length=1000, default="")
    Gender = models.CharField(max_length=15, choices=gender_choice)

    class Meta:
        db_table = 'police_varification'


class Report(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    Select_Category = models.CharField(max_length=20, choices=select_category)
    FullName = models.CharField(max_length=20, default="")
    Subject = models.CharField(max_length=15, default="")
    Address = models.CharField(max_length=200, default="")
    PoliceStation = models.CharField(max_length=20, default="")
    Mobile = models.CharField(max_length=12, default="")
    Discription = models.CharField(max_length=1000, default="")

    class Meta:
         db_table = 'report'


class Go_messege(models.Model):
    FullName = models.CharField(max_length=20, default="")
    Subject = models.CharField(max_length=20, default="")
    Address = models.CharField(max_length=200, default="")
    State = models.CharField(max_length=30, default="")
    City = models.CharField(max_length=30, default="")
    Messege = models.CharField(max_length=1000, default="")

    class Meta:
        db_table = 'go_messege'
            


          
