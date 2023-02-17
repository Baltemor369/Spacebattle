import tkinter as tk, threading as th, time, random as rd,math

# img= tk.ImageTk.PhotoImage(tk.Image.open("download.png"))

# task list :
# + make randomly spawning of ennemy (infity mode)
# + make logique spawning of ennemy (story mode)
# + make boss generation
# + make score
# + escape key
# + start exit param mode buttons (UI)

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
    def __init__(self,width:int,heigth:int,speed:int,pos=Coord(),life=1):
        self.pos=pos
        self.w=width
        self.h=heigth
        self.speed=speed
        self.life=life
    
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
    def get_life(self):
        return self.life
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
    def set_life(self,val:int):
        self.life=val
    
    def move_up(self):
        self.pos.set_y(self.get_pos().get_y()-self.get_speed())
    def move_down(self):
        self.pos.set_y(self.get_pos().get_y()+self.get_speed())
    def move_left(self):
        self.pos.set_x(self.get_pos().get_x()-self.get_speed())
    def move_right(self):
        self.pos.set_x(self.get_pos().get_x()+self.get_speed())
    
    def hit(self):
        if self.life>0:
            self.life-=1

class Spacebattle(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.win_w=900
        self.win_h=900
        self.x=(self.winfo_screenwidth()-self.win_w)/2
        self.y=(self.winfo_screenheight()-self.win_h)/2
        self.geometry(f"{self.win_w}x{self.win_h}+{int(self.x)}+{int(self.y)}")
        
        self.can_w=600
        self.can_h=900
        
        self.player_size=50
        self.player_speed=1/2
        self.missile_w=20
        self.missile_h=30
        self.missile_speed=1
        self.ennemy_size=50
        self.ennemy_speed=1/5
        self.boss_w=int(self.can_w*0.8)
        self.boss_h=int(self.can_h*0.3)
        self.boss_speed=1/10
        
        self.score=0
        self.endgame_message=""
        self.endgame=False

        self.canva=tk.Canvas(self,width=self.can_w,height=self.can_h,bg="cyan")
        self.canva.pack(side="left")

        self.score_L=tk.Label(self,text=f"score : {self.score}")
        self.score_L.pack()

        self.endgame_message_L=tk.Label(self,text=f"{self.endgame_message}")
        self.endgame_message_L.pack()

        self.player=Sprite(self.player_size,self.player_size,self.player_speed,Coord((self.can_w-self.player_size)/2,self.can_h*0.9))
        self.player_struct=self.canva.create_rectangle(self.player.get_x(),self.player.get_y(),self.player.get_x()+self.player.get_width(),self.player.get_y()+self.player.get_heigth(), fill="black")

        self.missile=[]
        self.missile_struct=[]
        
        self.ennemy=[Sprite(self.ennemy_size,self.ennemy_size,self.ennemy_speed,Coord((self.can_w-self.ennemy_size)/2,0))]
        self.ennemy_struct=[self.canva.create_rectangle(self.ennemy[0].get_x(),self.ennemy[0].get_y(),self.ennemy[0].get_x()+self.ennemy[0].get_width(),self.ennemy[0].get_y()+self.ennemy[0].get_heigth(),fill="black")]

        self.boss=[]
        self.boss_struct=[]
        
        self.move_up=False
        self.move_left=False
        self.move_down=False
        self.move_right=False

        self.bind("<KeyPress>",self.move)
        self.bind("<KeyRelease>",self.unmove)
        self.bind("<space>",self.fire)
        self.bind("<Escape>",self.exit)

    def run(self):
        self.game()

    def game(self):
        # player move management
        if self.move_up and self.out(self.player).find("U")==-1 :
            self.player.move_up()
        if self.move_right and self.out(self.player).find("R")==-1:
            self.player.move_right()
        if self.move_down and self.out(self.player).find("D")==-1:
            self.player.move_down()
        if self.move_left and self.out(self.player).find("L")==-1 :
            self.player.move_left()
        
        self.handle_collision()

        self.handle_move_ONP()

        self.handle_collision()

        # spawn ennemy every 1s, synchronize with the clock 
        if ennemy_spawn.is_set():
            self.gen_ennemy(rd.randrange(0,self.can_w-self.ennemy_size),-self.ennemy_size)
            ennemy_spawn.clear()
        
        # canva update
        for i in range(0,len(self.missile_struct)):
            self.canva.moveto(self.missile_struct[i],self.missile[i].get_x(),self.missile[i].get_y())
        for i in range(0,len(self.ennemy_struct)):
            self.canva.moveto(self.ennemy_struct[i],self.ennemy[i].get_x(),self.ennemy[i].get_y())
        
        self.canva.moveto(self.player_struct,self.player.get_x(),self.player.get_y())

        # score update
        self.score_L.config(text=f"score : {self.score}")
        # loop funtion
        if not self.endgame:
            self.after(1,self.game)
    
    def handle_move_ONP(self):# Object No PLayer
        # missile movement
        for elt in self.missile:
            elt.move_up()
        # ennemy movement
        i=0
        for elt in self.ennemy:
            elt.move_down()
            # ennemy elts out of the canva are delete
            if elt.get_y()>self.can_h:
                self.score+=10
                self.del_ennemy(i)
            i+=1
        #boss movement
        for elt in self.boss:
            if elt.get_y()<= self.can_h*0.35:
                elt.move()
    
    def handle_collision(self):
        # collision between player and ennemys management
        for elt in self.ennemy:
            if collision(self.player,elt):
                self.player.hit()
            if self.player.get_life()==0:
                self.endgame=True
                self.endgame_message="Game Over"
                break
        
        # collision between missiles and ennemy management
        for miss in range(0,len(self.missile)):
            for enn in range(0,len(self.ennemy)):
                if miss<len(self.missile) and enn<len(self.ennemy):
                    if collision(self.missile[miss],self.ennemy[enn]):
                        self.score+=100
                        self.canva.delete(self.missile_struct[miss])
                        self.canva.delete(self.ennemy_struct[enn])
                        self.del_ennemy(enn)
                        self.del_missile(miss)

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
        self.missile.append(Sprite(10,30,self.missile_speed,Coord(self.player.get_x()+(self.player.get_width())/2,self.player.get_y()-self.missile_h)))
        self.missile_struct.append(self.canva.create_rectangle(self.missile[-1].get_x(),self.missile[-1].get_y(),self.missile[-1].get_x()+self.missile[-1].get_width() ,self.missile[-1].get_y()+self.missile[-1].get_heigth(),fill="orange"))
         
    def gen_ennemy(self,x:int,y:int):# add elts to generate a ennemy
        self.ennemy.append(Sprite(self.ennemy_size,self.ennemy_size,self.ennemy_speed,Coord(x,y)))
        self.ennemy_struct.append(self.canva.create_rectangle(self.ennemy[0].get_x(),self.ennemy[0].get_y(),self.ennemy[0].get_x()+self.ennemy[0].get_width(),self.ennemy[0].get_y()+self.ennemy[0].get_heigth(),fill="black"))
    
    def gen_boss(self):# add elts to generate a boss
        self.boss.append(Sprite(self.boss_w,self.boss_h,self.boss_speed,Coord(self.can_w*0.1,-self.boss_h),5))# "5" for testing => adapt to the score
        self.boss_struct.append(self.canva.create_rectangle(self.ennemy[0].get_x(),self.ennemy[0].get_y(),self.ennemy[0].get_x()+self.ennemy[0].get_width(),self.ennemy[0].get_y()+self.ennemy[0].get_heigth(),fill="blue"))
    
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

    def exit(self,event):
        self.endgame=True
        self.destroy()

class Clock(th.Thread):
    def __init__(self):
        th.Thread.__init__(self)
        self.time=0
        self.stop=False

    def run(self):
        while not self.stop:
            self.time+=0.01
            time.sleep(0.01)
            self.time=round(self.time,3)
            if self.time%1==0:
                ennemy_spawn.set()
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

def between(val:int,start:int,end:int):
    if start>end:
        if start >= val >= end:
            return True
    else:
        if end >= val >= start:
            return True
    return False

def collision(sp1:Sprite,sp2:Sprite):
    if between(sp1.get_x(),sp2.get_x(),sp2.get_x()+sp2.get_width()) or between(sp1.get_x()+sp1.get_width(),sp2.get_x(),sp2.get_x()+sp2.get_width()):
        if between(sp1.get_y(),sp2.get_y(),sp2.get_y()+sp2.get_width()) or between(sp1.get_y()+sp1.get_heigth(),sp2.get_y(),sp2.get_y()+sp2.get_width()):
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