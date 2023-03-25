import copy

from modules.Manga import Manga
from modules.MangaLib import MangaLib
from modules.generator_manga import random_manga
from modules.MangaUI import UI


# test class Manga
manga_temoin = Manga(0,"test2","test2","test2",1,"test2",1)
manga_test = random_manga(0)

# test methods
manga_test.change_name("test2")
manga_test.change_author("test2")
manga_test.change_type("test2")
manga_test.change_volume_number(1)
manga_test.change_description("test2")
manga_test.change_valuation(1)

if manga_test.__dict__ == manga_temoin.__dict__: # verify __eq__ method
    print("Manga Class : OK")
else:
    print("Manga Class : not OK")

try:
    print(manga_test) # verify __repr__ method
    print("Display manga : OK")
except:
    print("Display manga : not OK")

lib = MangaLib()

# test add a manga
try:
    for i in range(5):
        lib.add_manga(random_manga(i))
    print("add_manga mangalib : OK")
except:
    print("add_manga mangalib : not OK")

# test delete a manga
try:
    lib.del_manga(3)
    if len(lib.get())==4:
        print("del_manga mangalib : OK")
    else:
        print("del_manga mangalib : not OK")
except:
    print("del_manga mangalib : not OK")

# test get a new id
try:
    if lib.get_new_id()==3:
        print("get_new_id mangalib : OK")
except:
    print("get_new_id mangalib : not OK")
    
# test __repr__ method
try:
    print(lib)
    print("Display mangalib : OK")
except:
    print("Display mangalib : not OK")

# test modify a manga
manga_temoin = random_manga(0)
manga_test = copy.copy(manga_temoin)


try:
    ui = UI()
    # ui.mainloop()
except:
    input()
input()