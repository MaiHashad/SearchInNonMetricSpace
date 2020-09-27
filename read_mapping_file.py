pics = []
filepath = 'pic_mapping.txt'  
with open(filepath) as fp:  
   line = "1"
   
   while line:
       #print(line.strip())
       line = line.strip
       #line = line.replace(" ","")
       line = fp.readline()
       if line == '':
            break
       str = line.strip().split(":")
       print(str)
       pics.append(str[1].replace(" ",""))
 
print(pics) 