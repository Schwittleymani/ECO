package oracle;

import oracle.cli.CLI;
import oracle.markov.MarkovChain;
import oracle.markov.MarkovChain2;
import oracle.markov.MarkovQueue;
import processing.core.PApplet;

import java.awt.event.KeyEvent;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.util.Arrays;

/**
 * Created by mrzl on 31.03.2016.
 */
public class LacunaLabOracle extends PApplet {

    public static String markovJsonFileName = "lacuna_markov_export.json";
    private CLI cli;
    private MarkovChain markov;

    public void settings() {
        size( 640, 480 );
        fullScreen( );
    }

    public void setup() {
        cli = new CLI( this );
        markov = new MarkovChain( 1 );
        //markov.train( loadText( "lacuna_lab_texts.txt" ) );
        //saveConfiguration();
        loadConfiguration();
        noCursor();
    }

    private String loadText( String fileName ) {
        String completeText = "";
        try ( Stream< String > stream = Files.lines( Paths.get( fileName ) )) {

            String s = stream.collect( Collectors.joining( ) );
            completeText += s;

        } catch (IOException e) {
            e.printStackTrace();
        }

        return completeText.toLowerCase();
    }

    public void draw() {
        background( 0 );
        cli.draw();
    }

    public void keyPressed( ) {
        if( key == CODED ){
            switch( keyCode ) {
                case KeyEvent.VK_F1:
                    cli.reset();
                    break;
            }
        } else {
            switch( key ) {
                case BACKSPACE:
                    cli.backspace();
                    break;
                case ENTER:
                    if( cli.getLastLine().getText().equals(CLI.inputPreChars)) {
                        return;
                    }
                    String [] inputWords = cli.getLastLine().getText().toLowerCase().split( " " );
                    MarkovQueue queue = new MarkovQueue( 1 );

                    for( String s : inputWords ) {
                        queue.push( s );
                    }

                    String result = markov.generateSentence( queue );
                    //println(Arrays.toString(inputWords));
                    if( result.equals( inputWords[2] + " " )) {
                        result = "oracle: we don't care about " + inputWords[ 2 ];
                    }
                    cli.finish( result );
                    break;
                case TAB:
                case DELETE:
                    break;
                case ESC:
                    cli.reset( );
                    break;
                case 'e':
                    // export markov chain to json
                    //saveConfiguration( );
                case 'l':
                    // load markov chain from json
                    //loadConfiguration();
                default:
                    cli.type( key );
                    break;
            }
        }
    }

    private void saveConfiguration() {
        try {
            markov.saveToFile( markovJsonFileName );
        } catch ( IOException e ) {
            e.printStackTrace( );
        }
        System.out.println( "Saved markov chain to " + markovJsonFileName );
    }

    private void loadConfiguration() {
        try {
            markov.loadFromFile( markovJsonFileName );
        } catch ( FileNotFoundException e ) {
            e.printStackTrace( );
        }
        System.out.println( "Loaded markov chain from " + markovJsonFileName );
    }


}
