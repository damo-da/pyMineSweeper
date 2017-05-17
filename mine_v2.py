######################################################################################################
##########################            MINESWEEPER         ############################################
######################################################################################################

########################
#game initialization
########################
import random,sys,time,pygame
from pygame.locals import *
pygame.init()
pygame.key.set_repeat(400,60)
pygame.display.set_caption("Minesweeper")
Clock=pygame.time.Clock()


##################################
#Change these variables as you want
###################################

HighLightBord=5
FPS=20
FontSize=30
GAMEBGCOLOR=(0,0,0)
TEXTCOLOR=(0,0,0)
WHITE=(255,255,255)
BLACK=(0,0,0)
xGap=3
yGap=3
fullscreen=0
#fullscreen=pygame.FULLSCREEN         #remove the hash to make it full screen



###########################
#images
###########################

BombPic = pygame.image.load('images/'+"Bomb.png")
BoxPic = pygame.image.load('images/'+"Box.png")
HBoxPic=pygame.image.load('images/'+"HighlightBox.png")
FlagPic = pygame.image.load('images/'+"Flag.png")
UnminedPic = pygame.image.load('images/'+"Unmined.png")
CrossFlagPic = pygame.image.load('images/'+"CrossFlag.png")
CrushPic = pygame.image.load('images/'+"Crush.PNG")
BackgroundPic = pygame.image.load('images/'+"BG.jpg")
MineCountPic=[]
for i in range(0,9):
    Image=pygame.image.load('images/'+str(i)+".png")
    MineCountPic.append(Image)


###########################
#Functions are here
###########################





################################
#function to reset the game
################################
Display=1
Mines=0
def reset():
    Board=[]
    Mine=[]
    for i in range(0,MapHeight):
        Board.append([])
        Mine.append([])
        for j in range(0,MapWidth):
            Board[i].append(0)
            Mine[i].append(0)

    #fill mined
    x=0
    while x<MinesCount:
        c=[random.randint(0,MapHeight-1),random.randint(0,MapWidth-1)]
        if Mine[c[0]][c[1]]==0:
            x+=1
            Mine[c[0]][c[1]]=-1

    #create numbers
    for i in range(0,MapHeight):
        for j in range(0,MapWidth):
            if Mine[i][j]==-1:
                continue
            Num=0
            if i!=0:
                if j!=0 and Mine[i-1][j-1]==-1:             #top left
                    Num+=1
                if j!=MapWidth-1 and Mine[i-1][j+1]==-1:    #top right
                    Num+=1
                if Mine[i-1][j]==-1:                        #top vertical
                    Num+=1
            if i!=MapHeight-1:
                if j!=0 and Mine[i+1][j-1]==-1:             #down left
                    Num+=1
                if j!=MapWidth-1 and Mine[i+1][j+1]==-1:    #down right
                    Num+=1
                if Mine[i+1][j]==-1:                        #down vertical
                    Num+=1

            if j!=0 and Mine[i][j-1]==-1:
                Num+=1
            if j!=MapWidth-1 and Mine[i][j+1]==-1:
                Num+=1
            Mine[i][j]=Num
    return [Mine,Board]

####################
#Disply on screen
####################
def PrintScreen(Death=False):
    #GameScreen.fill(GAMEBGCOLOR)
    ObjRect=pygame.Rect(0,0,GameWidth,GameHeight)
    GameScreen.blit(Background,ObjRect)
    
    #create an array of data of all images to be printed
    Images=[]
    for i in range(0,MapHeight):
        Images.append([])
        for j in range(0,MapWidth):
            Data=UnminedImage
            #if death
                #if the cell is mine,
                    #if flagged,
                        #data=flag
                    #if not flagged,
                        #data=bomb
                    #if hboxpos=this cell,
                        #print crush
                #if the cell is not mine,
                        #if flagged,
                            #print crossflag
                        #if not flagged,
                            #print number
            #else:
                #if not visible=-1,
                    #print flag
                #if visible=0,
                    #print null
                #if visible=1,
                    #print the number

            if Death:
                if Game[Mines][i][j]==-1:
                    if Game[Display][i][j]==-1:
                        Data=FlagImage
                    else:
                        Data=BombImage
                    if HBoxPos==[i,j]:
                        Data=CrushImage
                else:
                    if Game[Display][i][j]==-1:
                        Data=CrossImage
                    elif Game[Display][i][j]==1:
                        Data=MineCountImage[Game[Mines][i][j]]
            else:
                if Game[Display][i][j]==-1:
                    Data=FlagImage
                elif Game[Display][i][j]==1:
                    Data=MineCountImage[Game[Mines][i][j]]
            Images[i].append(Data)

    for i in range(0,MapHeight):
        topC=round((i+0.5)*yGap+i*BoxSize[1])
        for j in range(0,MapWidth):
            leftC=round((j+0.5)*xGap+j*BoxSize[0])
            ObjRect=pygame.Rect(leftC,topC,yGap,xGap)
            GameScreen.blit(Images[i][j],ObjRect)
    if not Death:
        #print the select box
        leftC=(HBoxPos[1]+0.5)*xGap+HBoxPos[1]*BoxSize[1]-HighLightBord
        topC=(HBoxPos[0]+0.5)*yGap+HBoxPos[0]*BoxSize[0]-HighLightBord
        Rect=pygame.Rect(leftC,topC,BoxSize[1]+HighLightBord*2,BoxSize[0]+HighLightBord*2)
        if HITPRESSED:
            GameScreen.blit(HBoxImage,Rect)
        else:
            GameScreen.blit(BoxImage,Rect)
    pygame.display.update()


#####################################
#The function to handle the game exit
#####################################
def ExitGame():
    #print my face
    mode=(500,500)
    pygame.display.set_mode(mode,fullscreen,32)
    GREEN=(0,255,0)
    GameScreen.fill(GREEN)
    GameScreen.blit(pygame.transform.scale(pygame.image.load('images/'+"DAM.jpg"),mode),pygame.Rect(0,0,mode[0],mode[1]))
    Font=pygame.font.SysFont("Verdana",25,False,False)
    Text=Font.render("Dam Underscore",True,GREEN,BLACK)
    TextRect=Text.get_rect()
    TextRect.left=0
    TextRect.top=0
    GameScreen.blit(Text,TextRect)
    pygame.display.update()
    time.sleep(4)
    pygame.quit()
    sys.exit()


######################################
#the function to take input from the user
#######################################
def RequestedMove():
    while True:
        Clock.tick(FPS)
        for i in pygame.event.get():
            if i.type==QUIT:
                ExitGame()
            if i.type==KEYUP:
                if i.key==K_ESCAPE:
                    return[0,False,True]
                if i.key==K_SPACE:
                    return [5,False,False]
            if i.type==KEYDOWN:
                if i.key==K_DOWN:
                    return [8,HITPRESSED,False]
                if i.key==K_UP:
                    return [2,HITPRESSED,False]
                if i.key==K_LEFT:
                    return [4,HITPRESSED,False]
                if i.key==K_RIGHT:
                    return [6,HITPRESSED,False]
                if i.key==K_SPACE:
                    return [0,True,False]
                if i.key==ord('z') or i.key==ord('Z'):
                    return [-1,HITPRESSED,False]

#########################################################
#returns true if all the mines are found, ie. game won
########################################################
def FoundAllMines():
    #if no of 1 in game[display]+minescount=mapheight*mapwidth, game won
    FCount=0
    for i in range(0,MapHeight):
        for j in range(0,MapWidth):
            if Game[Display][i][j]==1:
                FCount+=1

    if FCount+MinesCount>=MapHeight*MapWidth:
        return True
    else:
        return False

###############################################
#Gameover interface
    ###########################################
def GameOver(state="lose"):
    if state=="lose":
        Death=True
    else:
        Death=False
    PrintScreen(Death)
    RequestedMove()
    GameScreen.blit(Background,(0,0,MapWidth,MapHeight))
    if state.lower()=="win":
        msg="You won the game"
    else:
        msg="You lose"
    Text=GameFont.render(msg,True,TEXTCOLOR)
    TextRect=Text.get_rect()
    TextRect.centerx=round(GameWidth/2)
    TextRect.centery=round(GameHeight/2)
    GameScreen.blit(Text,TextRect)
    pygame.display.update()
    time.sleep(1)
    #ExitGame()

###############################################################
#sets visible to 0 mines touching boxes and their adjacents
###############################################################
def SetVisible():
    Moves=[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
    X=Game[Display]
    while True:
        Changed=False
        #get all the visible fields
        Visible=[]
        for i in range(0,MapHeight):
             for j in range(0,MapWidth):
                 if X[i][j]==1:
                     Visible.append([i,j])
        #make boxes visible, attached to the visible[] and has mine=0
        for a in range(len(Visible)):
            for b in range(len(Moves)):
                NextCell=[Visible[a][0]+Moves[b][0],Visible[a][1]+Moves[b][1]]
                if NextCell[0]<MapHeight and NextCell[1]<MapWidth and NextCell[0]>=0 and NextCell[1]>=0:
                    if Game[Mines][NextCell[0]][NextCell[1]]==0 and X[NextCell[0]][NextCell[1]]==0:
                        X[NextCell[0]][NextCell[1]]=1
                        Changed=True
        
        if not Changed:
            break
    #make the numbers to appear after blank spaces are revealed
    while True:
        Changed=False
        blanks=[]
        for i in range(0,MapHeight):
            for j in range(0,MapWidth):
                if X[i][j]==1 and Game[Mines][i][j]==0:
                    blanks.append([i,j])
        for a in range(len(blanks)):
            for b in range(len(Moves)):
                NextCell=[blanks[a][0]+Moves[b][0],blanks[a][1]+Moves[b][1]]
                if NextCell[0]<MapHeight and NextCell[1]<MapWidth and NextCell[0]>=0 and NextCell[1]>=0:
                    if X[NextCell[0]][NextCell[1]]==0:
                        X[NextCell[0]][NextCell[1]]=1
                        Changed=True
        if not Changed:
            break
    return X

#############################################
#Main menu
#############################################
def Menu():
    pygame.display.set_mode((400,400),fullscreen,32)
    while True:
        Menus=[]
        Menus.append("Easy")
        Menus.append("Medium")
        Menus.append("Hard")
        Menus.append("Exit Game")

        Key=0
        ret=False
        while True:
            MenuPrint(Menus,Key)
            x=pygame.event.wait()
            if x.type==QUIT:
                ExitGame()
            elif x.type==KEYUP:
                if x.key==K_SPACE:
                    ret=True
                    break
                elif x.key==K_ESCAPE:
                    ExitGame()
            elif x.type==KEYDOWN:
                    if x.key==K_UP:
                        Key-=1
                    elif x.key==K_DOWN:
                        Key+=1
            if ret:
                break
            if Key<0:
                Key=len(Menus)-1
            elif Key==len(Menus):
                Key=0
            time.sleep(0.1)
        #key has the option
        if Key==0:#new game
            return [5,5,3,220,220,(40,40)]
        elif Key==1:
            return [10,10,20,432,432,(40,40)]
        elif Key==2:
            return [20,20,80,663,663,(30,30)]
        elif Key==3:
            ExitGame()

################################
#main menu printer
################################
def MenuPrint(Menus,key):
    GameScreen.fill(WHITE)
    for i in range(len(Menus)):
        if i !=key:
            text=GameFont.render(Menus[i],True,BLACK,WHITE)
        else:
            text=GameFont.render(Menus[i],True,WHITE,BLACK)
        textRect=text.get_rect()
        textRect.top=i*50
        textRect.left=0
        GameScreen.blit(text,textRect)
        pygame.display.update()


#
#
#
#
#
#
##############################################
#The code of the game
##############################################


GameFont=pygame.font.SysFont(None,FontSize)
while True:
    GameScreen=pygame.display.set_mode((400,500),fullscreen,32)
    MapHeight,MapWidth,MinesCount,GameHeight,GameWidth,BoxSize=Menu()
    pygame.display.set_mode((GameWidth,GameHeight),fullscreen,32)
    #xGap=round((GameWidth-MapWidth*BoxSize[0])/MapWidth)
    #yGap=round((GameHeight-MapHeight*BoxSize[1])/MapHeight)    

    BombImage = pygame.transform.scale(BombPic,BoxSize)
    BoxImage = pygame.transform.scale(BoxPic,(BoxSize[0]+HighLightBord,BoxSize[1]+HighLightBord))
    HBoxImage = pygame.transform.scale(HBoxPic,(BoxSize[0]+HighLightBord,BoxSize[1]+HighLightBord))
    FlagImage = pygame.transform.scale(FlagPic,BoxSize)
    UnminedImage = pygame.transform.scale(UnminedPic,BoxSize)
    CrossImage = pygame.transform.scale(CrossFlagPic,BoxSize)
    CrushImage = pygame.transform.scale(CrushPic,BoxSize)
    Background = pygame.transform.scale(BackgroundPic,(GameWidth,GameHeight))
    MineCountImage=[]
    for i in range(0,9):
        Image = pygame.transform.scale(MineCountPic[i],BoxSize)
        MineCountImage.append(Image)

    Game=reset()
    HBoxPos=[0,0]
    FlagUsed=0
    HITPRESSED=False
    FirstTime=True
    while True:
        PrintScreen()
        
        c,HITPRESSED,Exit=RequestedMove()
        if Exit:
            break
        if c==2 and HBoxPos[0]!=0:
            HBoxPos[0]-=1
        elif c==8 and HBoxPos[0]!=MapHeight-1:
            HBoxPos[0]+=1
        elif c==4 and HBoxPos[1]!=0:
            HBoxPos[1]-=1
        elif c==6 and HBoxPos[1]!=MapWidth-1:
            HBoxPos[1]+=1
        elif c==5:
            #pressed
            if Game[Display][HBoxPos[0]][HBoxPos[1]]==0:
                Game[Display][HBoxPos[0]][HBoxPos[1]]=1

            #if pressed at mine and not flagged, game over
            if Game[Mines][HBoxPos[0]][HBoxPos[1]]==-1 and Game[Display][HBoxPos[0]][HBoxPos[1]]!=-1:
                if not FirstTime:
                    PrintScreen(True)
                    #ExitGame()
                    GameOver("lose")
                    break
                else:
                    while Game[Mines][HBoxPos[0]][HBoxPos[1]]==-1 :
                        Game=reset()
                    Game[Display][HBoxPos[0]][HBoxPos[1]]=1
                    
            FirstTime=False
            #act of making visible
            Game[Display]=SetVisible()
            Game[Display]=SetVisible()
            
            #if found all the mines, game win
            if FoundAllMines():
                GameOver("win")
                break
        elif c==-1:
            #flagged
            if Game[Display][HBoxPos[0]][HBoxPos[1]]==0 and FlagUsed!=MinesCount:
                Game[Display][HBoxPos[0]][HBoxPos[1]]=-1
                FlagUsed+=1
            elif Game[Display][HBoxPos[0]][HBoxPos[1]]==-1 and FlagUsed!=0:
                Game[Display][HBoxPos[0]][HBoxPos[1]]=0
                FlagUsed-=1
