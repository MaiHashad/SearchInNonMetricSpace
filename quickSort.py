import os
###NEED MERGE
#merge sort
#send to stack for jb's stuff



def compare(A,B):
    #add comparison to queue

    return True

def partition(list,low,high):
    i = (low - 1)
    x = list[high]
    for j in range(low,high):     #for j = p to r-1

        #if the compared value is bigger than the pivot value
        if compare(x,list[j]) == True:
        #if list[j]<=x:       #if the compared value is bigger than the pivot value
            i+= 1
            list[i],list[j] = list[j],list[i]
    list[i+1],list[high] = list[high],list[i+1]
    return (i + 1)

def quickSort(list,low,high):
    #if low is greater than high
    if compare(low, high):
    if low>=high:
        return list        #already sorted
    pivot = partition(list,low,high)
    quickSort(list,low,pivot - 1)      #sort everything before pivot
    quickSort(list,pivot + 1, high)#sort everything after pivot



###DRIVER
list = ["bob", "ben", "mai", "matt"]
print('list:')
print(list)
quickSort(list,0,len(list)-1)
print('sorted list:')
print(list)
