import csv
file = open("full_grouped_virgule.csv")
csvreader = csv.reader(file)
header = next(csvreader)
newFieldheader="Predicted Cases for tomorrow"
newHeader=[header[0],newFieldheader]
#print(newHeader)
rows = []

for row in csvreader:
    #predictedCases=int(row[1])+int(row[5])
    #print(predictedCases)
    newRow=[row[1],row[6],row[9]]
    #print(newRow)
    rows.append(newRow)
#print(rows)
file.close()

filename = 'preprocessedCovidData.csv'
with open(filename, 'w', newline="") as file:
    csvwriter = csv.writer(file) # 1. create a csvwriter object
    #csvwriter.writerow(newHeader) # 2. write the header
    csvwriter.writerows(rows) # 3. write the rest of the data