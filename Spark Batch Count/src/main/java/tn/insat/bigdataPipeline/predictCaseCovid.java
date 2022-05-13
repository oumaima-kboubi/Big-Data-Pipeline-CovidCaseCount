package tn.insat.bigdataPipeline;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import scala.Tuple2;

import static jersey.repackaged.com.google.common.base.Preconditions.checkArgument;
public class predictCaseCovid {
    private static final Logger LOGGER = LoggerFactory.getLogger(predictCaseCovid.class);

    public static void main(String[] args) {
        checkArgument(args.length > 1, "Please provide the path of input file and output dir as parameters.");
        new predictCaseCovid().run(args[0], args[1]);
    }

    public String splitCaseRegion(String ligne){
        String[] ligneValue = ligne.split(",");
            //*extraction des données
          // Integer confirmedCases = Integer.parseInt(ligneValue[0]);
            String region = ligneValue[1];
            return region;
    }

    public Integer splitCaseConfirmed(String ligne){
        String[] ligneValue = ligne.split(",");
        //*extraction des données
        Integer confirmedCases = Integer.parseInt(ligneValue[0]);
       // String region = ligneValue[1];
        return confirmedCases;
    }

    public void run(String inputFilePath, String outputDir) {
       // String master = "local[*]";
        SparkConf conf = new SparkConf()
                .setAppName(predictCaseCovid.class.getName());
               // .setMaster(master);
        JavaSparkContext sc = new JavaSparkContext(conf);
        JavaRDD<String> textFile = sc.textFile(inputFilePath);
        JavaPairRDD<String, Long> counts ;
        JavaPairRDD<String,Long>  regionResult =  textFile
                        //.flatMap(s -> Arrays.asList(s.split(",")).iterator())
                        .map(line -> line.split(","))
                        .mapToPair(s -> new Tuple2<String,Long>(s[1], Long.parseLong(s[0])))
                        .reduceByKey((x, y) -> x + y);
                        //.foreach(t -> System.out.println(t._1 + " -> " + t._2));
        regionResult.saveAsTextFile(outputDir);

    }
}
