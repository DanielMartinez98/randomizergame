from operator import countOf, truediv
import os,pygame,time,random,copy, math, threading
import perlin
from pygame import math

pygame.init()
spaces = 100
data = [[0]*spaces for _ in range(spaces)]    
datachange = copy.deepcopy(data)
whilecount = 0
#mapFunct
wallprob = 1
def generateMap():
    arr = [[0]*spaces for _ in range(spaces)]
    newseed = random.randrange(0,10000)
    #3print(newseed)    
    noise = perlin.perlin(newseed)
    noise.two_octave(10,10)
    noise = perlin.perlin(newseed)
    if noise.two(0,0)>wallprob or noise.two(spaces-1,spaces-1)>wallprob:
        return generateMap()
    for i in range(0,spaces):
        for y in range(0,spaces):
            #print(noise.two(i,y))
            if noise.two(i,y) >wallprob:
                arr[i][y] = 1
            if noise.two(i,y)>wallprob*4:
                arr[i][y] = 7
    return arr         
def clearData():
    global data
    global datachange
    global noise_data 
    noise_data = generateMap()
    data = [[0]*spaces for _ in range(spaces)]
    data[0][0] = 1
    data[spaces-1][spaces-1] =2
    datachange = copy.deepcopy(data)
    for i in range(0,spaces):
        for y in range(0,spaces):
            if noise_data[i][y]==1:
                data[i][y] = 3
                datachange[i][y] = 3
            elif noise_data[i][y]==7:
                data[i][y] = 7
                datachange[i][y] = 7
    
clearData()
#print(noise_data)
sizex,sizey, id,pth = 1000,1000, 1, os.path.dirname(__file__)
screen = pygame.display.set_mode((sizex,sizey+50))
#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(pth+'\\assets\\'+str(id)+'.png')
pygame.display.set_icon(icon)
#Player
print("the path: "+pth+"\\assets\player.png")
playerImg = pygame.image.load(pth+'\\assets\\'+str(id)+'.png')
newPlayerImg = pygame.transform.scale(playerImg,(sizex/spaces,sizey/spaces))
class advanceMap(threading.Thread):
    def __init__(self,i):
        threading.Thread.__init__(self)
        self.i = i
        #print(i)
        global spaces
        
    def run(self,j):
        global whilecount
        global data
        global datachange
        if j == 0:
            for y in range(0,spaces):
                check = True
                if data[i][y] != 0 and data[i][y]<3:
                    if i != spaces-1 and check :
                        print("a")
                        if random.randint(0,1)==True and datachange[i+1][y]!= data[i][y]:
                            if datachange[i+1][y]>=3 and datachange[i+1][y]!=6:
                                if datachange[i+1][y]==7:
                                    datachange[i+1][y]=data[i][y]
                                else:
                                    datachange[i+1][y] +=1
                            else:
                                datachange[i+1][y]= data[i][y]
                            check = False
                    if i != 0 and check:
                        if random.randint(0,1)==True and datachange[i-1][y]!= data[i][y]:
                            if datachange[i-1][y]>=3 and datachange[i-1][y]!=6:
                                if datachange[i-1][y]==7:
                                    datachange[i-1][y]=data[i][y]
                                else:
                                    datachange[i-1][y] +=1
                            else:
                                datachange[i-1][y]= data[i][y]
                            check = False
                    if y != spaces-1 and check:
                        if random.randint(0,1)==True and datachange[i][y+1]!= data[i][y]:
                            if datachange[i][y+1]>=3 and datachange[i][y+1]!=6:
                                if datachange[i][y+1]==7:
                                    datachange[i][y+1]=data[i][y]
                                else:
                                    datachange[i][y+1] +=1
                            else:
                                datachange[i][y+1]= data[i][y]
                            check = False
                    if y != 0 and check:
                        if random.randint(0,1)==True and datachange[i][y-1]!= data[i][y]:
                            if datachange[i][y-1]>=3 and datachange[i][y-1]!=6:
                                if datachange[i][y-1]==7:
                                    datachange[i][y-1]=data[i][y]
                                else:
                                    datachange[i][y-1] +=1
                            else:
                                datachange[i][y-1]= data[i][y]
                            check = False
        else:
            for y in range(spaces-1,0,-1):
                check = True
                if data[i][y] != 0 and data[i][y]<3:
                    if i != spaces-1 and check :
                        if random.randint(0,1)==True and datachange[i+1][y]!= data[i][y]:
                            if datachange[i+1][y]>=3 and datachange[i+1][y]!=6:
                                if datachange[i+1][y]==7:
                                    datachange[i+1][y]=data[i][y]
                                else:
                                    datachange[i+1][y] +=1
                            else:
                                datachange[i+1][y]= data[i][y]
                            check = False
                    if i != 0 and check:
                        if random.randint(0,1)==True and datachange[i-1][y]!= data[i][y]:
                            if datachange[i-1][y]>=3 and datachange[i-1][y]!=6:
                                if datachange[i-1][y]==7:
                                    datachange[i-1][y]=data[i][y]
                                else:
                                    datachange[i-1][y] +=1
                            else:
                                datachange[i-1][y]= data[i][y]
                            check = False
                    if y != spaces-1 and check:
                        if random.randint(0,1)==True and datachange[i][y+1]!= data[i][y]:
                            if datachange[i][y+1]>=3 and datachange[i][y+1]!=6:
                                if datachange[i][y+1]==7:
                                    datachange[i][y+1]=data[i][y]
                                else:
                                    datachange[i][y+1] +=1
                            else:
                                datachange[i][y+1]= data[i][y]
                            check = False
                    if y != 0 and check:
                        if random.randint(0,1)==True and datachange[i][y-1]!= data[i][y]:
                            if datachange[i][y-1]>=3 and datachange[i][y-1]!=6:
                                if datachange[i][y-1]==7:
                                    datachange[i][y-1]=data[i][y]
                                else:
                                    datachange[i][y-1] +=1
                            else:
                                datachange[i][y-1]= data[i][y]
                            check = False
        whilecount+= 1
def player(a,b):
    screen.blit(newPlayerImg,(a,b))
arr = []
for i in range(0,spaces):
    arr.append(advanceMap(i))
#GameLoops
running = True
counta = 0
countb = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    data = copy.deepcopy(datachange)
    if random.randint(0,1)==True:
        counta +=1
        for x in arr:
            x.run(0)
    else:
        countb +=1
        for x in reversed(arr):
            x.run(1)
    contr = 0
    contb = 0
    while(whilecount != spaces):
        print("yo",whilecount)
    whilecount = 0
    for i in range(0,spaces):
        for y in range(0,spaces):
            if data[i][y] ==1:
                contr += 1
            elif data[i][y] == 2:
                contb += 1
            if datachange[i][y] !=0:
                playerImg = pygame.image.load(pth+'\\assets\\'+str(datachange[i][y])+'.png')
                newPlayerImg = pygame.transform.scale(playerImg,(sizex/spaces+1,sizey/spaces+1))
                player(i*sizex/spaces,y*sizey/spaces)
    #time.sleep(.1)
    #print("a: "+str(counta)+" b: "+str(countb))
    if contr ==0 or contb ==0:
        if contr == 0:
            print("Blue Wins")
        else:
            print("Red Wins")
        running = False
    if event.type == pygame.KEYDOWN:
  
            # Check for backspace
            if event.key == pygame.K_BACKSPACE:
                clearData()
                
                screen.fill((0,0,0))                

                
    pygame.display.update()
    