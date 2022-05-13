import time
from operator import length_hint
file = open(r"two/part-00000")
lines=file.readlines()
print("Loading ..")
time.sleep(3)
#print(lines)
#print(length_hint (lines))
freshLines=[]
for line in lines:
   line1= line.replace("(","")
   line2=line1.replace(")","")
   #line3=line2.replace("\n","")
   freshLines.append(line2)
print ("This first part of Data has been processed")
file2 = open(r"two/part-00001")
lines2=file2.readlines()
#print(lines)
#print(length_hint (lines))
i=0
for line0 in lines2:
   line11= line0.replace("(",str(i)+",")
   line22=line11.replace(")","")
   #line33=line22.replace("\n","")
   freshLines.append(line22)
   i=i+1
print ("This second part of Data has been processed")


filename = 'two/part-00000Processed'
with open(filename, 'w', newline="") as fileProcess:
   fileProcess.writelines(freshLines)