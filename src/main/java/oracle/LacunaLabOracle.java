package oracle;

import oracle.cli.CLI;
import oracle.markov.MarkovChain;
import oracle.markov.MarkovQueue;
import processing.core.PApplet;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Created by mrzl on 31.03.2016.
 */
public class LacunaLabOracle extends PApplet {

    public static String markovJsonFileName = "lacuna_markov_export.json";
    private CLI cli;
    private MarkovChain markov;

    public void settings() {
        size( 640, 480 );
        //fullScreen( );
    }

    public void setup() {
        cli = new CLI( this );
        markov = new MarkovChain();
        //markov.train( loadText( "lacuna_lab_texts.txt" ) );
        loadConfiguration();
    }

    private String loadText( String fileName ) {
        String completeText = "";
        try ( Stream< String > stream = Files.lines( Paths.get( fileName ) )) {

            String s = stream.collect( Collectors.joining( ) );
            completeText += s;

        } catch (IOException e) {
            e.printStackTrace();
        }

        return completeText;
    }

    public void draw() {
        background( 0 );
        cli.draw();
    }

    public void keyPressed( ) {
        if( key == CODED ){
            switch( keyCode ) {
            }
        } else {
            switch( key ) {
                case BACKSPACE:
                    cli.backspace();
                    break;
                case ENTER:
                    MarkovQueue queue = new MarkovQueue( 1 );
                    String [] inputWords = cli.getLastLine().getText().split( " " );
                    queue.addFirst( inputWords[ 0 ] );
                    cli.finish( markov.generateSentence( queue ) );
                    break;
                case TAB:
                case DELETE:
                    break;
                case ESC:
                    cli.reset( );
                    break;
                case 'e':
                    // export markov chain to json
                    saveConfiguration( );
                case 'l':
                    // load markov chain from json
                    loadConfiguration();
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

    public void exit() {
        // simply overriding
    }
}
