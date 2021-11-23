from operator import countOf, truediv
import os,pygame,time,random,copy, math, threading
import perlin
from pygame import math

pygame.init()
spaces = 150
data = [[0] *spaces for _ in range(spaces)]
dataprev = copy.deepcopy(data)
datachange = copy.deepcopy(data)
newseed = 10
whilecount = 0
moneyr,moneyb = 0,0
oct1,oct2 = 5,1.5
#mapFunct
wallprob = 1
sprites = []
noise = []
def newseeder():
    global newseed
    global noise
    newseed = random.randrange(0,10000)
    noise = perlin.perlin(newseed)
    noise.two_octave(1,1)
    noise = perlin.perlin(newseed)
    
def generateMap():
    global newseed
    global data
    global datachange
    global noise
    check = 0
    arr = [[0]*spaces for _ in range(spaces)]
    #newseed = 9567
    #3print(newseed)    

    for i in range(0,spaces):
        for y in range(0,spaces):
            #print(noise.two(i,y))
            #print(noise.two(i,y))
            if noise.two(i,y) >oct1 or noise.two(i,y) <-oct1:
                arr[i][y] = 1
            if noise.two(i,y)>oct1*oct2 or noise.two(i,y) <-(oct1*oct2):
                arr[i][y] = 7
                check += 1
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
newseeder()
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
    def checa():
        for y in range(0,spaces):
            if data[i][y]!= spaces:
                if data[i][y]== data[i+1][y]:
                    data
def player(id,a,b):
    screen.blit(sprites[id-1],(a,b))
arr = []

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
    contr = 0
    contb = 0
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
    if event.type == pygame.KEYDOWN:
        # Check for backspace
        if event.key == pygame.K_BACKSPACE:
            print("reload")
            newseeder()
            clearData()
            screen.fill((0,0,0))
            moneyb, moneyr = 0 ,0
        if event.key == pygame.K_KP_1:
            oct1+=1
            print("yo")
            clearData()
        if event.key == pygame.K_KP_2:
            print("t")
            oct2+=.1
            clearData()
        if event.key == pygame.K_KP_4:
            print("c")
            oct1-=1
            clearData()
        if event.key == pygame.K_KP_5:
            print("o")
            oct2-=.1
            clearData()
        if event.key == pygame.K_KP_3:
            print("f")
            newseed +=100
            clearData()
        if event.key == pygame.K_KP_6:
            print("fak")
            newseed -=100
            clearData()

    textsurface = myfont.render(f"Seed: {newseed} check1: {oct1} check2: {oct2}", False, (250, 250, 250))       
    screen.blit(textsurface,(0,sizey+10))
    if spaces<100:
        time.sleep(0.1)
    pygame.display.update()
    
    