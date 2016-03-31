package oracle.test;

import oracle.markov.MarkovChain;
import oracle.markov.MarkovQueue;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Collections;
import java.util.stream.Collector;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Created by mrzl on 31.03.2016.
 */
public class MarkovTest {
    public static void main ( String[] args ) {
        String fileName = "lacuna_lab_texts.txt";
        String completeText = "";
        try ( Stream< String > stream = Files.lines( Paths.get( fileName ) )) {

            String s = stream.collect( Collectors.joining() );
            completeText += s;

        } catch (IOException e) {
            e.printStackTrace();
        }

        MarkovChain mc = new MarkovChain( 1 );
        mc.train( completeText );

        String input = "For me";

        String[] seed = input.split( "\\s+" );
        Collections.reverse( Arrays.asList( seed ) ); // somehow this needs to be reversed in order to be right
        MarkovQueue queue = new MarkovQueue( seed );
        System.out.println( mc.generateSentence( queue ) );
    }
}
