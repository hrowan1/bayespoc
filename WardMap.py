import json
import matplotlib.pyplot as plt
import numpy as np

blueWards = []
redWards = []

with open('bayes/1.json') as x:
    data = json.load(x)
    blueTeam = data['payload']['payload']['payload']['teams'][0]['urn']
    redTeam = data['payload']['payload']['payload']['teams'][1]['urn']

for i in range(1,4090):
    with open('bayes/{0}.json'.format(str(i))) as x:
        data = json.load(x)
        if data['payload']['payload']['action'] == 'PLACED_WARD':
            if data['payload']['payload']['payload']['gameTime'] < 200000:
                if data['payload']['payload']['payload']['placerTeamUrn'] == blueTeam:
                    blueWards.append([data['payload']['payload']['payload']['position'][0],
                                  data['payload']['payload']['payload']['position'][1]])
                elif data['payload']['payload']['payload']['placerTeamUrn'] == redTeam:
                    redWards.append([data['payload']['payload']['payload']['position'][0],
                                  data['payload']['payload']['payload']['position'][1]])



#print(wards)
            
def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    dist_2 = np.sum((nodes-node)**2, axis=1)
    return np.argmin(dist_2)
        
fig, ax = plt.subplots()
img = plt.imread('map12.png')

ax.imshow(img, extent=[0,14870,0,14980])

n = [5234,3423]
close = closest_node(n, blueWards)

#ax.plot([n[0],blueWards[close][0]],[n[1],blueWards[close][1]], color='white')

for i in range(len(blueWards)):
    ax.scatter(x=blueWards[i][0], y=blueWards[i][1], c='cyan', edgecolors='black')

for i in range(len(redWards)):
    ax.scatter(x=redWards[i][0], y=redWards[i][1], c='red', edgecolors='black')

plt.show()
