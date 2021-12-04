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
 
    def get_value(self):
        '''GUIDie.get_value() -> int
        returns the value of the die
        returns 0 if the die hasn't been rolled yet'''
        if hasattr(self,'top'):
            return self.valueList[self.top-1]
        else:
            return 0
 
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
 
class Decath400MFrame(Frame):
    '''frame for a game of 400 Meters'''
 
    def __init__(self,master,name):
        '''Decath400MFrame(master,name) -> Decath400MFrame
        creates a new 400 Meters frame
        name is the name of the player'''
        # set up Frame object
        Frame.__init__(self,master)
        self.grid()
        # label for player's name
        Label(self,text=name,font=('Arial',18)).grid(columnspan=3,sticky=W)
        # set up score and rerolls
        self.scoreLabel = Label(self,text='Score: 0',font=('Arial',18))
        self.scoreLabel.grid(row=0,column=3,columnspan=2)
        self.rerollLabel = Label(self,text='Rerolls: 5',font=('Arial',18))
        self.rerollLabel.grid(row=0,column=5,columnspan=3,sticky=E)
        # initialize game data
        self.score = 0
        self.rerolls = 5
        self.gameround = 0
        # set up dice
        self.dice = []
        for n in range(8):
            self.dice.append(GUIDie(self,[1,2,3,4,5,-6],['black']*5+['red']))
            self.dice[n].grid(row=1,column=n)
        # set up buttons
        self.rollButton = Button(self,text='Roll',command=self.roll)
        self.rollButton.grid(row=2,columnspan=2)
        self.keepButton = Button(self,text='Keep',state=DISABLED,command=self.keep)
        self.keepButton.grid(row=3,columnspan=2)
 
    def roll(self):
        '''Decath400MFrame.roll()
        handler method for the roll button click'''
        # roll both dice
        self.dice[2*self.gameround].roll()
        self.dice[2*self.gameround+1].roll()
        # if this was the first roll of the round, turn on the keep button
        if self.keepButton['state'] == DISABLED:
            self.keepButton['state'] = ACTIVE
        else:  # otherwise we just spent a reroll
            self.rerolls -= 1
            self.rerollLabel['text'] = 'Rerolls: '+str(self.rerolls)
        if (self.rerolls == 0):  # no rerolls left, so turn off roll button
            self.rollButton['state'] = DISABLED
 
    def keep(self):
        '''Decath400MFrame.keep()
        handler method for the keep button click'''
        # add dice to score and update the scoreboard
        self.score += self.dice[2*self.gameround].get_value() + \
                      self.dice[2*self.gameround+1].get_value()
        self.scoreLabel['text'] = 'Score: '+str(self.score)
        self.gameround += 1  # go to next round
        if self.gameround < 4:  # move buttons to next pair of dice
            self.rollButton.grid(row=2,column=2*self.gameround,columnspan=2)
            self.keepButton.grid(row=3,column=2*self.gameround,columnspan=2)
            self.rollButton['state'] = ACTIVE
            self.keepButton['state'] = DISABLED
        else:  # game over
            self.keepButton.grid_remove()
            self.rollButton.grid_remove()
            self.rerollLabel['text'] = 'Game over'
 
class Decath400MComputerFrame(Decath400MFrame):
    '''frame for a computer-played game of 400 Meters'''
 
    def __init__(self,master):
        '''Decath400MComputerFrame(master) -> Decath400MComputerFrame
        created a new computer-player 400 Meters frame'''
        Decath400MFrame.__init__(self,master,'Computer')
        self.isReroll = False
 
    def roll(self):
        '''Decath400MComputerFrame.roll()
        handler method for the roll button click'''
        Decath400MFrame.roll(self)  # call the superclass roll
        # deduct a reroll if necessary
        if self.isReroll:
            self.rerolls -= 1
            self.rerollLabel['text'] = 'Rerolls: '+str(self.rerolls)
        # decide whether to reroll or keep
        if self.should_reroll():
            self.keepButton['state'] = DISABLED # force reroll
            self.isReroll = True
        else:
            self.rollButton['state'] = DISABLED # force keep
            self.isReroll = False
 
    def should_reroll(self):
        '''Decath400MComputerFrame.should_reroll()
        returns True if computer player should reroll, False if should keep'''
        # must keep if no rerolls
        if self.rerolls == 0:
            return False
        rollValue = self.dice[2*self.gameround].get_value() + \
                    self.dice[2*self.gameround+1].get_value()
        # use chart from optimal strategy
        if self.gameround == 0 and self.rerolls >=2 :
            return rollValue < self.rerolls
        if self.gameround == 0 and self.rerolls == 1:
            return rollValue < -1
        if self.gameround == 1:
            return rollValue < (self.rerolls + 1)
        if self.gameround == 2 and self.rerolls >= 4:
            return rollValue < 6
        if self.gameround == 2 and 3 >= self.rerolls >= 2:
            return rollValue < (self.rerolls + 2)
        if self.gameround == 2 and self.rerolls == 1:
            return rollValue < 2
        if self.gameround == 3 and self.rerolls >= 3:
            return rollValue < 7
        if self.gameround == 3 and self.rerolls == 2:
            return rollValue < 6
        if self.gameround == 3 and self.rerolls == 1:
            return rollValue < 3
 
# play the game
name = ''
while name.strip() == '':
    name = input('Enter your name: ')
root = Tk()
root.title('400 Meters')
playerGame = Decath400MFrame(root,name.strip())
computerGame = Decath400MComputerFrame(root)
root.mainloop()