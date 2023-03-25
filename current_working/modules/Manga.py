import datetime

class Manga:
    def __init__(self, primary_key:int,name="",  author="", type="", volume_nb=0, description="", valuation=0.0, time=datetime.datetime.now()) -> None:
        self.name = name
        self.author = author
        self.type = type
        self.volume_number = volume_nb
        self.description = description
        self.valuation = valuation
        self.time = time # Will be used to store the time at which the manga was added
        self.Primary_key = primary_key

    def __repr__(self) -> str:
        buff = f"Name : {self.name} \nAutor : {self.author} \nType : {self.type} \n"
        buff += f"Number of volume : {self.volume_number} \nDescription : {self.description} \n"
        buff += f"Valuation : {self.valuation}/10 \nTime : {self.time.year}-{self.time.month}-{self.time.day} {self.time.hour}:{self.time.minute}:{self.time.second} \n"
        buff += f"ID : {self.Primary_key}\n"
        return buff

    def __eq__(self, __o: object) -> bool:
        for key in ["name", "author", "volume_number"]:
            if self.__dict__[key] != __o.__dict__[key]:
                return False
        return True
        

    def change_volume_number(self, new_value:int) -> None:
        self.volume_number = new_value
    
    def change_type(self, new_type:str) -> None:
        self.type = new_type
    
    def change_author(self, new_author:str) -> None:
        self.author = new_author

    def change_name(self, new_name:str) -> None:
        self.name = new_name
    
    def change_description(self, new_text:str) -> None:
        self.description = new_text

    def change_valuation(self, new_value:float) -> None:
        if 10 >= new_value >= 0:
            self.valuation = new_value
