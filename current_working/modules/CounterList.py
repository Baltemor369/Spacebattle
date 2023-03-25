class CounterList:
    def __init__(self) -> None:
        self.counter_list = []
    
    def __repr__(self) -> str:
        buff = "\n"
        for elt in self.counter_list:
            buff += f"{elt['name']} : {elt['counter']}\n"
        return buff

    def add_name(self, name:str) -> None:
        if not self.check_name(name):
            self.counter_list.append({'name': name, 'counter': 1})
        else:
            self.increment_counter(name)

    def increment_counter(self, name:str) -> None:
        for item in self.counter_list:
            if item['name'] == name:
                item['counter'] += 1

    def check_name(self, name:str) -> bool:
        for item in self.counter_list:
            if item['name'] == name:
                return True
        return False