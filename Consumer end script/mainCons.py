import os

#Compile then run the consumer in order to clean the dataset and complete the missing values
os.system('javac -cp "$KAFKA_HOME/libs/*":. SimpleConsumer.java')
os.system('java -cp "$KAFKA_HOME/libs/*":. SimpleConsumer Covid-Predict')