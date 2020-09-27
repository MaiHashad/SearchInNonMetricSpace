import math
import sys

def BuildHeap(array):
    num = int(len(array)/2)-1
    #print(num)
    unordered = array
    while num>=0:
        #print(num)
        #print(unordered)
        heapify(unordered,num)
        #print(unordered)
        num=num-1
    return unordered

def heapify(array,index):
    if index+index+1<len(array):
    
        left=array[index+index+1]
        
        if index +index + 2>=len(array):
            right = None
        else:
            right=array[index+index+2]
            
        smallest = None 
        if index+index+1 < len(array) and left<array[index]:
            smallest = index+index+1
        else:
            smallest = index
            
        if index+index+2 < len(array) and right<array[smallest]:
            smallest = index+index+2
        
        #print(array)
        #print(smallest)
        if smallest != index:
            
            temp = array[smallest]
            array[smallest] = array[index]
            array[index] = temp
            return heapify(array,smallest)
        return array

def printtree(array,index,depth):
    print("value: " + depth + str(array[index]))
    #print("index: ",index)
    depth = depth + " "
    if index+index+1 < len(array):
        printtree(array,index+index+1,depth)
    if index+index+2 < len(array):
        printtree(array,index+index+2,depth)
    
def extract_min(array):
    min = array[0]
    array[0] = array[len(array)-1]
    array.pop()
    heapify(array,0)
    return min
'''    
Vx = [[[2],[2],[1]],
      [[2],[2],[1]],
      [[2],[3],[3]],
      [[2],[3],[4]]
      ]'''
Vx = [[1,1,1,1],
      [1,1,2,2],
      [0,0,2,3]]
D = 3     
S = [[1],[1,2],[0,2,3]]
Data = [0,1,2,3]
M = 3
L1 = []
L = []
Vq = []
for i in range(0,M):
    if i == 0:
        L1.append(S[i])
        
        #Lx2 = y pt in S2 where Vy1 is in Lx1
    else:
        temp = []
        for y in S[i]:
            print("y= " + str(y))
            print(Vx[i-1][y])
            if Vx[i-1][y-1] in L[i-1]:
                #print(y)
                temp.append(y)
        L1.append(temp)       
    print(len(L1[i]))
    if len(L1[i]) == 0:
        print("Fail")
        sys.exit()
    
    H = BuildHeap(L1[i])
    temp2 = []
    #to be determined
    for k in range(0,min(108*D*math.log2(len(Data)),len(L1[i]))):
            
        z = extract_min(H)
        temp2.append(z)
        if k == 0:
            Vq.append(z) 
                
        L.append(temp2)
print("closest=",Vq[M-1])