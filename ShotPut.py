from tkinter import *
import random
 
class GUIDie(Canvas):
    '''6-sided Die class for GUI'''
 
    def __init__(self,master,valueList=[1,2,3,4,5,6],colorList=['black']*6):
        '''GUIDie(master,[valueList,colorList]) -> GUIDie
        creates a GUI 6-sided die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        # create a 60x60 white canvas with a 5-pixel grooved border
        Canvas.__init__(self,master,width=60,height=60,bg='white',\
                        bd=5,relief=GROOVE)
        # store the valuelist and colorlist
        self.valueList = valueList
        self.colorList = colorList
        # initialize the top value
        self.top = 1
 
    def get_top(self):
        '''GUIDie.get_top() -> int
        returns the value on the die'''
        return self.valueList[self.top-1]
 
    def roll(self):
        '''GUIDie.roll()
        rolls the die'''
        self.top = random.randrange(1,7)
        self.draw()
 
    def draw(self):
        '''GUIDie.draw()
        draws the pips on the die'''
        # clear old pips first
        self.erase()
        # location of which pips should be drawn
        pipList = [[(1,1)],
                   [(0,0),(2,2)],
                   [(0,0),(1,1),(2,2)],
                   [(0,0),(0,2),(2,0),(2,2)],
                   [(0,0),(0,2),(1,1),(2,0),(2,2)],
                   [(0,0),(0,2),(1,0),(1,2),(2,0),(2,2)]]
        for location in pipList[self.top-1]:
            self.draw_pip(location,self.colorList[self.top-1])
 
    def draw_pip(self,location,color):
        '''GUIDie.draw_pip(location,color)
        draws a pip at (row,col) given by location, with given color'''
        (centerx,centery) = (17+20*location[1],17+20*location[0])  # center
        self.create_oval(centerx-5,centery-5,centerx+5,centery+5,fill=color)
 
    def erase(self):
        '''GUIDie.erase()
        erases all the pips'''
        pipList = self.find_all()
        for pip in pipList:
            self.delete(pip)

 
class ShotPutFrame(Frame):
    '''frame for a game of Shot Put'''
 
    def __init__(self,master,name):
        '''ShotPutFrame(master,name) -> ShotPutFrameFrame
        creates a new Shot Put frame
        name is the name of the player'''
        # set up Frame object
        Frame.__init__(self,master)
        self.grid()

        # label for player's name
        Label(self,text=name,font=('Arial',10)).grid(columnspan=2,sticky=W)

        # set up attempt score and high score
        self.attemptscoreLabel = Label(self,text='Attempt #1 Score: 0',font=('Arial',10))
        self.attemptscoreLabel.grid(row=0,column=3,columnspan=2)
        self.scoreLabel = Label(self,text='High Score: 0',font=('Arial',10))
        self.scoreLabel.grid(row=0,column=6,columnspan=2)
        
        # initialize game data
        self.score = 0
        self.max_score = 0
        self.score_list = []
        self.die = 0
        self.attempt = 1
        
        # set up dice
        self.dice = []
        for n in range(8):
            self.dice.append(GUIDie(self,[1,2,3,4,5,6],['red']+['black']*5))
            self.dice[n].grid(row=1,column=n)
        
        # set up buttons
        self.rollButton = Button(self,text='Roll',command=self.roll)
        self.rollButton.grid(row=2,columnspan=1)
        self.stopButton = Button(self,text='Stop',state=DISABLED,command=self.stop)
        self.stopButton.grid(row=3,columnspan=1)
 
    def roll(self):
        '''ShotPutFrame.roll()
        handler method for the roll button click'''
        # roll a die
        self.dice[self.die].roll()

        # if this was the first roll of the round, turn on the stop button
        if self.stopButton['state'] == DISABLED:
            self.stopButton['state'] = ACTIVE
            self.attemptscore = 0

        # check for a foul roll
        self.rollFouled = self.dice[self.die].get_top() == 1
        if self.rollFouled:
            self.attemptscoreLabel['text'] = 'FOULED ATTEMPT'
            self.rollButton['state'] = DISABLED
            self.stopButton['text'] = 'FOUL'
        else:
            self.attemptscore += self.dice[self.die].get_top()
            self.attemptscoreLabel['text'] = f'Attempt #{self.attempt} Score: {self.attemptscore}'
            self.die += 1
            if self.die < 8:  # move buttons to next die
                self.rollButton.grid(row=2,column=self.die,columnspan=1)
                self.stopButton.grid(row=3,column=self.die,columnspan=1)
            else:
                self.rollButton['state'] = DISABLED
 
    def stop(self):
        '''ShotPutFrame.stop()
        handler method for the stop button click'''
        # check for foul
        if self.rollFouled:
            self.attemptscore = 0
        
        # append the score to the list of scores
        self.score_list.append(self.attemptscore)
     
        if max(self.score_list) == self.attemptscore:  # new high score
            self.score = self.attemptscore
            self.scoreLabel['text'] = f'High Score: {self.score}'
        self.attempt += 1  # go to next attempt
        if self.attempt <= 3:  # reset dice,buttons,labels
            self.attemptscoreLabel['text'] = f'Attempt #{self.attempt} Score: 0'
            self.rollButton['state'] = ACTIVE
            self.stopButton['state'] = DISABLED
            self.stopButton['text'] = 'Stop'
            self.rollButton.grid(row=2,column=0,columnspan=1)
            self.stopButton.grid(row=3,column=0,columnspan=1)
            for die in self.dice:
                die.erase()
            self.die = 0
        else:  # game over
            self.stopButton.grid_remove()
            self.rollButton.grid_remove()
            self.attemptscoreLabel['text'] = 'Game over'
 
 
# play the game
name = ''
while name.strip() == '':
    name = input('Enter your name: ')
root = Tk()
root.title('Shot Put')
game = ShotPutFrame(root,name.strip())
game.mainloop()