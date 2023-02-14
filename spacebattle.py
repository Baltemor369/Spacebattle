import tkinter as tk, threading as th, time

# img= tk.ImageTk.PhotoImage(tk.Image.open("download.png"))

# task list :
# + make randomly spawning of ennemy (infity mode)
# + make boss 
# + make score
# + escape key
# + start exit param mode buttons

class Coord():
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
    
    def set_x(self,val:int):
        self.x=val
    def set_y(self,val:int):
        self.y=val
    
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y

    def set(self,pos):
        self.x=pos.get_x()
        self.y=pos.get_y()

    def display(self):
        print(f"({self.x}:{self.y})")

class Sprite():
    def __init__(self,width:int,heigth:int,speed:int,pos=Coord()):
        self.pos=pos
        self.w=width
        self.h=heigth
        self.speed=speed
    
    def get_pos(self):
        return self.pos
    def get_x(self):
        return self.pos.get_x()
    def get_y(self):
        return self.pos.get_y()
    def get_width(self):
        return self.w
    def get_heigth(self):
        return self.h
    def get_speed(self):
        return self.speed
    def set_pos(self,pos:Coord):
        self.pos.set(pos)
    def set_w(self,width:int):
        self.w=width
    def set_h(self,heigth:int):
        self.h=heigth
    def set_speed(self,speed:int):
        self.speed=speed
    def set_x(self,val:int):
        self.pos.set_x(val)
    def set_y(self,val:int):
        self.pos.set_y(val)
    
    def move_up(self):
        self.pos.set_y(self.get_pos().get_y()-self.get_speed())
    def move_down(self):
        self.pos.set_y(self.get_pos().get_y()+self.get_speed())
    def move_left(self):
        self.pos.set_x(self.get_pos().get_x()-self.get_speed())
    def move_right(self):
        self.pos.set_x(self.get_pos().get_x()+self.get_speed())

class Spacebattle(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.endgame=False
        self.win_w=900
        self.win_h=900
        self.x=(self.winfo_screenwidth()-self.win_w)/2
        self.y=(self.winfo_screenheight()-self.win_h)/2
        self.geometry(f"{self.win_w}x{self.win_h}+{int(self.x)}+{int(self.y)}")
        
        self.can_w=600
        self.can_h=900
        self.canva=tk.Canvas(self,width=self.can_w,height=self.can_h,bg="cyan")
        self.canva.pack(side="left")

        self.player_size=50
        self.player=Sprite(self.player_size,self.player_size,1/2,Coord((self.can_w-self.player_size)/2,self.can_h*0.9))
        self.player_struct=self.canva.create_rectangle(self.player.get_x(),self.player.get_y(),self.player.get_x()+self.player.get_width(),self.player.get_y()+self.player.get_heigth(), fill="black")

        self.missile_w=20
        self.missile_h=30
        self.missile=[]
        self.missile_struct=[]
        
        self.ennemy_size=50
        self.ennemy=[Sprite(self.ennemy_size,self.ennemy_size,1/5,Coord((self.can_w-self.ennemy_size)/2,0))]
        self.ennemy_struct=[self.canva.create_rectangle(self.ennemy[0].get_x(),self.ennemy[0].get_y(),self.ennemy[0].get_x()+self.ennemy[0].get_width(),self.ennemy[0].get_y()+self.ennemy[0].get_heigth(),fill="black")]

        self.clock=list
        
        self.move_up=False
        self.move_left=False
        self.move_down=False
        self.move_right=False
        # self.fire_ready=False

        self.bind("<KeyPress>",self.move)
        self.bind("<KeyRelease>",self.unmove)
        self.bind("<space>",self.fire)

    def run(self):
        self.game()

    def game(self):
        # player move management
        if self.out(self.player).find("U")==-1 and self.move_up:
            self.player.move_up()
        if self.out(self.player).find("R")==-1 and self.move_right:
            self.player.move_right()
        if self.out(self.player).find("D")==-1 and self.move_down:
            self.player.move_down()
        if self.out(self.player).find("L")==-1 and self.move_left:
            self.player.move_left()
        
        # canva update
        self.canva.moveto(self.player_struct,self.player.get_x(),self.player.get_y())

        # collision between player and ennemys management
        for elt in self.ennemy:
            if collision(self.player,elt):
                self.endgame=True
        
        # collision between missiles and ennemy management
        for miss in range(0,len(self.missile)):
            for enn in range(0,len(self.ennemy)):
                if collision(self.missile[miss],self.ennemy[enn]):
                    self.canva.delete(self.missile_struct[miss])
                    self.canva.delete(self.ennemy_struct[enn])
                    self.del_ennemy(enn)
                    self.del_missile(miss)
        
        # missile move management
        i=0
        for elt in self.missile:
            elt.move_up()
            # canva update
            self.canva.moveto(self.missile_struct[i],elt.get_x(),elt.get_y())
            i+=1

        # spawn ennemy every 3s, synchronize with the clock 
        if ennemy_spawn.is_set():
            self.gen_ennemy()
            ennemy_spawn.clear()

        # ennemy move management
        i=0
        for elt in self.ennemy:
            elt.move_down()
            # ennemy elts out of the canva are delete
            if elt.get_y()>self.can_h:
                self.del_ennemy(i)
            i+=1
        # canva update
        for i in range(0,len(self.ennemy_struct)):
            self.canva.moveto(self.ennemy_struct[i],self.ennemy[i].get_x(),self.ennemy[i].get_y())

        # loop funtion
        if not self.endgame:
            self.after(1,self.game)
    
    def move(self,event):
        if event.keysym=="z":
                self.move_up= True
        elif event.keysym=="q":
                self.move_left = True
        elif event.keysym=="s":
                self.move_down= True
        elif event.keysym=="d": 
                self.move_right = True
    
    def unmove(self,event):
        if event.keysym=="z":
                self.move_up=False
        elif event.keysym=="q":
                self.move_left =False
        elif event.keysym=="s":
                self.move_down=False
        elif event.keysym=="d": 
                self.move_right =False

    def fire(self,event):
        if missile_ready.is_set():
            self.gen_missile()
            missile_ready.clear()

    def gen_missile(self):# add elts to generate a missile
        self.missile.append(Sprite(10,30,1,Coord(self.player.get_x()+(self.player.get_width())/2,self.player.get_y()-self.missile_h)))
        self.missile_struct.append(self.canva.create_rectangle(self.missile[-1].get_x(),self.missile[-1].get_y(),self.missile[-1].get_x()+self.missile[-1].get_width() ,self.missile[-1].get_y()+self.missile[-1].get_heigth(),fill="orange"))
         
    def gen_ennemy(self):# add elts to generate a ennemy
        self.ennemy.append(Sprite(self.ennemy_size,self.ennemy_size,1/5,Coord((self.can_w-self.ennemy_size)/2,-self.ennemy_size)))
        self.ennemy_struct.append(self.canva.create_rectangle(self.ennemy[0].get_x(),self.ennemy[0].get_y(),self.ennemy[0].get_x()+self.ennemy[0].get_width(),self.ennemy[0].get_y()+self.ennemy[0].get_heigth(),fill="black"))
    
    def del_ennemy(self,ind:int):
        self.ennemy.pop(ind)
        self.ennemy_struct.pop(ind)
    
    def del_missile(self,ind:int):
        self.missile.pop(ind)
        self.missile_struct.pop(ind)

    def out(self,sp:Sprite):
        buff=""
        if sp.get_x()<=0 :
             buff+="L"
        if sp.get_y()<=0 :
             buff+="U"
        if sp.get_x()+sp.get_width()>=self.can_w :
             buff+="R"
        if sp.get_y()+sp.get_heigth()>=self.can_h:
             buff+="D"
        return buff

class Clock(th.Thread):
    def __init__(self):
        th.Thread.__init__(self)
        self.time=0
        self.stop=False

    def run(self):
        while not self.stop:
            self.time+=0.5
            time.sleep(0.5)
            if self.time%3==0:
                ennemy_spawn.set()
            if self.time%1==0:
                missile_ready.set()

    def exit(self):
        self.stop=True

class Game(th.Thread):
    def __init__(self):
        th.Thread.__init__(self)
        self.spacebattle=Spacebattle()
        self.clock=Clock()

    def run(self):
        self.spacebattle.run()
        self.clock.run()

def between(nb:int,start:int,end:int):
    if start<=end:
        if nb >= start and nb <= end:
            return True
    else:
         if nb <= start and nb >= end:
            return True
    return False

def collision(sp1:Sprite,sp2:Sprite):
    if between(sp1.get_x(),sp2.get_x(),sp2.get_x()+sp2.get_width()):
        if between(sp1.get_y(),sp2.get_y(),sp2.get_y()+sp2.get_heigth()):
            return True
    if between(sp1.get_x()+sp1.get_width(),sp2.get_x(),sp2.get_x()+sp2.get_width()):
        if between(sp1.get_y()+sp1.get_heigth(),sp2.get_y(),sp2.get_y()+sp2.get_heigth()):
            return True
    return False

missile_ready=th.Event()
missile_ready.set()
ennemy_spawn=th.Event()
respawn_player=th.Event()

var=Game()
var.start()
var.spacebattle.mainloop()
var.clock.exit()
var._stop()