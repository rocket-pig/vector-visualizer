#!/usr/bin/python
import random
import datetime
import pygame
from time import sleep
from gensim.models import KeyedVectors as model
from threading import Thread
import sys,signal
from random import shuffle

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
global seed

###### ##### #### ### ## # _______Config______ # ## ### #### ##### ######
VECTOR_FILE_LOCATION = '/opt/data/wiki.simple.vec'
USE_RANDOM_COLORS = True
#if above is False, all text will be this color:
SINGLE_COLOR = (106,90,205)
#########################################################################
# Usage: python script.py "seed word"
#################################################################################################
###
#                              Word Vector Visualizer v1 by Rocketpig
#                                           3/30/2018
##
#################################################################################################
# ## Change Log ## #
# 3/30/2018
# Initial release.


#init pygame window
pygame.init()
screen = pygame.display.set_mode((800, 600)) #window size
font12 = pygame.font.SysFont("comicsansms", 12)
clock = pygame.time.Clock()
#only listen to keyboard events, hopefully help load?
pygame.event.set_allowed(None)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.USEREVENT])
done = False

def check_for_keys():
    global seed
    #listening for keypresses
    while True:
        event = pygame.event.wait()
        print("Event = "+str(event))
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            try: event.key
            except: event.key="0"
            if event.key == pygame.K_q: #Q - quit
                print("Quitting due to 'q' press")
                pygame.quit()
                signal_handler()
            #if a directional key, change seed to word at that position and update everything.
            if event.key == pygame.K_UP:
                seed=Word(seed.s_north)
                update_screen(seed)
            if event.key == pygame.K_DOWN:
                seed=Word(seed.s_south)
                update_screen(seed)
            if event.key == pygame.K_LEFT:
                seed=Word(seed.s_west)
                update_screen(seed)
            if event.key == pygame.K_RIGHT:
                seed=Word(seed.s_east)
                update_screen(seed)
            #else: #TODO: numkeys change visual styles and letters trigger the 'enter new word' function.
            #if event.key == pygame.K_n:
            #delete center area, display text as its typed

red_rando,green_rando,blue_rando = 80,80,255
def rando_color():
    if USE_RANDOM_COLORS == True:
      return (random.randint(20,red_rando),random.randint(20,green_rando),random.randint(20,blue_rando))
    else:
      return(SINGLE_COLOR)

def rw(word,size=24): #return the pygame font object for a word
    newfont = pygame.font.SysFont("comicsansms", size)
    return newfont.render(word, True, rando_color())


def load_vec():
    global m
    m = model.load_word2vec_format(VECTOR_FILE_LOCATION) #<-------------- .vec file --------------->

def start_vec_thread(seedtxt):
    global seed,m
    #start loading the vec file
    loader = Thread(target=load_vec)
    loader.daemon=True
    loader.start()
    #the db loading is backgrounded: we are free to do something clever till the vectors are 'online'.
    loading=rw('loading')
    seedword=rw(seedtxt)
    while loader.isAlive(): #flash loading in corner, TODO make some entertaining shit w argv 'seed' word.
        global seed
        #write 'loading...' in corner
        screen.blit(loading,((screen.get_width()-40) - loading.get_width(), (screen.get_height()-20) - loading.get_height() // 2))
        #write seed to middle of screen
        screen.blit(seedword,((screen.get_width()/2) - seedword.get_width() // 2, screen.get_height()/2 - seedword.get_height() // 2)) #display text in middle of screen
        pygame.display.flip() #refresh screen
        #check_for_keys() #allow quitting etc before loading finishes
        clock.tick(30)
        sleep(.5)
    #we've finished. write something else.
    finished = rw("load complete..",24)
    screen.fill((0, 0, 0)) #fill with rgb black
    pygame.display.flip() #refresh screen
    screen.blit(finished,(screen.get_width()-40 - finished.get_width() // 2, screen.get_height()-20 - finished.get_height() // 2)) #display text in middle of screen
    pygame.display.flip() #refresh screen
    clock.tick(30)
    sleep(.2)


def start_key_thread():
    global seed
    #listen for keys
    keypresses = Thread(target = check_for_keys)
    keypresses.daemon=True
    keypresses.start()


def get_similar(word): #returns a list of 4 most similar
    global m
    similars = [i[0] for i in m.similar_by_word(word,topn=500)] #<----------------can change 'topn1=500' to smaller value (100,even 10) for speed and closer relatedness of results
    shuffle(similars)
    if len(similars) >= 4:
        return similars[0:4:1]
    else:
        #pad with nones so we dont crash
        while len(similars) < 4:
            similars.append("none")
        return similars

#new_word = Word('word',[render size], [similar word render size])
class Word(object): #store word's similars and font objects under one roof:
    global m
    def __init__(self, name,size=34,simsize=14):
        self.name = name
        self.size = size
        self.simsize=simsize
        self.s = name #for consistency
        self.f = rw(self.name,self.size)
        #store the string (s_)
        self.s_north,self.s_east,self.s_south,self.s_west=get_similar(self.name)
        print(self.s, ": n:",self.s_north,self.s_east,self.s_south,self.s_west)
        #store the pygame font object (f_)
        self.f_north=rw(self.s_north,simsize)
        self.f_east=rw(self.s_east,simsize)
        self.f_south=rw(self.s_south,simsize)
        self.f_west=rw(self.s_west,simsize)


#display a Word(word) at coords, and it's four similar words in a circle around it:
def wordandsims(word,x,y,offset):
    #display argv word in center
    screen.blit(word.f,(x - word.f.get_width() // 2, y - word.f.get_height() // 2)) #main word
    pygame.display.flip() #refresh screen
    #display top 4 most similar around it (it being x/y)
    #north, same long, -offset lat
    screen.blit(word.f_north,(x - word.f_north.get_width() // 2, (y-offset) - word.f_north.get_height() // 2)) #display north
    #east, +offset long+seed word length, same lat
    screen.blit(word.f_east,((x+offset) + (word.f.get_width()/2), y - word.f_east.get_height() // 2)) #display east
    #south, same long, +offset lat
    screen.blit(word.f_south,(x - (word.f_south.get_width()//2), (y+offset) - word.f_south.get_height() // 2)) #display south
    #west, -offset long - seed word length, same lat
    screen.blit(word.f_west,((x-offset) - (word.f.get_width()), y - word.f_west.get_height() // 2)) #display west
    pygame.display.flip() #refresh screen


def update_screen(seed): #seed should just be a str.
    screen.fill((0, 0, 0)) #fill with rgb black
    #wordandsims(seed,400,300,200)
    screen.blit(seed.f,((screen.get_width()/2) - seed.f.get_width() // 2,(screen.get_height()/2) - seed.f.get_height() // 2)) #main word
    wordandsims(Word(seed.s_north,28,16),400,300-200,40)
    wordandsims(Word(seed.s_east,28,16),400+250,300,40)
    wordandsims(Word(seed.s_south,28,16),400,300+200,40)
    wordandsims(Word(seed.s_west,28,16),400-250,300,40)
    pygame.display.flip() #refresh screen

# for quick loading from interactive python.
# load python, 'from run import * ; ff()' thats it.
# you can then call functions, change vars, etc.
def ff():
    global seed
    seedtxt='hello'
    start_vec_thread(seedtxt)
    seed=Word(seedtxt,34,14)
    start_key_thread()
    update_screen(seed)

if __name__ == "__main__":
    try: seedtxt = sys.argv[1]
    except: print("Usage: "+sys.argv[0]+" <seed word>"); sys.exit()
    start_vec_thread(seedtxt)
    seed=Word(seedtxt,34,14)
    start_key_thread()
    update_screen(seed)
    while True:
            sleep(.5)

