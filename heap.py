'''
class Node: 

    def __init__(self, depth, parent = None, left = None, right = None):
        
        self.parent = parent
        self.depth = depth
        self.left = left
        self.right = right
'''        

Data=[0,3,5,8,4,9,14,22,25,29,35,46,49,52,57,59,62,65,78,89]
Data = [i for i in range(0,40)]
import random
query = 20

def comp(query,i,j):
    if abs(query-i)<abs(query-j):
        return i,j
    else:
        return j,i
Rank_Query = []
for i in Data:
    Rank_Query.append([])
        
for x in range(100000):
    i = random.randint(0,len(Data)-1)
    while i == query:
        i = random.randint(0,len(Data)-1)
    j = query
    #y = Data[i]
    #z = Data[i]
    while i == j or j == query:
        j = random.randint(0,len(Data)-1)
        z = Data[j]
    win,lose = comp(query,i,j)
    '''print("rank vector")
    print(Rank_Query)
    print("winner:")
    print(win)
    print(Data[win])
    print("loser:")
    print(lose)
    print(Data[lose])'''
    Rank_Query[win].append(lose)

print(Rank_Query)
    

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
        if index+index+1 < len(array) and array[index] in Rank_Query[left]:
            smallest = index+index+1
            #left<array[index]:
            #let Rank Query represents rank array of pics to query. Let Rank represent rank array of pics to pics
            #if array[index] in Rank[i][left] (i is pic num needed as input for heapify)
            #if array[index] in Rank_Query[left]
        else:
            smallest = index
            
        if index+index+2 < len(array) and array[smallest] in Rank_Query[right]:
            smallest = index+index+2
            #right<array[smallest]
            #if array[smallest] in Rank[i][right] (i is pic num needed as input for heapify)
            #if array[index] in Rank_Query[right]
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
    
x = [x for x in range(40)] 
print(x)      
ordered = BuildHeap(x) 
print(ordered)
depth = ""
printtree(ordered,0,depth)
index = 0
min = extract_min(ordered)
print("min: " ,min)
ordered = BuildHeap(x) 
print(ordered)
depth = ""
printtree(ordered,0,depth)   