import numpy as np
import math
import random



    

NUM_PICTURES = 20
NUM_ITERATIONS = math.ceil(NUM_PICTURES*NUM_PICTURES*math.log2(NUM_PICTURES))

rank =  [[  [] for col in range(NUM_PICTURES)] for row in range(NUM_PICTURES)]
images = np.random.rand(NUM_PICTURES)


def compare(targetIndex, index1, index2):
    if (math.fabs(images[targetIndex]- images[index1]) <= math.fabs(images[targetIndex]- images[index2])):
        winner = index1
        loser = index2
    else:
        winner = index2
        loser = index1
        
    print("{}: {} is closer than {}".format(images[targetIndex],images[winner],images[loser]))
    return (winner,loser)

print(images)


for i in range(NUM_ITERATIONS):  
    target = i % NUM_PICTURES
    index1 = np.random.randint(NUM_PICTURES)
    while(index1 == target):
        index1 = np.random.randint(NUM_PICTURES)
    index2 = np.random.randint(NUM_PICTURES)
    while((index2 == target) | (index2 == index1)):
        index2 = np.random.randint(NUM_PICTURES)
        
    print("target: {}\nindex1:{}\nindex2:{}".format(target, index1, index2))
    (winner, loser) = compare(target,index1,index2)
    rank[target][winner].append(loser)
    
print(rank)