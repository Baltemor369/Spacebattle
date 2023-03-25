import tkinter as tk
import dateutil.relativedelta as dr
import re
import datetime
from modules.MangaLib import MangaLib
from modules.Manga import Manga
from modules.CounterList import CounterList

RELIEF = "solid"
BORDER_WIDTH = 2
BACKUP_ERR_MSG = "Data recovery cannot be done\nThe file has been modified"


class UI(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.iconbitmap("asset/logo.ico")
        self.title("Manga Library")

        # listen Escap key press to exit
        self.bind("<Escape>", self.last_window)

        # Create our Manga Library
        self.all_manga = MangaLib()

        self.sort_key = "name"
        self.sort_reverse = False
        self.search_word = ""
        self.index_start_tab = 0
        self.len_tab = 10

        # recover the datas
        if self.all_manga.recover_data("data/data.txt"):
            self.all_manga.sort_manga(self.sort_key)
            self.display_menu()
        else:
            label = tk.Label(self, text=BACKUP_ERR_MSG)
            label.pack()
            self.display_recover_backup()

            self.set_geometry()

    # resize and position the window
    def set_geometry(self):
        self.update_idletasks()
        width = self.winfo_reqwidth() + 100  # margin E-W
        height = self.winfo_reqheight() + 20  # margin N-S

        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def display_menu(self):
        self.clear()
        
        self.search_word = ""

        lib_button = tk.Button(self,
                               width=10,
                               text="My Library",
                               command=self.display_library
                               )
        lib_button.pack(pady=10)

        add_manga_button = tk.Button(self,
                                     width=10,
                                     text="Add Manga",
                                     command=self.display_modification
                                     )
        add_manga_button.pack(pady=10)

        stat_button = tk.Button(self,
                                width=10,
                                text="Stats",
                                command=self.display_stats
                                )
        stat_button.pack(pady=10)

        exit_button = tk.Button(self,
                                width=10,
                                text="Exit",
                                command=self.last_window
                                )
        exit_button.pack(pady=10)

        self.set_geometry()

    def display_library(self):
        self.clear()

        self.index_start_tab = 0

        # HEADER : search bar
        frame_top = tk.Frame(self)
        frame_top.pack()

        label = tk.Label(frame_top, text="Research : ")
        label.pack(side="left")

        search_name = tk.StringVar(self)
        self.search_input = tk.Entry(frame_top,
                                     textvariable=search_name,
                                     width=50
                                     )
        self.search_input.pack(side="left")

        self.search_input.bind("<KeyRelease>", self.research_bar)

        # BODY : tab with mangas
        self.frame_body = tk.Frame(self)
        self.frame_body.pack()

        self.display_tab(self.frame_body,
                         MangaLib(self.all_manga.find_manga(self.search_word)),
                         self.index_start_tab, 
                         self.len_tab
                         )

        # FOOTER : return button and new manga button
        frame_footer = tk.Frame(self)
        frame_footer.pack(pady=5)

        modification_B = tk.Button(frame_footer,
                                   text="New Manga",
                                   width=9,
                                   relief="raised",
                                   command=self.display_modification
                                   )
        modification_B.pack(pady=5)

        back_button = tk.Button(frame_footer,
                                width=9,
                                text="Return",
                                command=self.display_menu
                                )
        back_button.pack(pady=5, side="bottom")

        self.set_geometry()
    
    def bottom_display(self, root_frame:tk.Frame):
        self.frame_bottom = tk.Frame(root_frame)
        self.frame_bottom.pack()
        
        frame_button = tk.Frame(root_frame)
        frame_button.pack()        
    
    def next_page(self):
        self.index_start_tab += self.len_tab
        
        self.table_frame.pack_forget()
        self.display_tab(self.frame_body,
                         MangaLib(self.all_manga.find_manga(self.search_word)),
                         self.index_start_tab, 
                         self.len_tab
                         )

        self.set_geometry()
    
    def previous_page(self):
        self.index_start_tab -= self.len_tab
        
        # tab update only
        self.table_frame.pack_forget()
        self.display_tab(self.frame_body,
                         MangaLib(self.all_manga.find_manga(self.search_word)),
                         self.index_start_tab, 
                         self.len_tab
                         )
        
        self.set_geometry()

    def research_bar(self, evt):
        self.search_word = self.search_input.get()
        
        self.index_start_tab = 0
        
        # tab update only 
        self.table_frame.pack_forget()
        self.display_tab(self.frame_body,
                         MangaLib(self.all_manga.find_manga(self.search_word.capitalize())),
                         self.index_start_tab, 
                         self.len_tab
                         )

        self.set_geometry()

    def display_tab(self, root_frame:tk.Frame, data:MangaLib, start:int, howmany:int):
        self.table_frame = tk.Frame(root_frame)
        self.table_frame.pack()

        table_labels = []
        row_labels = []
        # heading
        for j, key in enumerate(Manga(0).__dict__):
            match key:
                case "description":
                    label = tk.Label(self.table_frame,
                                     text=key,
                                     relief=RELIEF,
                                     borderwidth=BORDER_WIDTH
                                     )
                    label.grid(row=0, column=j, sticky="nsew")
                case "Primary_key":
                    # invisible case
                    label = tk.Label(self.table_frame, text="", relief="flat")
                    label.grid(row=0, column=j, sticky="nsew")
                case _:
                    if key == self.sort_key:
                        if not self.sort_reverse:
                            label = tk.Label(self.table_frame, text=f"{key} ▼", relief=RELIEF, borderwidth=BORDER_WIDTH)
                            label.grid(row=0, column=j, sticky="nsew")
                            label.bind("<Button-1>", lambda evt, k=key : self.sort_my_lib(k))
                        else:
                            label = tk.Label(self.table_frame, text=f"{key} ▲", relief=RELIEF, borderwidth=BORDER_WIDTH)
                            label.grid(row=0, column=j, sticky="nsew")
                            label.bind("<Button-1>", lambda evt, k=key : self.sort_my_lib(k))
                    else:
                        label = tk.Label(self.table_frame, text=f"{key}", relief=RELIEF, borderwidth=BORDER_WIDTH)
                        label.grid(row=0, column=j, sticky="nsew")
                        label.bind("<Button-1>", lambda evt, k=key : self.sort_my_lib(k))
            row_labels.append(label)
        table_labels.append(row_labels)

        # element add
        if len(data.get(start, howmany)) > 0:
            for i, elt in enumerate(data.get(start, howmany)):
                row_labels = []
                for j, key in enumerate(elt.__dict__):
                    if key == "Primary_key":
                        label = tk.Label(self.table_frame, text="Modify", relief="raised", borderwidth=BORDER_WIDTH)
                        label.grid(row=i+1, column=j, sticky="nsew")
                        label.bind("<Button-1>", lambda evt, i=data.get_id(elt) : self.display_modification(i))
                    else:
                        label = tk.Label(self.table_frame, text=elt.__dict__[key], relief=RELIEF, borderwidth=BORDER_WIDTH)
                        label.grid(row=i+1, column=j, sticky="nsew")
                    label.configure(padx=10, pady=5)
                    row_labels.append(label)
                table_labels.append(row_labels)

        frame = tk.Frame(self.table_frame)
        frame.grid(columnspan=len(Manga.__dict__))

        if self.index_start_tab > 0:
            previous_page = tk.Button(frame, text="Previous", command=self.previous_page)
            previous_page.pack(side="left")

        if len(data.get_all_manga()) > self.index_start_tab + self.len_tab:
            next_page = tk.Button(frame, text="Next", command=self.next_page)
            next_page.pack(side="left")
        
        self.set_geometry()

    def sort_my_lib(self, key:str):
        self.index_start_tab = 0
        if key == self.sort_key:
            self.sort_reverse = not self.sort_reverse
            self.all_manga.sort_manga(key, self.sort_reverse)
        else:
            self.sort_reverse = False
            self.sort_key = key
            self.all_manga.sort_manga(key)
        self.table_frame.pack_forget()
        self.display_tab(self.frame_body, self.all_manga, self.index_start_tab, self.len_tab)

    def display_modification(self, ID:int = -1):
        self.clear()

        frame_top = tk.Frame(self)
        frame_top.pack(side="top")

        frame_column_label = tk.Frame(frame_top)
        frame_column_label.pack(side="left", fill="x")

        frame_column_entry = tk.Frame(frame_top)
        frame_column_entry.pack(side="left", fill="x")

        for key in Manga(0).__dict__:

            frame_case = tk.Frame(frame_column_label)
            frame_case.pack(side="top", anchor="center")
            buffer = tk.StringVar(self)

            match key:
                case "name":
                    if ID != -1:
                        buffer.set(self.all_manga.get_manga(id=ID).name)
                    self.name_entry = tk.Entry(frame_column_entry, textvariable=buffer, justify=tk.LEFT)
                    self.name_entry.pack(side="top")
                    label = tk.Label(frame_case, text=f"{key} :")
                    label.pack(side="left")

                case "author":
                    if ID != -1:
                        buffer.set(self.all_manga.get_manga(id=ID).author)
                    else:
                        buffer.set("Unknown")
                    self.author_entry = tk.Entry(frame_column_entry, textvariable=buffer, justify=tk.LEFT)
                    self.author_entry.pack(side="top")
                    label = tk.Label(frame_case, text=f"{key} :")
                    label.pack(side="left")

                case "type":
                    if ID != -1:
                        buffer.set(self.all_manga.get_manga(id=ID).type)
                    else:
                        buffer.set("Unknown")
                    self.type_entry = tk.Entry(frame_column_entry, textvariable=buffer, justify=tk.LEFT)
                    self.type_entry.pack(side="top")
                    label = tk.Label(frame_case, text=f"{key} :")
                    label.pack(side="left")

                case "volume_number":
                    if ID != -1:
                        buffer.set(self.all_manga.get_manga(id=ID).volume_number)
                    self.volume_nb_entry = tk.Entry(frame_column_entry, textvariable=buffer, justify=tk.LEFT)
                    self.volume_nb_entry.pack(side="top")
                    label = tk.Label(frame_case, text="volume number :")
                    label.pack(side="left")

                case "description":
                    if ID != -1:
                        buffer.set(self.all_manga.get_manga(id=ID).description)
                    else:
                        buffer.set("None")
                    self.description_entry = tk.Entry(frame_column_entry, textvariable=buffer, justify=tk.LEFT)
                    self.description_entry.pack(side="top")
                    label = tk.Label(frame_case, text=f"{key} :")
                    label.pack(side="left")

                case "valuation":
                    if ID != -1:
                        buffer.set(self.all_manga.get_manga(id=ID).valuation)
                    self.valuation_entry = tk.Entry(frame_column_entry, textvariable=buffer, justify=tk.LEFT)
                    self.valuation_entry.pack(side="top")
                    label = tk.Label(frame_case, text=f"{key} :")
                    label.pack(side="left")

        frame_bottom = tk.Frame(self)
        frame_bottom.pack(side="top")

        add_button = tk.Button(frame_bottom, width=5, text="Add", command=lambda: self.modification(ID))
        add_button.pack(side="top")

        if ID != -1:
            del_button = tk.Button(frame_bottom, width=5, text="Delete", command=lambda Pkey=ID: self.delete_manga(Pkey))
            del_button.pack(side="top", pady=10)

            back_button = tk.Button(frame_bottom, width=5, text="Return", command=self.display_library)
            back_button.pack(side="top")
        else:
            back_button = tk.Button(frame_bottom, width=5, text="Return", command=self.display_menu)
            back_button.pack(side="top")

        self.set_geometry()

    def modification(self, ID:int):
        # recovery input datas
        name_get = self.name_entry.get()
        author_get = self.author_entry.get()
        type_get = self.type_entry.get()
        volume_nb_get = self.volume_nb_entry.get()
        description_get = self.description_entry.get()
        valuation_get = self.valuation_entry.get()

        # Check in input datas
        data_verify = True

        # Creating regex exp for the check in input data
        # allow alphanumeric characters and "," "." "-" " "
        reg_text = r"^[\w,\.\- ^_]+$"
        # allow list of int separate by "," or "-"
        reg_volume = r"^\d{1,4}(?:(?:,\d{1,4})|(?:-\d{1,4}))*$"
        # allow int and float between 0 and 10 included
        reg_valuation = r"^(?:10(?:\.0)?|\d(?:\.\d)?)$"

        if re.match(reg_text, name_get) is None:
            data_verify = False
        if re.match(reg_text, author_get) is None:
            data_verify = False
        if re.match(reg_text, type_get) is None:
            data_verify = False
        if re.match(reg_text, description_get) is None:
            data_verify = False
        if re.match(reg_volume, volume_nb_get) is None:
            data_verify = False
        if re.match(reg_valuation, valuation_get) is None:
            data_verify = False

        if data_verify:
            if ID != -1:
                # modify the manga at @index
                self.all_manga.modify_manga(Manga(ID, name_get.capitalize(), author_get, type_get, int(volume_nb_get), description_get, float(valuation_get)), ID)
                self.all_manga.save_data()
            else:
                # add the manga to manga list
                for elt in split_VN(volume_nb_get):
                    self.all_manga.add_manga(Manga(self.all_manga.get_new_id(), name_get.capitalize(), author_get, type_get, int(elt), description_get, float(valuation_get)))
                    self.all_manga.save_data()

            # display the new library
            self.display_library()

    def display_stats(self):
        self.clear()

        self.calcul_stats()

        # refaire l'affichae
        for key in self.data_stat:
            frame_row = tk.Frame(self)
            frame_row.pack()
            frame_case_key = tk.Frame(frame_row)
            frame_case_key.pack(side="left")
            label = tk.Label(frame_case_key, text=f"{key} : ")
            label.pack()
            frame_case_value = tk.Frame(frame_row)
            frame_case_value.pack(side="left")
            label = tk.Label(frame_case_value, text=f"{self.data_stat[key]}")
            label.pack()

        # back button
        back_button = tk.Button(self, width=9, text="Return", command=self.display_menu)
        back_button.pack(side="bottom", pady=5)

        self.set_geometry()

    def calcul_stats(self):
        self.data_stat = {}
        # total manga
        self.data_stat["Total mangas"] = len(self.all_manga.get_all_manga())

        # total by names
        stat_name = CounterList()
        for elt in self.all_manga.get_all_names():
            stat_name.add_name(elt)
        self.data_stat["Total by names"] = stat_name

        # total by type
        stat_type = CounterList()

        for elt in self.all_manga.get_all_types():
            stat_type.add_name(elt)
        self.data_stat["Total by types"] = stat_type

        # total par auteur
        stat_author = CounterList()

        for elt in self.all_manga.get_all_authors():
            stat_author.add_name(elt)
        self.data_stat["Total by authors"] = stat_author

        # current time
        now = datetime.datetime.now()

        # counter definition
        self.data_stat["Total last week"] = 0
        self.data_stat["Total last month"] = 0
        self.data_stat["Total last year"] = 0

        for elt in self.all_manga.get_all_manga():
            delta = dr.relativedelta(now, elt.time)
            if delta.days <= 7:
                self.data_stat["Total last week"] += 1
            if delta.months <=1:
                self.data_stat["Total last month"] += 1
            if delta.years <= 1:
                self.data_stat["Total last year"] += 1

        valuations = self.all_manga.get_all_valuations()
        try:
            self.data_stat["Valuation average"] = round(sum(valuations)/len(valuations), 2)
        except Exception:
            self.data_stat["Valuation average"] = 0
        try:
            self.data_stat["Valuation standard deviation"] = max(valuations) - min(valuations)
        except Exception:
            self.data_stat["Valuation standard deviation"] = 0

    def delete_manga(self, index:int):
        self.all_manga.del_manga(index)
        self.all_manga.save_data()
        
        self.search_word = ""

        self.display_library()

    # function to clear the window
    def clear(self) -> None:
        for widget in self.winfo_children():
            widget.pack_forget()

    # function execute before closing
    def last_window(self, evt="") -> None:
        for widget in self.winfo_children():
            widget.pack_forget()
        
        label_frame = tk.Frame(self)
        label_frame.pack()
        button_Frame = tk.Frame(self)
        button_Frame.pack()

        label = tk.Label(label_frame, text="Do you want to make a backup of your library ?")
        label.pack()

        yes_B = tk.Button(button_Frame, text="Yes", command=self.backup )
        yes_B.pack(side="left")

        no_B = tk.Button(button_Frame, text="No", command=self.exit)
        no_B.pack(side="left")

        self.set_geometry()

    def backup(self):
        with open("data/backup.txt","w") as file:
            self.all_manga.sort_manga("ID_key")
            for elt in self.all_manga.get_all_manga():
                elt.time = elt.time.replace(microsecond=0)
                buffer = f"@#ID-{str(elt.Primary_key)}#N-{str(elt.name)}#A-{str(elt.author)}#TY-{str(elt.type)}"
                buffer += f"#VN-{str(elt.volume_number)}#D-{str(elt.description)}#VA-{str(elt.valuation)}#TI-{str(elt.time)}#@\n"
                file.write(buffer)
        
        self.exit()

    def display_recover_backup(self):

        label_frame = tk.Frame(self)
        label_frame.pack()
        button_Frame = tk.Frame(self)
        button_Frame.pack()

        label = tk.Label(label_frame, text="Would you like to recover the data from the last backup ?")
        label.pack()
        
        yes_B = tk.Button(button_Frame, text="Yes", command= self.recover_backup)
        yes_B.pack(side="left")

        no_B = tk.Button(button_Frame, text="No", command=self.destroy)
        no_B.pack(side="left")

        self.set_geometry()
    
    def recover_backup(self):
        self.all_manga.recover_data("data/backup.txt")
        self.all_manga.save_data()
        self.display_menu()

    def exit(self):
        self.all_manga.save_data()
        self.destroy()


def split_VN(string:str) -> list[int]:
    list_volume_number = []
    buffer = string.split(",")
    for elt in buffer:
        if elt.find("-") == -1:
            list_volume_number.append(int(elt))
        else:
            starter = int(elt.split("-")[0])
            ending = int(elt.split("-")[1])
            for i in range(starter, ending+1):
                list_volume_number.append(int(i))

    return list_volume_number
