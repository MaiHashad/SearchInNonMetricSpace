import argparse
import math
import random
import numpy as np
import heap



parser = argparse.ArgumentParser()
parser.add_argument('d', type = int, help='Disorder Constant')
parser.add_argument('n', type = int, help='Number of Objects in Database')

args = parser.parse_args()
D = args.d
n = args.n


print("D:{}".format(D))
print("n:{}".format(n))
S = []
S.append([])


M = math.ceil(1 + math.log2(n)/math.log2(2*D))
print("M:{}".format(M))

gamma_tilde = [[  [] for col in range(n)] for row in range(M)]
gamma = [[  [] for col in range(n)] for row in range(M)]

# Build up the sets Si:
for i in range(1, M+1): # 1:M
    p = min(1,math.pow((2*D),(i-1))/n)
    S.append([])
    for j in range(1, n+1): # 1:n
        if(random.random() < p):
            S[i].append(j)
            
    print("P:{}".format(p))
    
    print(S[i])
    
# Check the size of S1:
if(len(S[1]) > (1 + math.sqrt(3*math.log(2*n)))):
    
    print((1 + math.sqrt(3*math.log(2*n))))
    print("Failed: 0")
    exit()

# Main algorithm loop
for i in range(1, M+1): # i is iteration number
    for x in range(1, n+1): # x is picture index
        #gamma.append([])
        #gamma_tilde.append([])
        if (i==1):
            for k in S[i]:
                gamma_tilde[i][x].append(k)
                print(gamma_tilde)
        else:
            for y in S[i]:
                if v[i][y] in gamma[i][x]:
                    gamma_tilde[i][x].append(y)
        if (len(gamma_tilde[i][x]) == 0):
            print("Failed: 1")
            exit()
        H = BuildHeap(gamma_tilde[i][x])
        for k in range(1,min(math.floor(108*D*math.log2(n)),len(H))+1):
            z = extract_min(H)
            gamma[i][x].append(z)
            if k == 1:
                v[i][x] = z