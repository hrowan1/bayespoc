import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from matplotlib.animation import PillowWriter
import cv2
import urllib.request
import numpy as np
from skimage import io
import datetime
from celluloid import Camera
import gc
import math

with open('bayes/1.json') as x:
    data = json.load(x)
    blueTeam = data['payload']['payload']['payload']['teams'][0]['urn']
    redTeam = data['payload']['payload']['payload']['teams'][1]['urn']

champUrl = 'http://ddragon.leagueoflegends.com/cdn/12.12.1/data/en_US/champion.json'
with urllib.request.urlopen(champUrl) as url:
    championData = json.loads(url.read())

blueTeamPlayers = []
redTeamPlayers = []
blueTeamChampions = []
redTeamChampions = []
blueWards = []
redWards = []

xPos = [[] for i in range(10)]
yPos = [[] for i in range(10)]

timeArray = []


for i in range(5):
    blueTeamPlayers.append(data['payload']['payload']['payload']['teams'][0]['participants'][i]['name'])
    redTeamPlayers.append(data['payload']['payload']['payload']['teams'][1]['participants'][i]['name'])
    
for i in range(1,int(400)):

    xList = []
    yList = []
    with open('bayes/{0}.json'.format(str(i))) as x:
        data = json.load(x)

        if data['payload']['payload']['action'] == 'PLACED_WARD':
            timeStamp = int(data['payload']['payload']['payload']['gameTime']/1000)
            m, s = divmod(timeStamp, 60)
            if data['payload']['payload']['payload']['placerTeamUrn'] == blueTeam:
                blueWards.append([data['payload']['payload']['payload']['position'][0],
                                  data['payload']['payload']['payload']['position'][1]])
                
            elif data['payload']['payload']['payload']['placerTeamUrn'] == redTeam:
                redWards.append([data['payload']['payload']['payload']['position'][0],
                                 data['payload']['payload']['payload']['position'][1]])

        else:
            try:
                for zi in range(10):
                    xPos[zi].append(data['payload']['payload']['payload']['positions'][zi]['position'][0])
                    yPos[zi].append(data['payload']['payload']['payload']['positions'][zi]['position'][1])

                timeStamp = int(data['payload']['payload']['payload']['gameTime']/1000)
                m, s = divmod(timeStamp, 60)
                timeArray.append('{:02d}:{:02d}'.format(m,s))
                blueWards.append(['',''])
                redWards.append(['',''])
            except:
                pass

            try:
                for z in range(5):
                    champId = data['payload']['payload']['payload']['teams'][0]['participants'][z]['championId']
                    if champId != 0:
                        for xi in championData['data']:
                            if championData['data'][xi]['key'] == str(champId):
                                blueTeamChampions.append(championData['data'][xi]['id'])
                for z in range(5):
                    champId = data['payload']['payload']['payload']['teams'][1]['participants'][z]['championId']
                    if champId != 0:
                        for xi in championData['data']:
                            if championData['data'][xi]['key'] == str(champId):
                                redTeamChampions.append(championData['data'][xi]['id'])
            except:
                pass 

xP = [[] for i in range(10)]
yP = [[] for i in range(10)]

fig, ax = plt.subplots()
camera = Camera(fig)
img = plt.imread('map12.png')

image = io.imread(r'ChampPortrait/{0}.png'.format(blueTeamChampions[0]))
image1 = io.imread(r'ChampPortrait/{0}.png'.format(blueTeamChampions[1]))
image2 = io.imread(r'ChampPortrait/{0}.png'.format(blueTeamChampions[2]))
image3 = io.imread(r'ChampPortrait/{0}.png'.format(blueTeamChampions[3]))
image4 = io.imread(r'ChampPortrait/{0}.png'.format(blueTeamChampions[4]))

image5 = io.imread(r'ChampPortrait/{0}.png'.format(redTeamChampions[0]))
image6 = io.imread(r'ChampPortrait/{0}.png'.format(redTeamChampions[1]))
image7 = io.imread(r'ChampPortrait/{0}.png'.format(redTeamChampions[2]))
image8 = io.imread(r'ChampPortrait/{0}.png'.format(redTeamChampions[3]))
image9 = io.imread(r'ChampPortrait/{0}.png'.format(redTeamChampions[4]))

links = [0 for i in range(4)]
pLinks = [0 for i in range(4)]

#print(links)
def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    dist = np.sum((nodes-node)**2, axis=1)
    #print((nodes-node)**2)
    #print(dist)
    links[np.argmin(dist)] += 1
    return nodes[np.argmin(dist)]

currentWards = []

def animate(i):
    #for vi in range(5):
    #    xP[vi].append(xPos[vi][i])
    #    yP[vi].append(yPos[vi][i])
    
    ax.clear()

    jungler1 = [xPos[1][i], yPos[1][i]]
    blueRest = [[xPos[0][i],yPos[0][i]],
            [xPos[2][i],yPos[2][i]],
            [xPos[3][i],yPos[3][i]],
            [xPos[4][i],yPos[4][i]],
            ]
    
    closest = closest_node(jungler1, blueRest)
    #if i>=180:
    if(math.sqrt(((jungler1[0]-closest[0])**2)+((jungler1[1]-closest[1])**2)) <= 2000):
        ax.plot([jungler1[0],closest[0]],[jungler1[1],closest[1]], color='white')

    jungler2 = [xPos[6][i], yPos[6][i]]
    redRest = [[xPos[5][i],yPos[5][i]],
            [xPos[7][i],yPos[7][i]],
            [xPos[8][i],yPos[8][i]],
            [xPos[9][i],yPos[9][i]],
            ]

    closest = closest_node(jungler2, redRest)
    #ax.plot([jungler2[0],closest[0]],[jungler2[1],closest[1]], color='white')
    
    #ax.plot(xP[0],yP[0], color='yellow', marker='o' ,markevery=len(xP)-1, markersize=0)
    #ax.plot(xP[1],yP[1], color='blue', marker='o' ,markevery=len(xP)-1, markersize=0)
    #ax.plot(xP[2],yP[2], color='green', marker='o' ,markevery=len(xP)-1, markersize=0)
    #ax.plot(xP[3],yP[3], color='red', marker='o' ,markevery=len(xP)-1, markersize=0)
    #ax.plot(xP[4],yP[4], color='white', marker='o' ,markevery=len(xP)-1, markersize=0)
    #ax.plot(xP[5],yP[5], color='yellow', marker='o' ,markevery=len(xP)-1, markersize=0)
    #ax.plot(xP[6],yP[6], color='blue', marker='o' ,markevery=len(xP)-1, markersize=0)
    #ax.plot(xP[7],yP[7], color='green', marker='o' ,markevery=len(xP)-1, markersize=0)
    #ax.plot(xP[8],yP[8], color='red', marker='o' ,markevery=len(xP)-1, markersize=0)
    #ax.plot(xP[9],yP[9], color='white', marker='o' ,markevery=len(xP)-1, markersize=0)
    
    ax.set_xlim([0,14870])
    ax.set_ylim([0,14980])
    ax.imshow(img,extent=[0,14870,0,14980])
    
    ax.imshow(image, extent = [xPos[0][i]-500,xPos[0][i]+500,yPos[0][i]-500,yPos[0][i]+500])
    ax.imshow(image1, extent = [xPos[1][i]-500,xPos[1][i]+500,yPos[1][i]-500,yPos[1][i]+500])
    ax.imshow(image2, extent = [xPos[2][i]-500,xPos[2][i]+500,yPos[2][i]-500,yPos[2][i]+500])
    ax.imshow(image3, extent = [xPos[3][i]-500,xPos[3][i]+500,yPos[3][i]-500,yPos[3][i]+500])
    ax.imshow(image4, extent = [xPos[4][i]-500,xPos[4][i]+500,yPos[4][i]-500,yPos[4][i]+500])

    #ax.imshow(image5, extent = [xPos[5][i]-500,xPos[5][i]+500,yPos[5][i]-500,yPos[5][i]+500])
    #ax.imshow(image6, extent = [xPos[6][i]-500,xPos[6][i]+500,yPos[6][i]-500,yPos[6][i]+500])
    #ax.imshow(image7, extent = [xPos[7][i]-500,xPos[7][i]+500,yPos[7][i]-500,yPos[7][i]+500])
    #ax.imshow(image8, extent = [xPos[8][i]-500,xPos[8][i]+500,yPos[8][i]-500,yPos[8][i]+500])
    #ax.imshow(image9, extent = [xPos[9][i]-500,xPos[9][i]+500,yPos[9][i]-500,yPos[9][i]+500])
    
    plt.title(timeArray[i])
    ax.axis('off')

    if blueWards[i][0] != '':
        currentWards.append([blueWards[i][0],blueWards[i][1],'blue'])
    elif redWards[i][0] != '':
        currentWards.append([redWards[i][0],redWards[i][1],'red'])

    for i in currentWards:
        if i[2] == 'blue':
            ax.scatter(x=i[0],y=i[1], c='cyan', edgecolors='black')
        else:
            ax.scatter(x=i[0],y=i[1], c='red', edgecolors='black')
    gc.collect()

ani = animation.FuncAnimation(fig, animate, frames = len(xPos[0]), interval = 1, repeat = False, save_count=0)

ani.save("TLI.gif", dpi=150, writer=PillowWriter(fps=60))

plt.show()

#print(links)
