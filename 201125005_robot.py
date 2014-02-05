import curses
from curses import *
import random

# -----------------------------------------------------------------------------
class curses_screen:
	""" Creates A Screen """
	def __enter__(self):
		self.stdscr = curses.initscr()
		curses.cbreak()
		self.stdscr.clear()
		curses.noecho()
		self.stdscr.keypad(1)
		self.stdscr.border(0)
		return self.stdscr
	def __exit__(self,a,b,c):
		curses.echo()
		curses.endwin()
		self.stdscr.getch()
		self.stdscr.clear()
		self.stdscr.refresh()
# -----------------------------------------------------------------------------
class curses_window:
	""" Creates A Window """
	def __init__(self):
		curses.curs_set(0)
		curses.noecho()
		self.win=curses.newwin(LINES-4,COLS-4,2,2)
		self.win.clear()
		self.win.refresh()
		self.win.keypad(1)
#------------------------------------------------------------------------------
class Gun:
	""" Generates Firing Machines """
	def __init__(self,Arena,Y,X,Pos,LINES,COLS,Level):
		""" Initializing Gun """
		if LEVEL==2:
			self.Y=Y
			self.X=X+3 if Pos==0 else X-1
			map(lambda x: map(lambda y: Arena.addch(Y+y,X+x,'#'),range(3)),range(3))
			if Pos==0: 
				Arena.addch(Y,X+2,' ')
				Arena.addch(Y+2,X+2,' ')
			if Pos==1: 
				Arena.addch(Y,X,' ')
				Arena.addch(Y+2,X,' ')
		if LEVEL==3:
			if Pos ==0: map(lambda x: Arena.addstr(1,x,"### "),range(3,COLS-7,4))
			else:  map(lambda x: Arena.addstr(LINES-1,x,"### "),range(3,COLS-7,4))
			self.yx=range(4,COLS-3,4)
	def fire_small(self,Pos):
		""" Calculate Position Of Small Bullet """
		if Pos==0:
			return (self.X+2) if self.X<COLS-2 else 4
		else: 
			return (self.X-2) if self.X>1 else COLS-5 

	def getBullPos(self,Arena,Pos):
		""" Firing Small Bullet """
		if Arena.inch(self.Y+1,self.X)&255!=ord('D'):
			Arena.addch(self.Y+1,self.X,' ')
		self.X=self.fire_small(Pos)
		if Pos==0:
			if Arena.inch(self.Y+1,self.X)&255!=ord('D'):
				Arena.addch(self.Y+1,self.X,'>')
		elif Pos==1:
			if Arena.inch(self.Y+1,self.X)&255!=ord('D'):
				Arena.addch(self.Y+1,self.X,'<')
		return self.Y+1,self.X
	
	def fire_big(self,Arena,flag,x_loc,y_loc,Pos):
		""" Calculate Position Of Big Bullet """
		if flag==0:
			x_loc=random.choice(self.yx)
		if Pos==0:
			if Arena.inch(y_loc,x_loc)&255!=ord('D'):
				Arena.addstr(y_loc,x_loc,'/')
			if Arena.inch(y_loc+1,x_loc)&255!=ord('D'):
				Arena.addstr(y_loc+1,x_loc,'\\')
			return y_loc+2,x_loc
		else:
			if Arena.inch(y_loc,x_loc)&255!=ord('D'):
				Arena.addstr(y_loc,x_loc,'/')
			if Arena.inch(y_loc-1,x_loc)&255!=ord('D'):
				Arena.addstr(y_loc-1,x_loc,'\\')
			return y_loc-2,x_loc
				
	def clear(self,Arena,x_loc,Pos):
		""" Clearing Game Window """
		L=range(2,LINES-1)
		if Pos==0:
			for i in L:
				if Arena.inch(i,x_loc)&255!=ord('D'):
					Arena.addstr(i,x_loc,' ')
		else:
			L.reverse()
			for i in L:
				if Arena.inch(i,x_loc)&255!=ord('D'):
					Arena.addstr(i,x_loc,' ')
#+-----------------------------------------------------------------------------
def Print_File(self,file,y,x,LINES,COLS):
	""" Printing ASCII Art """
	F=open(file)
	F=F.readlines()
	for lines in F:
		self.addstr(y,x,lines);
		y+=1
		if y==LINES-1: break
	return y
def Pause2(self,time):
	""" Simple Pause """
	for i in range(25):
		self.timeout(time)
		getKey=self.getch()

class MyGame(curses_window):
	""" Main Game Class """
	def Pause(self):
		""" Pause = Press P or p """
		while True:
			if self.win.getch() in [80,112]:
				break
	
	def Display_Hash(self,LINES,COLS,x_loc,y_loc):
		""" Display Animated Hash """
		a,b,x,y,flag,ctr=LINES-2,1,1,COLS-2,0,3
		while True:
			self.win.timeout(ctr)
			getKey=self.win.getch()
			if len([(l,m) for l in range(y_loc-4,y_loc+4*2) for m in range(x_loc-5,x_loc+5*2) if (l,m) ==(a,b)])==0:
				self.win.addch(a,b,'#')
			if len([(l,m) for l in range(y_loc-4,y_loc+4*2) for m in range(x_loc-5,x_loc+5*2) if (l,m) ==(x,y)])==0:
				self.win.addch(x,y,'#')
			if flag==0:
				if b==(COLS-2):
					a,flag,x=a-1,1,x+1
				else:
					b,y=b+1,y-1
			else:
			  	if b==1:
			  		a,x,flag=a-1,x+1,0
			  	else:
			  		b,y=b-1,y+1
			if (abs(b-y)==1 or b==y) and a==x:
				ctr=1
			if a==0:
			  	break
	def Display_Crash(self,Game,x_loc,y_loc):
		""" Display Flashing Effect """
		j,flag=3,0
		for i in range(5):
			Game.getch()
			curses.flash()	
		Game.clear()
		
	def Start(self,Game,LINES,COLS,LEVEL):
		""" Initialize The Game @ Given Level -- Heart Of Program"""
		Game.clear()
		Game.border('|','|','-','-','+','+','+','+')
		x_loc=random.randint(8,COLS-10) # Generating Random Coordinates
		y_loc=random.randint(8,LINES-10)
		ROBO.Place(y_loc,x_loc,Game) #Placing The Robot
		DIFFUSE_C,N_Codes,DC_xy,Key,B_xy=0,10,{},KEY_LEFT,{} #Specifying Constants Which Can Be Altered By The Programmer
		flag=0
		bull_y,bull_x=LINES/5+1,2
		l,m=(random.randint(4,LINES-5),random.randint(4,COLS-6))
		for x in range(3):
			for y in range(3): 
				B_xy[(l+x,m+y)]=1
		for x in range(N_Codes): DC_xy[(random.randint(1,LINES-5),random.randint(4,COLS-6))]=x
		map(lambda x: Game.addch(x[0],x[1],'D'),DC_xy) #Placing Diffuce Codes & Bomb
		map(lambda x: Game.addch(x[0],x[1],'0'),B_xy)
		global Score
		if LEVEL==1:
			    Score=0
			    Limit=401
		if LEVEL==2:
			    Gun1=Gun(Game,LINES/5,1,0,LINES,COLS,LEVEL) #Creating Gun Objects
			    Gun2=Gun(Game,3*LINES/5,1,0,LINES,COLS,LEVEL)
			    Gun3=Gun(Game,2*LINES/5,COLS-4,1,LINES,COLS,LEVEL)
			    Gun4=Gun(Game,4*LINES/5,COLS-4,1,LINES,COLS,LEVEL)
			    Limit=601
		if LEVEL==3:
			    MultiGun1=Gun(Game,1,COLS,0,LINES,COLS,LEVEL)#Creating Lightening Objects
			    MultiGun2=Gun(Game,1,COLS,1,LINES,COLS,LEVEL)
			    La=map(lambda x: (1,x),range(COLS))
			    mxa_loc,mya_loc=4,2
			    Lb=map(lambda x: (LINES-1,x),range(COLS))
			    mxb_loc,myb_loc=LINES-2,COLS-2
			    flag2=0
			    Limit=801
		time=0
		REASON=""
		while True:
			if Key==27:
				self.End(self.win,Score,LEVEL,LINES,COLS)
				return -1,REASON
			if time==Limit:
				   map(lambda x: map(lambda y:Game.addch(l+x,m+y,'0'), range(3)),range(3))
				   Game.addch(l+3/2,m+3/2,'0')
				   for i in range(3):
					   Game.addstr(l-2,m-2,"BEEP!")
					   Pause2(self.win,25)		  
					   Game.addstr(l-2,m-2,"     ")
					   Pause2(self.win,25)		  
					   Pause2(self.win,3)		  
				   Game.addstr(l-2,m,"KABOOM!")
				   self.Display_Hash(LINES,COLS,m,l)
				   REASON="*****TIME FINISHED & BOMB EXPLODED*****"
			time+=1
			if flag==0:
				   map(lambda x: map(lambda y:Game.addch(l+x,m+y,' '), range(3)),range(3))
				   Game.addch(l+3/2,m+3/2,'0')
				   flag=1
			else:
				   map(lambda x: map(lambda y:Game.addch(l+x,m+y,'0'), range(3)),range(3))
				   Game.addch(l+3/2,m+3/2,' ')
				   flag=0
			Game.addstr(0,36," ")
			Game.addstr(0,5,"NUMBER OF DIFFUSE CODES LEFT: "+str(N_Codes-DIFFUSE_C))
			Game.addstr(0,COLS-4,"   ")
			Game.addstr(0,COLS-16,"TIME LEFT: "+str(Limit-time))
			Game.addstr(0,COLS/2+7,"   ")
			Game.addstr(0,COLS/2,"SCORE: "+str(Score))
			Game.timeout(180)
			getKey=Game.getch()
			if getKey in [80,112]:
				Game.addstr(LINES-2,2,"GAME PAUSED")
			     	self.Pause()
				Game.addstr(LINES-2,2,"           ")
			Key=Key if getKey not in [258,259,260,261,27] else getKey
			x_loc,y_loc=ROBO.Move(y_loc,x_loc,Game,Key)
			if LEVEL==2:
			   	L=[]
			   	L.append(Gun1.getBullPos(Game,0))
			   	L.append(Gun2.getBullPos(Game,0))
			   	L.append(Gun3.getBullPos(Game,1))
			   	L.append(Gun4.getBullPos(Game,1))
			if LEVEL==3:
				if flag2==0:
					L=[(mya_loc,mxa_loc),(myb_loc,mxb_loc)]
					mya_loc,mxa_loc=MultiGun1.fire_big(Game,flag2,mxa_loc,2,0)
					myb_loc,mxb_loc=MultiGun2.fire_big(Game,flag2,mxb_loc,LINES-2,1)
					flag2=1
				else:
					mya_loc,mxa_loc=MultiGun1.fire_big(Game,flag2,mxa_loc,mya_loc,0)
					myb_loc,mxb_loc=MultiGun2.fire_big(Game,flag2,mxb_loc,myb_loc,1)
					L[len(L):]=[(mya_loc,mxa_loc),(myb_loc,mxb_loc)]
				     	if abs(mya_loc-LINES)<3: 
						flag2=0
						MultiGun1.clear(Game,mxa_loc,0)
						MultiGun2.clear(Game,mxb_loc,1)
			for x in range(x_loc,x_loc+5): 
				for y in range(y_loc,y_loc+4): 
					if (y,x) in B_xy:
						if DIFFUSE_C<N_Codes: 
							self.Display_Hash(LINES,COLS,x_loc,y_loc)
							REASON="****YOU DIDN'T HAVE ENOUGH DIFFUSE CODES!****"
							return 0,REASON
						else: 
							return 1,REASON
					if (y,x) in DC_xy:
						DIFFUSE_C+=1
						Score+=DIFFUSE_C*(Limit-time)
						DC_xy.pop((y,x))
					if LEVEL==2:
					 	if (y,x) in L:
							curses.flash()
							self.Display_Hash(LINES,COLS,x_loc,y_loc)
							REASON="****YOUR ROBOT GOT SCREWED!****"
							return 0,REASON
					if LEVEL==3:
					  	if (y,x) in L or (y,x) in La+Lb:
							curses.flash()
							REASON="****YOUR ROBOT WAS STRUCK BY LIGHTENING!****"
							self.Display_Hash(LINES,COLS,x_loc,y_loc)
							return 0,REASON	
			if x_loc in [0,COLS-5] or y_loc in [0,LINES-4]:
			   	self.Display_Crash(Game,x_loc,y_loc)
				REASON="****YOUR ROBOT WENT OUT OF BOUNDS!****"
				return 0,REASON
	def End(Arena,self,Score,LEVEL,LINES,COLS):
		""" Ending The Game """
		self.clear()
		F=open("GameOver.txt")
		F=F.readlines()
		y,x=2,2
		for lines in F:
			self.addstr(y,x,lines)
			y+=1
		self.border('|','|','-','-','+','+','+','+')
		self.addstr(LINES/2,COLS/2,"Your Score :"+str(Score))
		self.addstr(LINES/2+1,COLS/2,"You Completed "+str(LEVEL-1)+" Level(s)!")
		Key=self.getch()
		while True:
			self.addstr(LINES/2+2,COLS/2,"Press Escape To Exit...")
			if Key==27: break
			Key=self.getch()
		
	
	
	def Loading(self,LINES,COLS):
		""" Loading A Particular Level """
		self.win.addch(LINES-2,2,'[')
		self.win.addch(LINES-2,COLS-2,']')
		x=3
		while x!=COLS-2:
			self.win.addch(LINES-2,x,'#')
			x+=1
			Pause2(self.win,1)
	
	def Display_Choice(Arena,self,REASON,LINES,COLS):
		""" Display Choices When Robot Dies """
		self.clear()
		self.border('|','|','-','-','+','+','+','+')
		self.addstr(LINES/2-10,COLS/2-10,REASON)
		self.addstr(LINES/2-9,COLS/2-10,"Choices Available: ")
		self.addstr(LINES/2-8,COLS/2-10,"1: Restart Level")
		self.addstr(LINES/2-7,COLS/2-10,"2: Exit Game")
		Key=self.getch()
		while True:
			if Key in [49,50]:
				return Key-48
			elif Key!=-1:
				self.addstr(LINES/2-5,COLS/2-10,"Press 1 or 2 Only!")
			Key=self.getch()
		
# -----------------------------------------------------------------------------
#ROBOT_STYLES:
			
R=[[[' ','i',' ','i',' '],['[','*','_','*',']'],['/','|','_','|','\\'],[' ','/',' ','\\',' ']],
[[' ','!',' ','!',' '],['[','+','_','+',']'],['!','.','_','.','!'],['_','|',' ','|','_']],
[[' ','|','_','|',' '],['d','O','_','O','b'],[' ','[','_',']',' '],[' ','^',' ','^',' ']],
[[' ','\\',' ','/',' '],['[','@','_','@',']'],['/','|','_','|','\\'],[' ','d',' ','b',' ']],
[['\\','^',' ','^','/'],['[','o',' ','o',']'],['$','[','_',']','$'],['_','|',' ','|','_']],
[['\\','_','*','_','/'],['|','^','_','^','|'],['<','|',' ','|','>'],[' ','0',' ','0',' ']],
[[' ','M',' ','M',' '],['<','@','_','@','>'],['\\','\"','_','\"','/'],[' ','%',' ','%',' ']],
[[' ','*','_','*',' '],['[','0','_','0',']'],['/','(','+',')','\\'],['_','|',' ','|','_']],
[[' ','$','^','$',' '],['{','x','_','x','}'],['/',')','_','(','\\'],[' ','u',' ','u',' ']],
[['_','|','^','|','_'],['[','p','_','p',']'],['-','|','_','|','-'],['\\','0','_','0','/']]]
class Robot: 
	""" ROBOT Definitions """
	def __init__(self,choice):
		""" Initialize Robot On Selection Criteria """
		self.type=R[choice]
	def Place(self,y_loc,x_loc,scr):
		""" Place Robot @ Given Coordinates """
		map(lambda i: map(lambda j: scr.addch(i,j,self.type[i-y_loc][j-x_loc]),range(x_loc,x_loc+5)),range(y_loc,y_loc+4))
	def Move(self,y_loc,x_loc,scr,Key):
		""" Move Robot @ Given Coordinates """
		x_a,y_a=(Key==KEY_LEFT and -1 or Key==KEY_RIGHT and 1),(Key==KEY_UP and -1 or Key==KEY_DOWN and 1)
		x_r,y_r=(Key==KEY_LEFT and 5 or Key==KEY_RIGHT and -1),(Key==KEY_UP and 4 or Key==KEY_DOWN and -1)
		start=(((Key==KEY_LEFT or Key==KEY_RIGHT) and y_loc+y_a) or ((Key==KEY_UP or Key==KEY_DOWN) and x_loc+x_a))
		end=(((Key==KEY_LEFT or Key==KEY_RIGHT) and y_loc+y_a+4) or ((Key==KEY_UP or Key==KEY_DOWN) and x_loc+x_a+5))
		self.Place(y_loc+y_a,x_loc+x_a,scr)
		if Key==KEY_LEFT or Key==KEY_RIGHT:
			map(lambda i: scr.addch(i,x_loc+x_a+x_r,' '),range(start,end))
		if Key==KEY_UP or Key==KEY_DOWN:
			map(lambda i: scr.addch(y_loc+y_a+y_r,i,' '),range(start,end))
		return x_loc+x_a,y_loc+y_a
# -----------------------------------------------------------------------------
with curses_screen() as welcome:
	""" Welcome Is An Object Of The Class: curses_screen """
	LINES,COLS=welcome.getmaxyx()
	y=Print_File(welcome,"Robot2.txt",2,2,LINES,COLS)
	y=Print_File(welcome,"Robot1.txt",2,COLS/2,LINES,COLS)
	welcome.border(0)
	welcome.addstr(y-3,COLS/2-30,"WELCOME TO ROBO-BOMB-DEFUSER!")
	welcome.addstr(y-2,COLS/2-30,"Press Any Key To Continue...")
# -----------------------------------------------------------------------------
with curses_screen() as Select_Robot:
	""" Select_Robot Is An Object Of The Class: curses_screen """
	LINES,COLS=Select_Robot.getmaxyx()
	Select_Robot.addstr(2,(COLS-18)/2,"SELECT YOUR ROBOT!")
	MyRobo={}
	for i in range(10):
		MyRobo[i]=Robot(i)
		MyRobo[i].Place(LINES/2,(((COLS-50)/11)+5)*(i+1),Select_Robot)
		Select_Robot.addstr(LINES/2+5,(((COLS-50)/11)+5)*(i+1),"Robot "+"%c"%(i+ord('A')))
	Select_Robot.addstr(LINES/2+10,COLS/2-32,"Enter Your Selection: ")
	global ROBO
	Key=Select_Robot.getch()
	SELECTED=False
	while True:
		if Key in range(65,75):
			Select_Robot.addch(LINES/2+10,COLS/2-10,Key)
			ROBO=Robot(Key-ord('A'))
			ROBO.Place(LINES/2+7,COLS/2,Select_Robot)
			SELECTED=True
		else:
			Select_Robot.addstr(LINES-2,COLS/2-30,"Press Keys Between A-J Only!")
		Key=Select_Robot.getch()
		if Key==10 and SELECTED==True: break
	Select_Robot.addstr(LINES-2,COLS/2-30,"Press Any Key To Continue...")
# -----------------------------------------------------------------------------
Game=MyGame() # Creating an object of MyGame Class
Arena=Game.win
Arena.bkgd(curses.A_REVERSE)
LINES,COLS=Arena.getmaxyx()
LEVEL=1
while True:
	Arena.clear()
	Arena.refresh()
	Arena.border('|','|','-','-','+','+','+','+')
	Print_File(Arena,"Loading.txt",LINES/2-10,COLS/2-30,LINES,COLS)
	Print_File(Arena,'Level'+str(LEVEL)+'.txt',LINES/2-10+8,COLS/2-30,LINES,COLS)
	Arena.border('|','|','-','-','+','+','+','+')
	Game.Loading(LINES,COLS)
	Key=Arena.getch()
	global Score
	while Key==-1:
		Arena.addstr(LINES-10,COLS/2-20,"Press Any Key To Continue...")
		Key=Arena.getch()
	Exit_Status,REASON=Game.Start(Arena,LINES,COLS,LEVEL)
	if Exit_Status==-1: break
	elif Exit_Status==1:
		LEVEL+=1
	else:
		Exit_Status=Game.Display_Choice(Arena,REASON,LINES,COLS)
		if Exit_Status==1: Score=0
	if Exit_Status==2 or LEVEL==4: 
		Game.End(Arena,Score,LEVEL,LINES,COLS)
		break
Game.win.clear() # Exiting Quitely!
curses.endwin()
