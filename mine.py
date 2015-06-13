"""Minesweeper, version 2.0"""

import random, time, pygame, sys    #do the import job
from pygame.locals import *

color={"WHITE":(255,255,255),
       "BLACK":(0,0,0),
       "RED":(255,0,0),
       "GREEN":(0,255,0),
       "BLUE":(0,0,255)}
boardState={"MINED":1,
            "UNMINED":0,
            "FLAGGED":-1}
event={"leftMouseDown":"left mouse button pressed",
        "leftMouseUp":"left mouse button released",
        "rightMouseDown":"right mouse button pressed",
        "rightMouseUp":"right mouse button released",
        "escUp":"Escape button released",
        "exit":"Exit",
        "mouseMotion":"The motion caused by movement of mouse"}

class theMineGame(object):
    """The actual game class"""

    imgSrc={"bomb":"Bomb.png",
            "selectBox":{"onClick":"HighlightBox.png","onHover":"Box.png"},
            "flag":"Flag.png",
            "crossFlag":"CrossFlag.png",
            "crush":"Crush.PNG",
            "unmined":"Unmined.png",
            "num":{
                "0":"0.png",
                "1":"1.png",
                "2":"2.png",
                "3":"3.png",
                "4":"4.png",
                "5":"5.png",
                "6":"6.png",
                "7":"7.png",
                "8":"8.png"}}
    preConfigured=False
    def __init__(self, fullScreen=False,gameCellsCount=8,minesCount=40, gameSize=600,cellSize=70):

        #changeable variables
        self.__gameSize=gameSize
        self.__cellSize=cellSize          #the size of each cell
        self.__cellsCount=gameCellsCount  #it means, the board has 8*8 boxes
        self.__minesCount=minesCount      #the total number of mines

        if(fullScreen):
            self.__fullScreen=pygame.FULLSCREEN
        else:
            self.__fullScreen=0
            
        self.__fps=20                     #the speed of game
        self.__highLightBorder=5            #the width of the highlight border
        self.__fontSize=30
        self.__gameFont=None
        self.__bgColor=(133,133,133)
        self.__fontColor=color['BLUE']
        self.__font=None
        
        #unchangeable variables
        self.__gameOver=False
        self.__gameWon=False
        self.__clock=pygame.time.Clock()
        self.__gameScreen=0
        self.__cellSpacing=0
        self.__highLightBoxSpacing=3
        self.__gameFont=0
        self.__minedNoOfCells=0     #to represent how many boxes have been mined
        self.__curNoOfFlags=0       #number of flags placed currently
        self.__notifyPanelHeight=100
        self.__theImages={"bomb":0,
                          "selectBox":{"onClick":0,"onHover":0},
                          "flag":0,
                          "crossFlag":0,
                          "crush":0,
                          "unmined":0,
                          "num":{
                              "0":0,
                              "1":0,
                              "2":0,
                              "3":0,
                              "4":0,
                              "5":0,
                              "6":0,
                              "7":0,
                              "8":0}}

        
    def __resetTheBoard(self):
        """Reset the maps"""
        board=[]     #the board array is the one which is visible to the user
        mine=[]      #the mine array is the actual board containing mines
        for i in range(0,self.__cellsCount):
            board.append([])
            mine.append([])
            for j in range(0,self.__cellsCount):
                board[i].append(boardState["UNMINED"])
                mine[i].append(0)

        #fill the mine array
        x=0     #no of mines filled currently in the board
        while (x<self.__minesCount):
            c=(random.randint(0,self.__cellsCount-1),
               random.randint(0,self.__cellsCount-1))   #get a random cell
            if(mine[c[0]][c[1]] == 0):       #got a new random cell
                mine[c[0]][c[1]]=-1  #-1 for indicating that the cell is a mine
                x += 1

        #fill the number in the mine array
        for i in range(0, len(mine)):
            for j in range(0, len(mine[i])):
                if mine[i][j]==-1:
                    continue #no need to take any action since the cell is already mine

                num=0   #the number to be inserted in current cell

                if (i!=0):       #first line check
                    if (j!=0 and mine[i-1][j-1]==-1):#top left
                        num+=1
                    if (j!=len(mine)-1 and mine[i-1][j+1]==-1):#top right
                        num+=1
                    if (mine[i-1][j]==-1):   #top
                        num+=1
                if (i!=len(mine[i])-1):  #last line check
                    if (j!=0 and mine[i+1][j-1]==-1):#bottom left
                        num+=1
                    if (j!=len(mine)-1 and mine[i+1][j+1]==-1):#bottom right
                        num+=1
                    if (mine[i+1][j]==-1):#bottom
                        num+=1
                if (j!=0 and mine[i][j-1]==-1): #left
                    num+=1
                if (j!=len(mine[i])-1 and mine[i][j+1]==-1): #right
                    num+=1
                mine[i][j]=num
        self.__boardUser=board
        self.__boardMine=mine

        return True

    def __preConfigure(self):
        """Preconfigures the settings. Should be called only once"""
        if ( not theMineGame.preConfigured):
            preConfigured=True
            pygame.init()
            pygame.key.set_repeat(400,60)
            pygame.display.set_caption("The Mine Game")
        return True

    def __init_graphics(self):
        """Load images"""

        bomb=pygame.image.load(theMineGame.imgSrc["bomb"])
        selectBox={"onClick":0,"onHover":0}
        selectBox['onClick']=pygame.image.load(theMineGame.imgSrc["selectBox"]["onClick"])
        selectBox['onHover']=pygame.image.load(theMineGame.imgSrc["selectBox"]["onHover"])
        flag=pygame.image.load(theMineGame.imgSrc["flag"])
        crossFlag=pygame.image.load(theMineGame.imgSrc["crossFlag"])
        crush=pygame.image.load(theMineGame.imgSrc['crush'])
        unmined=pygame.image.load(theMineGame.imgSrc['unmined'])

        num=[]
        for i in range(0,9):
            num.append(pygame.image.load(theMineGame.imgSrc['num'][str(i)]))

        #now convert into aspect ratio
        boxSize=(self.__cellSize,self.__cellSize)
        activeCellSize=(self.__highlightBoxSize,self.__highlightBoxSize)

        self.__theImages['bomb']=pygame.transform.scale(bomb, boxSize)
        self.__theImages['flag']=pygame.transform.scale(flag, boxSize)
        self.__theImages['crossFlag']=pygame.transform.scale(crossFlag, boxSize)
        self.__theImages['crush']=pygame.transform.scale(crush, boxSize)
        self.__theImages['unmined']=pygame.transform.scale(unmined, boxSize)

        self.__theImages['selectBox']['onClick']=pygame.transform.scale(selectBox['onClick'], activeCellSize)
        self.__theImages['selectBox']['onHover']=pygame.transform.scale(selectBox['onHover'], activeCellSize)
        
        #load the numbers
        for i in range(0,9):
            self.__theImages['num'][str(i)]=pygame.transform.scale(num[i],boxSize)
        
        return True
        
    def __init_video(self):
        """Make the video ready"""

        #set font
        self.__gameFont=pygame.font.SysFont(self.__font,self.__fontSize)
        
        #set video mode, test display the screen
        self.__gameScreen=pygame.display.set_mode((self.__gameSize,self.__gameSize+self.__notifyPanelHeight),self.__fullScreen,32)

        return True

    def __recreateRatios(self):
        """Make aspect ratio of images, rebuild cell spacing, etc"""

        #rebuild cell spacing
        self.__cellSpacing=int(self.__gameSize-self.__cellsCount*self.__cellSize)/(self.__cellsCount+1)
        
        #size of the highlight box:
        self.__highlightBoxSize=(2*self.__highLightBorder)+self.__cellSize

        #aspect ratio of images=cell size
        return True
    def __gameReady(self):
        """The funtion to initialise all the resources"""

        print("preConfiguring the default options")
        if (not theMineGame().__preConfigure()):
            return -1

        print("Creating a new board")
        if(not self.__resetTheBoard()):
            return -2

        print("Recreating aspect ratios, and variables")
        if(not self.__recreateRatios()):
            return -3
        
        print("Initialising graphics")
        if(not self.__init_graphics()):
            return -4

        print("Loading video")
        if(not self.__init_video()):
            return -5
        
        return 1
    
    
    def __render(self,leftClick,mousePosition):
        """The game screen render"""
        bg=pygame.Rect(0,0,self.__gameSize,self.__gameSize)
        self.__gameScreen.fill(self.__bgColor)

        #create an array of all images
        array=[]
        for i in range(0, len(self.__boardUser)):
            array.append([])
            for j in range(0, len(self.__boardUser[i])):
                box=0
                if (self.__boardUser[i][j]==boardState['UNMINED']):
                    #print the bomb if game over
                    if(self.__gameOver and self.__boardMine[i][j]==-1):
                        box=self.__theImages['bomb']
                    else:
                        box=self.__theImages['unmined']
                elif (self.__boardUser[i][j]==boardState['FLAGGED']):
                    #if death, check if the flag is inserted in proper place, else, show crossflag
                    if(self.__gameOver and self.__boardMine[i][j]>-1):
                        box=self.__theImages['crossFlag']
                    else:
                        box=self.__theImages['flag']
                else:
                    if(self.__gameOver and self.__boardMine[i][j]==-1):
                        box=self.__theImages['crush']
                    elif (self.__boardMine[i][j]==-1):
                        box=self.__theImages['bomb']
                    else:
                        box=self.__theImages['num'][str(self.__boardMine[i][j])]

                array[i].append(box)


        #for highlight box
        xPos=mousePosition[0]
        xMouseHover=0
        while (xPos > self.__cellSpacing+self.__cellSize):
            xMouseHover+=1
            xPos-=self.__cellSpacing+self.__cellSize

        yPos=mousePosition[1]
        yMouseHover=0
        while (yPos>self.__cellSpacing+self.__cellSize):
            yMouseHover+=1
            yPos-=self.__cellSpacing+self.__cellSize


        #print the array inside the display
        rect=0
        height=self.__cellSize
        width=self.__cellSize
        x=0
        y=0
        for i in range(0,len(self.__boardUser)):
            for j in range(0, len(self.__boardUser[i])):
                x=self.__cellSpacing*(i+1)+self.__cellSize*(i)
                y=self.__cellSpacing*(j+1)+self.__cellSize*(j)
                rect=pygame.Rect(x,y,width,height)
                self.__gameScreen.blit(array[i][j],rect)

                #the job for highlighting the selected position
                if(yMouseHover==j and xMouseHover==i):
                    highLightBoxLeft=x
                    highLightBoxUp=y
        curBoxPos=(xMouseHover,yMouseHover)

        #print the highlighted box
        if not(self.__gameOver or self.__gameWon):
            if(xMouseHover<len(self.__boardUser) and yMouseHover<len(self.__boardUser[0])):
                left=highLightBoxLeft-self.__highLightBoxSpacing-self.__cellSpacing
                top=highLightBoxUp-self.__highLightBoxSpacing-self.__cellSpacing
                width=self.__cellSize+2*self.__highLightBoxSpacing
                height=self.__cellSize+2*self.__highLightBoxSpacing
                rect=pygame.Rect(left,top,width,height)

                if not leftClick:
                    self.__gameScreen.blit(self.__theImages['selectBox']['onHover'],rect)
                else:
                    self.__gameScreen.blit(self.__theImages['selectBox']['onClick'],rect)

        #time for notification panel
        if(self.__gameWon or self.__gameOver):
            if(self.__gameWon):
                text="You win the game!!"
            else:
                text="Oops, you lose!!"
            objRect=pygame.Rect(0,self.__gameSize,self.__gameSize,self.__notifyPanelHeight)
            toBlitImage=self.__gameFont.render(text,1,self.__fontColor)
            toBlitImage=pygame.transform.scale(toBlitImage,(self.__gameSize,self.__notifyPanelHeight))
            self.__gameScreen.blit(toBlitImage,objRect)
        else:
            text="Boxes revealed: " + str(self.__getRevealedNoOfBoxes()) +" out of " +str(self.__cellsCount*self.__cellsCount-self.__minesCount)
            objRect=pygame.Rect(0,self.__gameSize,self.__gameSize,int(self.__notifyPanelHeight/2))
            toBlitImage=self.__gameFont.render(text,1,self.__fontColor)
            toBlitImage=pygame.transform.scale(toBlitImage,(self.__gameSize,int(self.__notifyPanelHeight/2)-1))
            self.__gameScreen.blit(toBlitImage,objRect)

            text2="Flags:"+ str(self.__curNoOfFlags)+" out of "+str(self.__minesCount)
            objRect=pygame.Rect(0,self.__gameSize+int(self.__notifyPanelHeight/2),self.__gameSize,int(self.__notifyPanelHeight/2))
            toBlitImage=self.__gameFont.render(text2,1,self.__fontColor)
            toBlitImage=pygame.transform.scale(toBlitImage,(self.__gameSize,int(self.__notifyPanelHeight/2)-1))
            self.__gameScreen.blit(toBlitImage,objRect)
        
        pygame.display.update()

        return curBoxPos

    def __getMove(self):
        """sends the event type and also the mouse position"""
        while True:
            self.__clock.tick(self.__fps)
            mousepos=(0,0)
            for i in pygame.event.get():
                if i.type==QUIT:
                     return [event['exit']]
                elif i.type==KEYUP:
                    return [event['escUp']]
                elif i.type==MOUSEBUTTONDOWN:
                    if i.button==1:
                        return [event['leftMouseDown']]
                    elif i.button==3:
                        return [event['rightMouseDown']]
                elif i.type==MOUSEBUTTONUP:
                    if i.button==1:
                        return [event['leftMouseUp']]
                    elif i.button==3:
                        return [event['rightMouseUp']]
                elif i.type==MOUSEMOTION:
                    return [event['mouseMotion'],i.pos]

    def __putFlag(self,mouseBox):
        #check if the position is mined, if mined, then donot allow to flag
        if(self.__boardUser[mouseBox[0]][mouseBox[1]]==boardState['UNMINED']) and (self.__curNoOfFlags<self.__minesCount):
            self.__boardUser[mouseBox[0]][mouseBox[1]]=boardState['FLAGGED']
            self.__curNoOfFlags+=1
        elif(self.__boardUser[mouseBox[0]][mouseBox[1]]==boardState['FLAGGED']):
            self.__boardUser[mouseBox[0]][mouseBox[1]]=boardState['UNMINED']
            print("removed flag")
            self.__curNoOfFlags-=1
        else:
            print("not an unmined position")
                
        #multiArrayPrinter(self.__boardUser)
        return True

    def __handleClick(self, mousePos):
        if(self.__gameOver):
            print("Game already over")
            return False
        if (self.__boardUser[mousePos[0]][mousePos[1]] != boardState['UNMINED']):
            print("cannot click here, flagged or already mined")
            return False
        else:            
            #reveal the current box
            self.__boardUser[mousePos[0]][mousePos[1]]= boardState['MINED']

            if(self.__boardMine[mousePos[0]][mousePos[1]]==-1):
                self.__gameOver=True
                return True
            else:
                move=[[-1,-1],[-1,0],[-1,+1],[0,-1],[0,+1],[+1,-1],[+1,0],[+1,+1]]

                
                emptyBoxStack=[]
                if(self.__boardMine[mousePos[0]][mousePos[1]]==0):
                    emptyBoxStack.append(mousePos)

                toAct=[mousePos]
                x=0
                while True:
                    for i in list(move):
                        newPos=[toAct[0][0]+i[0],toAct[0][1]+i[1]]
                        
                        if self.__isValidPoint(newPos)and self.__boardMine[newPos[0]][newPos[1]]==0 and self.__boardUser[newPos[0]][newPos[1]]==boardState['UNMINED']:
                                self.__boardUser[newPos[0]][newPos[1]]=boardState['MINED']
                                toAct.append(newPos)
                                emptyBoxStack.append(newPos)
                    
                    if(len(toAct) <= 1):
                            break
                    else:
                        toAct.pop(0)
                    x+=1

                #emptyBoxStack has all the empty boxes, now reveal their sides
                while not(emptyBoxStack==[]):
                    for i in list(move):
                        newPos=[emptyBoxStack[0][0]+i[0],emptyBoxStack[0][1]+i[1]]
                        if self.__isValidPoint(newPos):
                            if self.__boardUser[newPos[0]][newPos[1]]==boardState['UNMINED']:
                                self.__boardUser[newPos[0]][newPos[1]] = boardState['MINED']
                    emptyBoxStack.pop(0)
                    
            return True

    def __isValidPoint(self,newPos):
        c=(newPos[0]>=0 and newPos[0] <= len(self.__boardUser)-1 and newPos[1]>=0 and newPos[1]<=len(self.__boardUser)-1)
        return c
    
    def __getRevealedNoOfBoxes(self):
        revealedBoxes=0

        for i in list(self.__boardUser):
            for j in list(i):
                if j==boardState['MINED']:
                    revealedBoxes+=1

        return revealedBoxes
    
    def __userHasWon(self):
        revealedBoxes=self.__getRevealedNoOfBoxes()
        if revealedBoxes==self.__cellsCount*self.__cellsCount-self.__minesCount:
            return True
        else:
            return False
    def __gameOverInterface(self):
        self.__render(False,(0,0))
        while True:
            z=self.__getMove()
            if (z[0]==event['leftMouseDown'] or z[0]==event['leftMouseUp'] or z[0] ==event['exit'] or z[0] ==event['escUp']):
                EndGame()
    def play(self):
        """The actual gameloop"""

        z=self.__gameReady()
        if(z < 0):
            print("Died because the game couldnot be ready %s"%(z))
        else:
            print("Welcome to minesweeper")

        #the gameloop now
        leftClick=False
        mousePos=(0,0)

        firstTime=True
        while True:
            mouseBox=self.__render(leftClick,mousePos)
            action=self.__getMove()
            
            if(action[0] == event['exit'] or action[0] == event['escUp']):
                break
            elif (action[0]==event['mouseMotion']):
                mousePos=action[1]
            elif (action[0]==event['leftMouseDown']):
                leftClick=True
            else:
               
                if(mouseBox[0] <0 or mouseBox[1]<0 or mouseBox[0]>=len(self.__boardUser) or mouseBox[1]>=len(self.__boardUser[0])):
                    continue
                if (action[0]==event['leftMouseUp']):
                    leftClick=False
                    
                    while True:
                        self.__handleClick(mouseBox)
                        if(self.__gameOver and firstTime):
                                self.__resetTheBoard()
                                self.__gameOver=False
                                continue
                        elif(self.__gameOver):
                            self.__gameOverInterface()
                        else:
                            break
                    firstTime=False

                    if (self.__userHasWon()):
                        print("You won the game")
                        self.__gameWon=True
                        self.__gameOverInterface()
                        
                elif (action[0]==event['rightMouseUp']):
                  self.__putFlag(mouseBox)            
            
        EndGame()
        
def multiArrayPrinter(array):       #prints 2-dimensional array
    x=""
    for j in range(0,len(array)):
        for i in range(0,len(array[j])):
            x+=str(array[i][j])+"\t"
        x+="\n"
    print("\n"+x)  

def EndGame():
    
    pygame.quit()
    print("Good bye!")
    sys.exit()
    
theMineGame(False).play()

