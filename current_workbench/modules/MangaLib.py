import datetime
import re
from typing import List
from modules.Manga import Manga


class MangaLib:
    def __init__(self,all_manga:List[Manga]=[]) -> None:
        self.list_manga:List[Manga] = all_manga.copy()

    def __repr__(self) -> str:
        buff = ""
        for elt in self.list_manga:
            buff += elt.__repr__() +"\n"
        return buff

    def add_manga(self, manga:Manga) -> None:
        if not self.is_in(manga):
            self.list_manga.append(manga) # adds the manga to the list
    
    def del_manga(self,ID_key=-1) -> None:
        if 0 <= ID_key < len(self.get_all_manga()):
            self.list_manga.pop(self.get_index(ID_key))

    def modify_manga(self, manga:Manga, id:int) -> None:
        #recherche de l'index avec id
        index = self.get_index(id)
        self.list_manga[index].change_name(manga.name)
        self.list_manga[index].change_author(manga.author)
        self.list_manga[index].change_type(manga.type)
        self.list_manga[index].change_volume_number(manga.volume_number)
        self.list_manga[index].change_description(manga.description)
        self.list_manga[index].change_valuation(manga.valuation)    
        
    def find_manga(self, name:str) -> List[Manga]:
        if name=="":
            return self.get_all_manga()
        else:
            result = []
            for elt in self.list_manga:
                if len(name)<=len(elt.name):
                    check_char = True
                    for char_name,char_elt in zip(name.lower(),elt.name.lower()):
                        if char_name != char_elt:
                            check_char = False
                    if check_char:
                        result.append(elt)
            return result
    
    def set_mangas(self, mangas:List[Manga]) -> None:
        self.list_manga = mangas

    # return a copy of mangas
    def get(self, index=0, howmany=10) -> List[Manga]:
        buffer = []
        
        if howmany >= len(self.list_manga)-index:
            howmany = len(self.list_manga)-index
        for i in range(index, index + howmany):
            buffer.append(self.list_manga[i])
        return buffer

    def get_all_manga(self):
        return self.list_manga.copy()

    # return the manga's @id of @manga
    def get_id(self,manga:Manga) -> int:
        for elt in self.get_all_manga():
            if manga == elt:
                return elt.Primary_key
        return -1 # code error

    # return the manga's index by id research
    def get_index(self, id:int) -> int:
        for i,elt in enumerate(self.get_all_manga()):
            if elt.Primary_key == id:
                return i
        return -1 # code error
    
    # return a manga depends on a id or index given
    def get_manga(self, id:int=-1, index:int=-1):
        if id != -1:
            for elt in self.get_all_manga():
                if elt.Primary_key == id:
                    return elt
        elif index != -1:
            return self.get_all_manga()[index]
        else:
            return -1 # code error
                  
    # sort the list of mangas by a sort_key @sort_category and a order @reverse
    def sort_manga(self,sort_category="name", reverse=False) -> None:
        match sort_category:
            case "name":
                self.list_manga.sort(key=lambda Manga: Manga.name, reverse=reverse) 
            case "time":
                self.list_manga.sort(key=lambda Manga: Manga.time, reverse=reverse)
            case "type":
                self.list_manga.sort(key=lambda Manga: Manga.type, reverse=reverse)
            case "volume_number":
                self.list_manga.sort(key=lambda Manga: Manga.volume_number, reverse=reverse)
            case "author":
                self.list_manga.sort(key=lambda Manga: Manga.author, reverse=reverse)
            case "valuation":
                self.list_manga.sort(key=lambda Manga: Manga.valuation, reverse=reverse)    
            case "ID_key":
                self.list_manga.sort(key=lambda Manga: Manga.Primary_key, reverse=reverse)
    
    # return a list of all names
    def get_all_names(self) -> List[str]:
        buff = []
        for elt in self.get_all_manga():
            buff.append(elt.name)
        return buff
    
    # return a list of all authors
    def get_all_authors(self) -> List[str]:
        buff = []
        for elt in self.get_all_manga():
            buff.append(elt.author)
        return buff
    
    # return a list of all types
    def get_all_types(self) -> List[str]:
        buff = []
        for elt in self.get_all_manga():
            buff.append(elt.type)
        return buff
    
    # return a list of all valuations
    def get_all_valuations(self) -> List[float]:
        buff = []
        for elt in self.get_all_manga():
            buff.append(elt.valuation)
        return buff
    
    def get_all_id(self) -> List[int]:
        buff = []
        for elt in self.get_all_manga():
            buff.append(elt.Primary_key)
        return buff

    # Function to save the datas in a file
    def save_data(self) -> None:
        with open("data/data.txt","w") as file:
            self.sort_manga("name")
            for elt in self.get_all_manga():
                elt.time = elt.time.replace(microsecond=0)
                buffer = f"@#ID-{str(elt.Primary_key)}#N-{str(elt.name)}#A-{str(elt.author)}#TY-{str(elt.type)}"
                buffer += f"#VN-{str(elt.volume_number)}#D-{str(elt.description)}#VA-{str(elt.valuation)}#TI-{str(elt.time)}#@\n"
                file.write(buffer)
    
    # Function to retrieve the datas saved
    def recover_data(self, path:str) -> bool:
        return self.read_file(path)
            

    def read_file(self, file_path:str) -> bool:
        list_mangas = []
        with open(file_path,"r") as file:
            while 1:
                buffer = file.readline()
                if buffer != "":
                    list_mangas.append(buffer)
                else:
                    break
            if len(list_mangas)==0:
                return True
        return self.convert_data(list_mangas)

    def convert_data(self, mangas:List[str]) -> bool:
        id_r = r"#ID-(\d+)#"
        name_r = r"#N-([\w,\.\- ^_]+)#"
        author_r = r"#A-([\w,\.\- ^_]+)#"
        type_r = r"#TY-([\w,\.\- ^_]+)#"
        volume_nb_r = r"#VN-(\d+)#"
        description_r = r"#D-([\w ,\.\-^_]+)#"
        valuation_r = r"#VA-(10(?:\.0)?|\d(?:\.\d)?)#"
        time_r = r"#TI-(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})#"

        format_string = "%Y-%m-%d %H:%M:%S"
        
        for elt in mangas:
            try:
                ID_key = re.search(id_r,elt).group(1)
                name = re.search(name_r,elt).group(1)
                author = re.search(author_r,elt).group(1)
                type = re.search(type_r,elt).group(1)
                volume_nb = re.search(volume_nb_r,elt).group(1)
                description = re.search(description_r,elt).group(1)
                valuation = re.search(valuation_r,elt).group(1)
                time = re.search(time_r,elt).group(1)
                time = datetime.datetime.strptime(time,format_string)
                self.add_manga(Manga(int(ID_key), name, author, type, int(volume_nb), description, float(valuation), time))
            except:
                return False
        return True
            
    
    def is_in(self, manga:Manga) -> bool:
        for elt in self.get_all_manga():
            if elt == manga:
                return True
        return False
            

    def get_new_id(self):
        self.sort_manga("ID_key")

        ID_key = 0
        for elt in self.get_all_manga():
            if elt.Primary_key == ID_key:
                ID_key += 1
            else:
                return ID_key
        return ID_key