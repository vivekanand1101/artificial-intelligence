# This question is done under the
# assumption that there won't be any
# faulty cars.
# ----------------PEAS-------------
# Performance Measure:
#      1. The agent covers all the cars
#      2. He does not come out with a faulty car
#      3. He takes the shortest path
#      4. Does this in minimum time
# Environment:
#      1. Cars
#      2. Road
#      3. Shop
# Actuators:
#      1. Instruments (to check whether faulty or not)
# Sensors (don't need 1st and 4th in question_1):
#      1. Faulty tire detection sensor (checks for tire in hand)
#      2. Current location sensor (whether at rear, front, corner etc.)
#      3. Car detection sensor (if a car is present at that location)
#      4. Tire detection sensor (check whether the tire is present at that
#         location)
#      5. Sensor to detect car with faulty tire
# Rules:
#      1. Start the agent from the shop
#      2. If in the front and at the last car's second tire, go up
#      3. if in the rear and at the last car's second tire, go down
#      4. if in the front and not at the last car's second tire, go left
#      5. if in the rear and not at the last car's second tire, go right

class environment():

    def get_shop_parking_size(self):
        self.parking_size = int(raw_input())
        return self.parking_size

    def get_location_and_condition(self):
        self.                

class agent():

    def __init__(self):
        self.number_of_cars = environ.get_shop_parking_size()
        self.location_and_condition = environ.get_location_and_condition()

    def start(self):
        self.number_of_cars = self.get_number_of_cars()

def main():
    number_of_test_cases = int(raw_input())
    while(number_of_test_cases):
        environ = environment()
        _agent = agent()
        number_of_test_cases = number_of_test_cases - 1

if "__name__" == "__main__":
    main()
