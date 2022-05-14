# Big-Data-Pipeline-CovidCaseCount

The pipeline goal is to count the latest COVID19 case number in each region worldwide from 22/01/2020 till 27/07/2020

<img src= "https://github.com/oumaima-kboubi/Big-Data-Pipeline-CovidCaseCount/blob/main/Big%20Data%20Pipeline%20Architecture.png" />

## The architecture details:

  * The Dataset extracted from Kaggle : https://www.kaggle.com/datasets/imdevskp/corona-virus-report?select=full_grouped.csv and has been modified by replacing the 0 by "NaN" for the sake of testing, so the file user as a data entry of the pipeline is ``/Kaggle Dataset/full_grouped_virgule.csv``

  * The Dataset is preprocessed by a python script in order to generate a new csv file containing just the needed attributes columns. The code file is ``/Kaggle Dataset Preprocessing/preprocessRegion.py``
 
  * The Kafka Producer will transfer the data stored in the dataset preprocessed to a consumer, this consumer will replace all the "NaN" values by 0 in order to provide to spark a valid dataset. The goals is to allow diffrent consumers(aka data scientists) listening to the same topic to treat the data and complete the missing value depending on the treated case. The Consumer code file  is ``/Kafka Producer-Consumer/SimpleConsumer.java`` and the Producer code file is ``/Kafka Producer-Consumer/SimpleProducer.java`` 

  * Spark Batch Job will count the covid case number in every region and store the result into HDFS. In this example, i tried to run spark localy and on a cluster using yarn too. The code file is in the full project ``/Spark Batch Count``

  * A python script will process the files stored in HDFS so that it can be stored in hbase. The goal here is that we can generate a python script that can store the result of the pipeline in diffrent databases (mongoDB or other ..). The code file is ``/Hbase Saver Preprocessing Script/hbaseSaverOne.py``, the second file in the same directory ``/Hbase Saver Preprocessing Script`` allows you tto safe in an other Hbase table

  * In order to view the result, you can simply go to hbase shell and scan the database and check the timestamp of the rows.


## How to run the pipeline

### The configuration needed
  * First of all you need to use this docker image (kafka, hbase config is ready ..) using this command: ``docker pull liliasfaxi/spark-hadoop:hv-2.7.2``. For more details about the configuration you can check : https://insatunisia.github.io/TP-BigData/tp1/

  * In the docker container you need to create certain directories and files as follows:
    * -Create a directory called ``pipeline`` where all the pipeline will be configured
    * -In the ``pipeline`` directory create these directories ``one`` et ``two``
    * -In the ``pipeline`` directory in the docker container copy using this command the files needed to run the pipeline ``docker cp FILENAME haddop-master:/root/pipeline/FILENAME``(on your windows CMD) and replace the ``FILENAME`` by the filename to copy, you need to copy these files : 
    * Hbase Saver ``Hbase Saver Preprocessing Script/hbaseSaverOne.py`` , ``Hbase Saver Preprocessing Script/hbaseSaverTwo.py``
    * The kafka consumer ``/Kafka Producer-Consumer/SimpleConsumer.java ``
    * The kafka producer ``/Kafka Producer-Consumer/SimpleProducer.java ``
    * The dataset ``full_grouped_virgule.csv``
    * The main files: ``Producer end script/mainProd.py`` et ``Consumer end script/mainCons.py``
    * The dataset preprocessing file ``/Kaggle Dataset Preprocessing/preprocessRegion.py``
    * The Spark Batch Job Jar File ``/Spark Batch Count/target/bigdata-pipeline-1.jar``
    
    
<img src= "https://github.com/oumaima-kboubi/Big-Data-Pipeline-CovidCaseCount/blob/main/Execution%20Screenshots/config1.png" />
    
  * In the HDFS create a directory called ``input``, ce fichier va contenir lors de l'exécution du pipeline le résultat du kafka consumer ``result.csv``.
  * Create in HBase the table where the data will be stored, access the hbase shell using this command ``hbase shell`` and the this command ``create 'covid_case_prediction','covidcases' `` and then ``create 'covid_case_prediction_two','covidcases' `` for the second table
  * Start by running the containers in the image pulled, kafka and hbase (the details are in the other TPs in the link above with simplified explication)
  * Run the file ``mainCons.py`` in the docker container in order to rub the kafka consumer
  <img src= "https://github.com/oumaima-kboubi/Big-Data-Pipeline-CovidCaseCount/blob/main/Execution%20Screenshots/config2.png" />
 
  * Run the file ``mainProd.py`` in the docker container (in an other CMD of course)
  
 * There you have it your pipeline is running!
-In order to verify the result all you habe to do is check the row added in the hbase table ``scan 'covid_case_prediction``
-Execute the ``mainProd.py`` and you will see that the timestamps changed because the data is saved again in the same hbase table.
 
## Execution Result

* The dataset has been processed and the kafka producer has sent all the data that has been received and processed by the kafka consumer and stored in the ``input`` directory as follows: 
  <img src= "https://github.com/oumaima-kboubi/Big-Data-Pipeline-CovidCaseCount/blob/main/Execution%20Screenshots/config4.png" />
  
* Now The Spark Job will run localy 
 <img src= "https://github.com/oumaima-kboubi/Big-Data-Pipeline-CovidCaseCount/blob/main/Execution%20Screenshots/config5.png" />
 
 * This is the result of the first spark batch job is stored in HDFS under the ``output`` directory, the same Spark Batch Job will run the on the cluster using yarn as follows
  <img src= "https://github.com/oumaima-kboubi/Big-Data-Pipeline-CovidCaseCount/blob/main/Execution%20Screenshots/config6.png" />
  
 * This is the result of the second run stored in HDFS under the directory ``output2``
   <img src= "https://github.com/oumaima-kboubi/Big-Data-Pipeline-CovidCaseCount/blob/main/Execution%20Screenshots/config7.png" />
   
 * The file stored in HDFS ``output/part-00000`` will be processed in order to be saved in hbase
    <img src= "https://github.com/oumaima-kboubi/Big-Data-Pipeline-CovidCaseCount/blob/main/Execution%20Screenshots/config8.png" />
    
 * And the same process goes for the files ``output2/part-00000`` and ``output2/part-00001`` 
    <img src= "https://github.com/oumaima-kboubi/Big-Data-Pipeline-CovidCaseCount/blob/main/Execution%20Screenshots/config9.png" />
    
 * The pipeline execution has come to an end 
     <img src= "https://github.com/oumaima-kboubi/Big-Data-Pipeline-CovidCaseCount/blob/main/Execution%20Screenshots/end.png" />
 
#### Now let's verify if the results are saved in hbase hbase or not

* The table state before executing the pipeline
 <img src= "https://github.com/oumaima-kboubi/Big-Data-Pipeline-CovidCaseCount/blob/main/Execution%20Screenshots/hbaseBefore.png" />
 
* The table state after executing the pipeline 
 <img src= "https://github.com/oumaima-kboubi/Big-Data-Pipeline-CovidCaseCount/blob/main/Execution%20Screenshots/hbaseAfter.png" />
 
Now We just have ti compare the timestap between the same rows before and after the execution

Thanks for tuning By :)

## Refrences
https://insatunisia.github.io/TP-BigData/
