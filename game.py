from operator import countOf, truediv
import os,pygame,time,random,copy, math, threading
import perlin
from pygame import math

pygame.init()
spaces = 90
data = [[0] *spaces for _ in range(spaces)]
dataprev = copy.deepcopy(data)
datachange = copy.deepcopy(data)
newseed = 0
whilecount = 0
moneyr,moneyb = 0,0
#mapFunct
wallprob = 1
sprites = []

    
def generateMap():
    global newseed
    check = 0
    arr = [[0]*spaces for _ in range(spaces)]
    newseed = random.randrange(0,10000)
    #3print(newseed)    
    noise = perlin.perlin(newseed)
    noise.two_octave(1,1)
    noise = perlin.perlin(newseed)
    
    if noise.two(0,0)>wallprob or noise.two(spaces-1,spaces-1)>wallprob or (noise.two(0,0)<-wallprob or noise.two(spaces-1,spaces-1)<-wallprob):
        print("dang")
        return generateMap()
    for i in range(0,spaces):
        for y in range(0,spaces):
            #print(noise.two(i,y))
            #print(noise.two(i,y))
            if noise.two(i,y) >wallprob or noise.two(i,y) <-wallprob:
                arr[i][y] = 1
            if noise.two(i,y)>wallprob*4 or noise.two(i,y) <-wallprob*4:
                arr[i][y] = 7
                check += 1
    if check < spaces*spaces/8:
        print("not even close")
        return generateMap()
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
pygame.display.set_caption("COCA Vs Bepis")
icon = pygame.image.load(pth+'\\assets\\'+str(id)+'.png')
pygame.display.set_icon(icon)
#Player
for i in range(1,11):
    playerImg = pygame.image.load(pth+'\\assets\\'+str(i)+'.png')
    newPlayerImg = pygame.transform.scale(playerImg,(sizex/spaces+1,sizey/spaces+1))
    sprites.append(newPlayerImg)
class advanceMap(threading.Thread):
    def __init__(self,i):
        threading.Thread.__init__(self)
        self.m = i
        #print(i)
        global spaces
    def run(self,j):
        #print(i)
        i = self.m
        global moneyr
        global moneyb
        global whilecount
        global data
        global datachange
        if j == 0:
            for y in range(0,spaces):
                counter = 0
                check = True
                if dataprev[i][y] > 0 and dataprev[i][y]<3:
                    if i != spaces-1:
                        if random.randint(0,1)==True and datachange[i+1][y]!= dataprev[i][y]:
                            if datachange[i+1][y]>=3 and datachange[i+1][y]!=6:
                                if datachange[i+1][y]==7:
                                    datachange[i+1][y]=dataprev[i][y]
                                    data[i+1][y]= dataprev[i][y]
                                    if dataprev[i][y] == 1:
                                        moneyr +=100
                                    else:
                                        moneyb +=100
                                else:
                                    datachange[i+1][y] +=1
                            else:
                                datachange[i+1][y]= dataprev[i][y]
                                data[i+1][y]= dataprev[i][y]
                            check = False
                        if datachange[i+1][y]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                    if i != 0 :
                        if random.randint(0,1)==True and datachange[i-1][y]!= dataprev[i][y] and check:
                            if datachange[i-1][y]>=3 and datachange[i-1][y]!=6:
                                if datachange[i-1][y]==7:
                                    datachange[i-1][y]=dataprev[i][y]
                                    data[i-1][y]= dataprev[i][y]
                                    if dataprev[i][y] == 1:
                                        moneyr +=100
                                    else:
                                        moneyb +=100
                                else:
                                    datachange[i-1][y] +=1
                            else:
                                datachange[i-1][y]= dataprev[i][y]
                                data[i-1][y]= dataprev[i][y]
                            check = False
                        if datachange[i-1][y]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                    if y != spaces-1 :
                        if random.randint(0,1)==True and datachange[i][y+1]!= dataprev[i][y] and check:
                            if datachange[i][y+1]>=3 and datachange[i][y+1]!=6:
                                if datachange[i][y+1]==7:
                                    datachange[i][y+1]=dataprev[i][y]
                                    data[i][y+1]= dataprev[i][y]
                                    if dataprev[i][y] == 1:
                                        moneyr +=100
                                    else:
                                        moneyb +=100
                                else:
                                    datachange[i][y+1] +=1
                            else:
                                datachange[i][y+1]= dataprev[i][y]
                                data[i][y+1]= dataprev[i][y]
                            check = False
                        if datachange[i][y+1]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                    if y != 0 :
                        if random.randint(0,1)==True and datachange[i][y-1]!= dataprev[i][y] and check:
                            if datachange[i][y-1]>=3 and datachange[i][y-1]!=6:
                                if datachange[i][y-1]==7:
                                    datachange[i][y-1]=dataprev[i][y]
                                    data[i][y-1]= dataprev[i][y]
                                    if dataprev[i][y] == 1:
                                        moneyr +=100
                                    else:
                                        moneyb +=100
                                else:
                                    datachange[i][y-1] +=1
                            else:
                                datachange[i][y-1]= dataprev[i][y]
                                data[i][y-1]= dataprev[i][y]
                            check = False
                        if datachange[i][y-1]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                if counter == 4:
                    data[i][y]=0
        else:
            for y in range(spaces-1,0,-1):
                counter = 0
                check = True
                if dataprev[i][y] > 0 and dataprev[i][y]<3:
                    if i != spaces-1:
                        if random.randint(0,1)==True and datachange[i+1][y]!= dataprev[i][y]:
                            if datachange[i+1][y]>=3 and datachange[i+1][y]!=6:
                                if datachange[i+1][y]==7:
                                    datachange[i+1][y]=dataprev[i][y]
                                    data[i+1][y]= dataprev[i][y]
                                    if dataprev[i][y] == 1:
                                        moneyr +=100
                                    else:
                                        moneyb +=100
                                else:
                                    datachange[i+1][y] +=1
                            else:
                                datachange[i+1][y]= dataprev[i][y]
                                data[i+1][y]= dataprev[i][y]
                            check = False
                        if datachange[i+1][y]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                    if i != 0 :
                        if random.randint(0,1)==True and datachange[i-1][y]!= dataprev[i][y] and check:
                            if datachange[i-1][y]>=3 and datachange[i-1][y]!=6:
                                if datachange[i-1][y]==7:
                                    datachange[i-1][y]=dataprev[i][y]
                                    data[i-1][y]= dataprev[i][y]
                                    if dataprev[i][y] == 1:
                                        moneyr +=100
                                    else:
                                        moneyb +=100
                                else:
                                    datachange[i-1][y] +=1
                            else:
                                datachange[i-1][y]= dataprev[i][y]
                                data[i-1][y]= dataprev[i][y]
                            check = False
                        if datachange[i-1][y]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                    if y != spaces-1 :
                        if random.randint(0,1)==True and datachange[i][y+1]!= dataprev[i][y] and check:
                            if datachange[i][y+1]>=3 and datachange[i][y+1]!=6:
                                if datachange[i][y+1]==7:
                                    datachange[i][y+1]=dataprev[i][y]
                                    data[i][y+1]= dataprev[i][y]
                                    if dataprev[i][y] == 1:
                                        moneyr +=100
                                    else:
                                        moneyb +=100
                                else:
                                    datachange[i][y+1] +=1
                            else:
                                datachange[i][y+1]= dataprev[i][y]
                                data[i][y+1]= dataprev[i][y]
                            check = False
                        if datachange[i][y+1]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                    if y != 0 :
                        if random.randint(0,1)==True and datachange[i][y-1]!= dataprev[i][y] and check:
                            if datachange[i][y-1]>=3 and datachange[i][y-1]!=6:
                                if datachange[i][y-1]==7:
                                    datachange[i][y-1]=dataprev[i][y]
                                    data[i][y-1]= dataprev[i][y]
                                    if dataprev[i][y] == 1:
                                        moneyr +=100
                                    else:
                                        moneyb +=100
                                else:
                                    datachange[i][y-1] +=1
                            else:
                                datachange[i][y-1]= dataprev[i][y]
                                data[i][y-1]= dataprev[i][y]
                            check = False
                        if datachange[i][y-1]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                if counter == 4:
                    data[i][y]=0
        whilecount+= 1
    def checa():
        for y in range(0,spaces):
            if data[i][y]!= spaces:
                if data[i][y]== data[i+1][y]:
                    data
def player(id,a,b):
    screen.blit(sprites[id-1],(a,b))
arr = []
for i in range(0,spaces):
    arr.append(advanceMap(i))
#GameLoops
running = True
counta = 0
countb = 0
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)
textsurface = myfont.render("Hello my name is minecraft steve", False, (250, 250, 250))
while running:
    data = copy.deepcopy(datachange)
    dataprev = copy.deepcopy(data)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if random.randint(0,1)==True:
        counta +=1
        for x in range(0,spaces):
            arr[x].run(0)
    else:
        countb +=1
        for x in (range(spaces-1,0,-1)):
            arr[x].run(1)
    contr = 0
    contb = 0
    while(whilecount < spaces-1):
        print("yo",whilecount)
    whilecount = 0
    screen.fill((0,0,0))
    for i in range(0,spaces):
        for y in range(0,spaces):
            if datachange[i][y] ==1:
                contr += 1
            elif datachange[i][y] == 2:
                contb += 1
            if datachange[i][y] !=0:
                player(datachange[i][y],i*sizex/spaces,y*sizey/spaces)
    #time.sleep(.1)
    #for i in range(0,spaces):
            #print(data[i])
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
            moneyb, moneyr = 0 ,0
        if event.key == pygame.K_KP_1:
            if moneyr>=300:
                #print("my boi")
                moneyr -=300
    moneyr +=3
    moneyb +=3

    textsurface = myfont.render(f"Seed: {newseed} Red: {moneyr} Blue: {moneyb}", False, (250, 250, 250))       
    screen.blit(textsurface,(0,sizey+10))
    if spaces<100:
        time.sleep(0.1)
    pygame.display.update()
    
    