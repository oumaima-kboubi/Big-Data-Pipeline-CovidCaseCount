import time
from operator import length_hint
file = open(r"one/part-00000")
lines=file.readlines()
print(lines)
print("Loading ..")
time.sleep(3)
#print(length_hint (lines))
freshLines=[]
i=0
for line in lines:
   line1= line.replace("(",str(i)+",")
   line2=line1.replace(")","")
   #line3=line2.replace("\n","")
   freshLines.append(line2)
   i=i+1

print ("This Data has been processed")
#print(freshLines)

filename = 'one/part-00000Processed'
with open(filename, 'w', newline="") as fileProcess:
   fileProcess.writelines(freshLines)