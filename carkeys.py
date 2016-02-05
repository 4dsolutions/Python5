"""
For more background on the story told by this "play"
http://insights.cermacademy.com/2016/01/124-personal-risk-in-the-internet-of-things-kirby-urner/

"""

class BatteryDead(Exception):
    pass

class IgnitionKeyBreak(Exception):
    def __init__(self, ext = True):
        self.key_extracted = ext

class Car:
    def ignition(self):
        """may raise exceptions (comment / uncomment )"""
        # raise IgnitionKeyBreak(False)
        
my_car = Car()

try:
    print("Open car door")  # might be a database
    my_car.ignition( ) # may raise exceptions

# such as...

except BatteryDead:
    print("Call AAA")

except IgnitionKeyBreak as event:
    if event.key_extracted:
        print("Seek backup key") # what I did
    else:
        print("Call AAA")

except Exception:
    pass    

else:
    # happens if try block raises no exceptions
    print("Motor running... ")

finally:
    # happens no matter what
    print("Close car Door")  # if one were open
    
    
    
    