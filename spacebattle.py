import tkinter as tk, threading as th, time

# img= tk.ImageTk.PhotoImage(tk.Image.open("download.png"))
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
        self.missile=[Sprite(self.missile_w,self.missile_h,2,Coord(self.player.get_x()+self.player_size/2,self.player.get_y()-self.missile_h))]
        self.missile_struct=[]
        # Coord(self.player.get_x()+self.player_size/2,self.player.get_y()-self.missile_h)

        self.ennemy_size=50
        self.ennemy=[Sprite(self.ennemy_size,self.ennemy_size,1/5,Coord((self.can_w-self.ennemy_size)/2,0))]
        self.ennemy_struct=[self.canva.create_rectangle(self.ennemy[0].get_x(),self.ennemy[0].get_y(),self.ennemy[0].get_x()+self.ennemy[0].get_width(),self.ennemy[0].get_y()+self.ennemy[0].get_heigth(),fill="black")]


        self.move_up=False
        self.move_left=False
        self.move_down=False
        self.move_right=False

        self.bind("<KeyPress>",self.move)
        self.bind("<KeyRelease>",self.unmove)

        self.game()

    def game(self):
        # Event player(move, fire)
        if self.move_up:
            self.player.move_up()
        if self.move_right:
            self.player.move_right()
        if self.move_down:
            self.player.move_down()
        if self.move_left:
            self.player.move_left()
        self.canva.moveto(self.player_struct,self.player.get_x(),self.player.get_y())

        # Collision(Player-IA,Missile-IA)
        for elt in self.ennemy:
            if collision(self.player,elt):
                self.endgame=True
        
        # for elt in self.missile:

        # Event IA(moving)
        for elt in self.ennemy:
            elt.move_down()
        for i in range(0,len(self.ennemy_struct)):
            self.canva.moveto(self.ennemy_struct[i],self.ennemy[i].get_x(),self.ennemy[i].get_y())

        if not self.endgame:
            self.after(1,self.game)
    
    def move(self,event):
        if event.keysym=="z":
            if not self.move_down:
                self.move_up= True
        elif event.keysym=="q":
            if not self.move_right:
                self.move_left = True
        elif event.keysym=="s":
            if not self.move_up:
                self.move_down= True
        elif event.keysym=="d": 
            if not self.move_left:
                self.move_right = True
    
    def unmove(self,event):
        if event.keysym=="z":
            if not self.move_down:
                self.move_up=False
        elif event.keysym=="q":
            if not self.move_right:
                self.move_left =False
        elif event.keysym=="s":
            if not self.move_up:
                self.move_down=False
        elif event.keysym=="d": 
            if not self.move_left:
                self.move_right =False

        
    def fire(self):
        self.missile_struct.append(self.canva.create_rectangle(self.missile.get_pos().get_x()))

class Timer(th.Thread):
    def __init__(self,time:int):
        th.Thread.__init__(self)
        self.stop=True
        self.time=time

    def run(self):
        while self.time!=0:
            time.sleep(1/self.speed)
            self.time-=1

def collision(sp1:Sprite,sp2:Sprite):
    if sp1.get_x()>=sp2.get_x() and sp1.get_x()<=sp2.get_x()+sp2.get_width():
        if sp1.get_y()>=sp2.get_y() and sp1.get_y()<=sp2.get_y()+sp2.get_heigth():
            return True
    if sp1.get_x()+sp1.get_width()>=sp2.get_x() and sp1.get_x()+sp1.get_width()<=sp2.get_x()+sp2.get_width():
        if sp1.get_y()+sp1.get_heigth()>=sp2.get_y() and sp1.get_y()+sp1.get_heigth()<=sp2.get_y()+sp2.get_heigth():
            return True
    return False

game=Spacebattle()
game.start()
game.mainloop()