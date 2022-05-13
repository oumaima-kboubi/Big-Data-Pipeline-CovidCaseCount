//package tn.insat.bigdataPipeline;

import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Properties;
import java.util.Arrays;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.ConsumerRecord;

public class SimpleConsumer {
    public static void main(String[] args) throws Exception {
        if(args.length == 0){
            System.out.println("Entrer le nom du topic");
            return;
        }
        String topicName = args[0].toString();
        Properties props = new Properties();

        props.put("bootstrap.servers", "localhost:9092");
        props.put("group.id", "test");
        props.put("enable.auto.commit", "true");
        props.put("auto.commit.interval.ms", "1000");
        props.put("session.timeout.ms", "30000");
        props.put("key.deserializer",
                "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer",
                "org.apache.kafka.common.serialization.StringDeserializer");

        KafkaConsumer<String, String> consumer = new KafkaConsumer <String, String>(props);

        // Kafka Consumer va souscrire a la liste de topics ici
        consumer.subscribe(Arrays.asList(topicName));

        // Afficher le nom du topic
        System.out.println("Souscris au topic " + topicName);
        int i = 0;
        File csvOutputFile = new File("result.csv");
        while (true) {
            ConsumerRecords<String, String> records = consumer.poll(100);
            for (ConsumerRecord<String, String> record : records) {
                try (FileWriter fr = new FileWriter(csvOutputFile, true);
                     PrintWriter pw = new PrintWriter(fr);) {
                    String res="";
                    if(record.value().equals("NaN")) {
                         res = "0" + "," + record.key();
                    }else{
                         res =  record.value()+","+record.key();
                    }
                    pw.println(res);
                    System.out.println("Instance (" + res + ") added ");

                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }

    }
}
