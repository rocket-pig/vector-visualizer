# vector-visualizer
Visualize / explore word2vec datasets with pygame 
\
\
![foo](https://darknesseverytime.live/mirror/sample.gif "title")  

_"Surf" through word-relatedness in wide-eyed amazement!_  
_Astonish your friends, scare your neighbors, earn the respect of your spouse!_
## Intro
"Word2vec takes as its input a large corpus of text and produces a vector space, typically of several hundred dimensions, with each unique word in the corpus being assigned a corresponding vector in the space. Word vectors are positioned in the vector space such that words that share common contexts in the corpus are located in close proximity to one another in the space."  ...*Wow*, right? I was already downloading the .vec file before I understood how I could use it. I wanted to *see* 300 dimensions, and there wasn't really any way to do that, so I began writing this. I know it doesn't even scratch the surface of ***300-D***, but hey, us mere mortals *aren't ready for the truth* 


## Getting started
You'll need gensim, pygame installed and of course a dataset. If you're already there, simply:  
`git clone https://github.com/rocket-pig/vector-visualizer`\
`cd vector-visualizer`\
open main.py and set the proper location of your .vec file.
run with\
`python main.py 'seed'`\
...once loaded, ***use the keyboard arrow keys*** to surf! ie, 
pressing left will bring the word to the left to the center. You'll be in word-heaven in no time.  



## Getting a dataset
the one shown above is the wikipedia word vector dataset: (104MB download, 280MB unzipped)  
[wiki.simple.vec.zip](https://darknesseverytime.live/mirror/wiki.simple.vec.zip)  
or mirror [wiki.simple.vec.zip](https://drive.google.com/uc?id=1u79f3d2PkmePzyKgubkbxOjeaZCJgCrt&export=download)  
...you're of course free to plug any .vec file into this. If you use other ones, I'd love to see/hear about the results!
EDIT: years have passed and both those links are gone.  Here they are these days: [link](https://wikipedia2vec.github.io/wikipedia2vec/pretrained/)

## Installing gensim:
`pip install -U gensim`\
or visit their [github](https://github.com/RaRe-Technologies/gensim) for more.

## Installing pygame:
`pip install pygame`\
Or visit for more:  
[Github: pygame](https://github.com/pygame/pygame)\
[Pygame: Downloads](https://www.pygame.org/download.shtml)

## Other stuff
I'm all about forks, pull requests, rants, raves, complaints, death threats you name it
