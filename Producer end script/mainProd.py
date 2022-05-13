import os
import time

#Please Execute mainCons.py file to run the consumer before the producer in an other shell

#Deleting files from previous data processing manipulations
os.system('hadoop fs -rm preprocessedCovidData.csv')
#Data Preprocessing
os.system('python .\preprocessRegion.py')
#Compile then run the producer
os.system('javac -cp "$KAFKA_HOME/libs/*":. SimpleProducer.java')
os.system('java -cp "$KAFKA_HOME/libs/*":. SimpleProducer Covid-Prdict')
#Wait for 5 seconds to make sure that the consumer has completed its task
time.sleep(10)
#Load the result file produced by the consumer (clean dataset) in hadoop hdfs
os.system('hadoop fs -put -f result.csv input')
#Delete the existant output directories from previous manipulations
os.system('hadoop fs -rm -r output')
os.system('hadoop fs -rm -r output2')
os.system('hadoop fs -ls')
time.sleep(10)
#Run the spark task localy to predict the covid19 case number in every region 
os.system('echo "First Option: Running the spark task localy"')
time.sleep(5)
os.system('spark-submit  --class tn.insat.bigdataPipeline.predictCaseCovid --master local --driver-memory 4g --executor-memory 2g --executor-cores 1 bigdata-pipeline-1.jar input/result.csv output')
#Show the results
os.system('hadoop fs -ls')
time.sleep(5)
os.system('hadoop fs -ls output')
time.sleep(5)
os.system('hadoop fs -cat output/part-00000')
time.sleep(10)
#Run the spark task in cluster mode to predict the covid19 case number in every region 
os.system('echo "Second Option: Running the spark task in cluster mode using yarn"')
time.sleep(5)
os.system('spark-submit  --class tn.insat.bigdataPipeline.predictCaseCovid --master yarn --deploy-mode cluster --driver-memory 4g --executor-memory 2g --executor-cores 1 bigdata-pipeline-1.jar input/result.csv output2')
#Show the results
os.system('hadoop fs -ls')
time.sleep(3)
os.system('hadoop fs -ls output2')
time.sleep(3)
os.system('hadoop fs -cat output2/part-00000')
time.sleep(3)
os.system('hadoop fs -cat output2/part-00001')

#Save it to HBase from the first method
os.system('hadoop fs -get output/part-00000 one')
os.system('python3 hbaseSaverOne.py')
os.system('hadoop fs -put  one/part-00000Processed  output')
time.sleep(2)
os.system('echo "the preprocessing of the first option is done"')
time.sleep(3)
os.system('echo "Removing the part-00000 original file is permited if we do not want to save the data in the file along with the processed data"')
time.sleep(4)
os.system('echo "in out case we will be removing the part-00000 file in order to see thee diffrence in the timestamp')
os.system('hadoop fs -rm output/part-00000')
time.sleep(10)
os.system("hbase org.apache.hadoop.hbase.mapreduce.ImportTsv  -Dimporttsv.separator=','  -Dimporttsv.columns=HBASE_ROW_KEY,covidcases:region,covidcases:casenumber  covid_case_prediction output")
#Save it to HBase from the second method
os.system('hadoop fs -get output2/part-00000 two')
os.system('hadoop fs -get output2/part-00001 two')
os.system('python3 hbaseSaverTwo.py')
os.system('hadoop fs -put  one/part-00000Processed  output2')
time.sleep(2)

os.system('echo "the preprocessing of the first option is done"')
time.sleep(3)
os.system('echo "Removing the part-00000 and part-00001 original files is permited if we do not want to save the data in the file along with the processed data"')
time.sleep(4)
os.system('echo "in out case we will be removing the part-00000 and part-00001 files in order to see thee diffrence in the timestamp')
os.system('hadoop fs -rm output2/part-00000')
os.system('hadoop fs -rm output2/part-00001')
time.sleep(10)
os.system("hbase org.apache.hadoop.hbase.mapreduce.ImportTsv  -Dimporttsv.separator=','  -Dimporttsv.columns=HBASE_ROW_KEY,covidcases:region,covidcases:casenumber  covid_case_prediction_two output2")

os.system('echo "The Covid Case Prediction is done! Thank for tuning by"')