
class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def show_details(self):

        print(f"Name : {self.name}")
        print(f"ID: {self.id}")