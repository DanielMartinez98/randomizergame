from operator import countOf, truediv
import os,pygame,time,random,copy, math, threading
import perlin
from pygame import math

pygame.init()
moneyr,moneyb,counta,countb,bankr,bankb,powerr,powerb,whilecount,newseed,wallprob,spaces,winner = 0,0,0,0,0,0,0,0,0,0,1,90,0
sprites = []
data = [[0] *spaces for _ in range(spaces)]
items,dataprev,datachange = copy.deepcopy(data),copy.deepcopy(data),copy.deepcopy(data)

#generate the map and place walls and money
def generateMap():
    global newseed
    check = 0
    arr = [[0]*spaces for _ in range(spaces)]
    newseed = random.randrange(0,10000)
    #newseed = 9567
    #3print(newseed)    
    noise = perlin.perlin(newseed)
    noise.two_octave(1,1)
    noise = perlin.perlin(newseed)
    if noise.two(0,0)>wallprob or noise.two(spaces-1,spaces-1)>wallprob or (noise.two(0,0)<-wallprob or noise.two(spaces-1,spaces-1)<-wallprob):
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
#reloads the map and adds all the info into the data array        
def clearData():
    global data
    global datachange
    global noise_data 
    global dataprev
    global items
    noise_data = generateMap()
    data = [[0]*spaces for _ in range(spaces)]
    dataprev = copy.deepcopy(data)
    items = copy.deepcopy(data)
    datachange = copy.deepcopy(data)
    for i in range(0,spaces):
        for y in range(0,spaces):
            if noise_data[i][y]==1:
                data[i][y] = 3
                datachange[i][y] = 3
            elif noise_data[i][y]==7:
                data[i][y] = 7
                datachange[i][y] = 7
    datachange[0][0] = 1
    datachange[spaces-1][spaces-1] =2
#places randomly the item that was purchised from the store number1 = team, number2 = type of building
def placeItem(number1,number2):
    global spaces
    global datachange
    global items
    global data
    global contr
    global contb
    value = 0
    check = False
    if number1 == 1:
        print(contr/3000)
        value = contr
        for i in range(0,spaces):
            for y in range(0,spaces):
                if data[i][y] == 1:  
                    if items[i][y] == 0:
                        if random.randint(0,value)<=1:
                            print(contr,value)
                            items[i][y] = number2
                            check = True
                            break
                        else:
                            value-=1
                    else:
                        value-=1
            if check:
                break
    else:
        counter =0 
        value = contb
        for i in range(spaces-1,0,-1):
            for y in range(spaces-1,0,-1):
                if data[i][y] == 2:
                    if items[i][y] == 0:
                        if random.randint(0,value)<=1:
                            print(contb,value)
                            items[i][y] = number2
                            check = True
                            break
                        else:
                            #print(contb,value)
                            value-=1
                    else:
                        #print(contb,value)
                        value-=1
                counter+=1
            if check:
                break
    if not check:
        placeItem(number1,number2)
clearData()
#print(noise_data)
sizex,sizey, id,pth = 1000,1000, 1, os.path.dirname(__file__)
screen = pygame.display.set_mode((sizex,sizey+50))
#Title and Icon
pygame.display.set_caption("COCA Vs Bepis")
icon = pygame.image.load(pth+'\\assets\\'+str(id)+'.png')
pygame.display.set_icon(icon)
#Restablishes the size of each sprite depending on the ammount of spaces
def resetsprites():
    global sprites
    global spaces
    global sizex
    global sizey
    sprites = []
    for i in range(1,11):
        playerImg = pygame.image.load(pth+'\\assets\\'+str(i)+'.png')
        newPlayerImg = pygame.transform.scale(playerImg,(sizex/spaces+1,sizey/spaces+1))
        sprites.append(newPlayerImg)
#class made to make the proces of checking locations multithreaded,"in theory it could be replaced "
class advanceMap(threading.Thread):
    def __init__(self,i):
        threading.Thread.__init__(self)
        self.m = i
        #print(i)
    def run(self,j):
        #print(i)
        i = self.m
        global spaces
        global moneyr
        global moneyb
        global whilecount
        global data
        global datachange
        global items
        #checks to see if the value will load the screen from 0,0 to spaces,spaces or backwards
        if j == 0:
            for y in range(0,spaces):
                #counts the amount of options on each side of each object to see if it deserves to keep getting checkeds
                counter = 0
                #checks if the item has already chosen a side to move towards, meaning each block can only expand in one direction per round
                check = True
                #checks to see if the value of the position is capable of moving.
                if dataprev[i][y] > 0 and dataprev[i][y]<3:
                    #  all the sections bellow are the same only checking different values so i will only document this on the first one
                    #checks if the item is at the right most position of the screen if so it skips this part
                    if i != spaces-1:
                        #checks if the block is lucky enough to advance and if so it checks that the value its trying to replace is not already equal to the new value
                        if (random.randint(0,100)<=49+powerr and dataprev[i][y]==1)or(random.randint(0,100)<=49+powerb and dataprev[i][y]==2) and datachange[i+1][y]!= dataprev[i][y]:
                            #checks to see if the position it is trying to replace is a wall
                            if datachange[i+1][y]>=3 and datachange[i+1][y]!=6:
                                #checks to see if the position contains a gold piece
                                if datachange[i+1][y]==7:
                                    #replaces the gold piece and deposits money on the players account
                                    datachange[i+1][y]=dataprev[i][y]
                                    data[i+1][y]= dataprev[i][y]
                                    if dataprev[i][y] == 1:
                                        moneyr +=100
                                    else:
                                        moneyb +=100
                                else:
                                    #it weakens the wall
                                    datachange[i+1][y] +=1
                            else:
                                #it replaces the position with the team value 
                                datachange[i+1][y]= dataprev[i][y]
                                #checks to see if the position that is being replaced is from the other team if so it replaces its itemposition to 0
                                if (datachange[i+1][y] ==1 and dataprev[i+1][y]==2) or (datachange[i+1][y] ==2 and dataprev[i+1][y]==1):
                                    items[i+1][y]=0
                                data[i+1][y]= dataprev[i][y]
                            #prevents other sides from checking themselves
                            check = False
                        #it checks if the value is changed if so it adds to the counter so that the computer know that this side no longer needs to be computed
                        if datachange[i+1][y]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                    if i != 0 :
                        if (random.randint(0,100)<=49+powerr and dataprev[i][y]==1)or(random.randint(0,100)<=49+powerb and dataprev[i][y]==2) and datachange[i-1][y]!= dataprev[i][y] and check:
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
                                if (datachange[i-1][y] ==1 and dataprev[i-1][y]==2) or (datachange[i-1][y] ==2 and dataprev[i-1][y]==1):
                                    items[i-1][y]=0
                                data[i-1][y]= dataprev[i][y]
                            check = False
                        if datachange[i-1][y]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                    if y != spaces-1 :
                        if (random.randint(0,100)<=49+powerr and dataprev[i][y]==1)or(random.randint(0,100)<=49+powerb and dataprev[i][y]==2) and datachange[i][y+1]!= dataprev[i][y] and check:
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
                                if (datachange[i][y+1] ==1 and dataprev[i][y+1]==2) or (datachange[i][y+1] ==2 and dataprev[i][y+1]==1):
                                    items[i][y+1]=0
                                data[i][y+1]= dataprev[i][y]
                            check = False
                        if datachange[i][y+1]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                    if y != 0 :
                        if (random.randint(0,100)<=49+powerr and dataprev[i][y]==1)or(random.randint(0,100)<=49+powerb and dataprev[i][y]==2) and datachange[i][y-1]!= dataprev[i][y] and check:
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
                                if (datachange[i][y-1] ==1 and dataprev[i][y-1]==2) or (datachange[i][y-1] ==2 and dataprev[i][y-1]==1):
                                    items[i][y-1]=0
                                data[i][y-1]= dataprev[i][y]
                            check = False
                        if datachange[i][y-1]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                #if the counter is equal to 4 it removes this object from being checked again unitl one side is liberated
                if counter == 4:
                    data[i][y]=0
        else:
            #same as the top version but backwards
            for y in range(spaces-1,0,-1):
                counter = 0
                check = True
                if dataprev[i][y] > 0 and dataprev[i][y]<3:
                    if i != 0 :
                        if (random.randint(0,100)<=49+powerr and dataprev[i][y]==1)or(random.randint(0,100)<=49+powerb and dataprev[i][y]==2) and datachange[i-1][y]!= dataprev[i][y] and check:
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
                                if (datachange[i-1][y] ==1 and dataprev[i-1][y]==2) or (datachange[i-1][y] ==2 and dataprev[i-1][y]==1):
                                    items[i-1][y]=0
                                data[i-1][y]= dataprev[i][y]
                            check = False
                        if datachange[i-1][y]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                    if i != spaces-1:
                        if (random.randint(0,100)<=49+powerr and dataprev[i][y]==1)or(random.randint(0,100)<=49+powerb and dataprev[i][y]==2) and datachange[i+1][y]!= dataprev[i][y]:
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
                                if (datachange[i+1][y] ==1 and dataprev[i+1][y]==2) or (datachange[i+1][y] ==2 and dataprev[i+1][y]==1):
                                    items[i+1][y]=0
                                data[i+1][y]= dataprev[i][y]
                            check = False
                        if datachange[i+1][y]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                    if y != 0 :
                        if (random.randint(0,100)<=49+powerr and dataprev[i][y]==1)or(random.randint(0,100)<=49+powerb and dataprev[i][y]==2) and datachange[i][y-1]!= dataprev[i][y] and check:
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
                                if (datachange[i][y-1] ==1 and dataprev[i][y-1]==2) or (datachange[i][y-1] ==2 and dataprev[i][y-1]==1):
                                    items[i][y-1]=0
                                data[i][y-1]= dataprev[i][y]
                            check = False
                        if datachange[i][y-1]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                if counter == 4:
                    data[i][y]=0
                    if y != spaces-1 :
                        if (random.randint(0,100)<=49+powerr and dataprev[i][y]==1)or(random.randint(0,100)<=49+powerb and dataprev[i][y]==2) and datachange[i][y+1]!= dataprev[i][y] and check:
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
                                if (datachange[i][y+1] ==1 and dataprev[i][y+1]==2) or (datachange[i][y+1] ==2 and dataprev[i][y+1]==1):
                                    items[i][y+1]=0
                                data[i][y+1]= dataprev[i][y]
                            check = False
                        if datachange[i][y+1]==datachange[i][y]:
                            counter+=1
                    else: counter+=1
                if counter == 4:
                    data[i][y]=0
        whilecount+= 1
#serves as basis to all sprites
def player(id,a,b):
    screen.blit(sprites[id-1],(a,b))
#sets up the array that contains the threads that manage the whole game
def setArr():
    global arr
    arr = []
    for i in range(0,spaces):
        arr.append(advanceMap(i))
setArr()
#GameLoop setters
running = True
runningmenu = True
#text setup
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)
textsurface = myfont.render("Hello my name is minecraft steve", False, (250, 250, 250))
#loop that allows the main menu to exist
def menu():
    global runningmenu
    global running
    global moneyr
    global moneyb
    global spaces
    global winner
    active = False
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    user_text = "90"
    base_font = pygame.font.Font(None, 32)
    input_rect = pygame.Rect(sizex/4, 200, sizex/2-30, 32)
    runningmenu = True
    while runningmenu:
        #text
        if winner>0:
            if winner ==1:
                textsurface = myfont.render(f"Red Team Won", False, (250, 0, 0))       
            else:
                textsurface = myfont.render(f"Blue Team Won", False, (0, 0, 250))     
            screen.blit(textsurface,(sizex/2-100,100))
            
        textsurface = myfont.render(f"Menu", False, (250, 250, 250))       
        screen.blit(textsurface,(sizex/2-50,10))
        textsurface = myfont.render(f"Instructions", False, (250, 250, 250))       
        screen.blit(textsurface,(sizex/2-80,250))
        textsurface = myfont.render(f"player 1:", False, (250, 250, 250))       
        screen.blit(textsurface,(sizex/4,300))
        textsurface = myfont.render(f"place banks a", False, (250, 250, 250))       
        screen.blit(textsurface,(sizex/4,350))
        textsurface = myfont.render(f"place power units s", False, (250, 250, 250))       
        screen.blit(textsurface,(sizex/4,400))
        textsurface = myfont.render(f"player 2:", False, (250, 250, 250))       
        screen.blit(textsurface,(sizex/2+80,300))
        textsurface = myfont.render(f"place banks k", False, (250, 250, 250))       
        screen.blit(textsurface,(sizex/2+80,350))
        textsurface = myfont.render(f"place power units l", False, (250, 250, 250))       
        screen.blit(textsurface,(sizex/2+80,400))
        textsurface = myfont.render(f"press enter to play", False, (250, 250, 250))       
        screen.blit(textsurface,(sizex/4,500))
        pygame.draw.rect(screen, color, input_rect)
        textsurface = myfont.render(f"Size", False, (250, 250, 250))       
        screen.blit(textsurface,(sizex/2-50,150))
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        # render at position stated in arguments
        screen.blit(text_surface, (input_rect.x, input_rect.y+5))
        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(sizex/2-30, text_surface.get_width()+10)
        # display.flip() will update only a portion of the
        # screen to updated, not full area
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningmenu = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    print("wassap")
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_RETURN:
                    winner = 0
                    # Check for backspace
                    runningmenu= False
                    try:
                        if int(user_text)>=10:
                            spaces = int(user_text)
                            resetsprites()
                            clearData()
                            setArr()
                    except:
                        print("lol")
                    screen.fill((0,0,0))
                    moneyb, moneyr = 0 ,0
                # Check for backspace
                elif active: 
                    if event.key == pygame.K_BACKSPACE:
                        # get text input from 0 to -1 i.e. end.
                        user_text = user_text[:-1]
                        # Unicode standard is used for string
                        # formation
                    else:
                        user_text += event.unicode
                        try:
                            int(user_text)
                        except ValueError:
                            user_text = user_text[:-1]
        pygame.display.flip()
        pygame.display.update()
resetsprites()
menu()
#game
while running:
    #restablishes data and dataprev
    data = copy.deepcopy(datachange)
    dataprev = copy.deepcopy(data)
    #start the loop on the order depending on luck and runs the threads to advance the map by one round
    if random.randint(0,1)==True:
        for x in range(0,spaces):
            if random.randint(0,1)==True: arr[x].run(0)
            else: arr[x].run(1)
    else:
        for x in (range(spaces-1,0,-1)):
            if random.randint(0,1)==True: arr[x].run(0)
            else: arr[x].run(1)
    #sets screen to black
    screen.fill((0,0,0))
    #setters
    bankb,bankr,powerr,powerb,whilecount,contr,contb = 0,0,0,0,0,0,0
    #prints all the new values that where generated
    for i in range(0,spaces):
        for y in range(0,spaces):
            #counts the amount of apearances of each team
            if datachange[i][y] ==1:
                contr += 1
            elif datachange[i][y] == 2:
                contb += 1
            #finds the changes and prints them on screen
            if datachange[i][y] !=0:
                player(datachange[i][y],i*sizex/spaces,y*sizey/spaces)
                if datachange[i][y] ==1:
                    if items[i][y] == 1:
                        player(9,i*sizex/spaces,y*sizey/spaces)
                        bankr+=1
                    elif items[i][y]==2:
                        player(8,i*sizex/spaces,y*sizey/spaces)
                        powerr +=1
                elif datachange[i][y] ==2:
                    if items[i][y] == 1:
                        player(9,i*sizex/spaces,y*sizey/spaces)
                        bankb+=1
                    elif items[i][y]==2:
                        player(8,i*sizex/spaces,y*sizey/spaces)
                        powerb +=1
    #money that is generated for each team per round
    moneyr +=3+bankr*3
    moneyb +=3+bankb*3
    #inputs of the player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Check for backspace
            if event.key == pygame.K_BACKSPACE:
                clearData()
                screen.fill((0,0,0))
                moneyb, moneyr = 0 ,0
            if event.key == pygame.K_a:
                if moneyr>=10000:
                    #bank red
                    print("bank red")
                    placeItem(1,1)
                    moneyr -=10000
            if event.key == pygame.K_s:
                if moneyb>=5000:
                    #bank blue
                    print("power red")
                    placeItem(1,2)
                    moneyb -=5000
            if event.key == pygame.K_k:
                if moneyr>=10000:
                    #power red
                    print("bank blue")
                    placeItem(2,1)
                    moneyr -=10000
            if event.key == pygame.K_l:
                if moneyb>=5000:
                    #power blue
                    print("power blue")
                    placeItem(2,2)
                    moneyb -=5000
            if event.key == pygame.K_ESCAPE:
                screen.fill((0,0,0))
                menu()
                clearData()
                moneyb, moneyr = 0 ,0
    #checks if one player has won the game
    if contr ==0 or contb ==0:
        if contr == 0:
            winner = 2
            screen.fill((0,0,0))
            menu()
            clearData()
        else:
            winner = 1
            screen.fill((0,0,0))
            menu()
            clearData()
    #sets up bottom text with information for the players       
    textsurface = myfont.render(f"Red: money={moneyr} power={powerr} banks = {bankr} Blue: money={moneyb} power={powerb} banks = {bankb}", False, (250, 250, 250))       
    screen.blit(textsurface,(0,sizey+10))
    #if the map is too small it adds a small delay
    if spaces<100:
        time.sleep(.01)
    #updates the pygame screen
    pygame.display.update()
    
    