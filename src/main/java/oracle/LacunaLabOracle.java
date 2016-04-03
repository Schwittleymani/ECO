package oracle;

import oracle.cli.CLI;
import oracle.markov.MarkovChain;
import oracle.markov.MarkovChain2;
import oracle.markov.MarkovQueue;
import processing.core.PApplet;

import java.awt.event.KeyEvent;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Vector;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.util.Arrays;

/**
 * Created by mrzl on 31.03.2016.
 */
public class LacunaLabOracle extends PApplet {

    public static String markovJsonFileName = "lacuna_markov_export-order";
    private CLI cli;
    private ArrayList< MarkovChain > markovChains;

    public void settings () {
        size( 640, 480 );
        //fullScreen( );
    }

    public void setup () {
        cli = new CLI( this );
        markovChains = new ArrayList<>( );

        //saveConfiguration();
        loadConfiguration();
        noCursor( );
    }

    private String loadText ( String fileName ) {
        String completeText = "";
        try ( Stream< String > stream = Files.lines( Paths.get( fileName ) ) ) {

            String s = stream.collect( Collectors.joining( ) );
            completeText += s;

        } catch ( IOException e ) {
            e.printStackTrace( );
        }

        return completeText.toLowerCase( );
    }

    public void draw () {
        background( 0 );
        cli.draw( );
    }

    public void keyPressed () {
        if ( key == CODED ) {
            switch ( keyCode ) {
                case KeyEvent.VK_F1:
                    cli.reset( );
                    break;
            }
        } else {
            switch ( key ) {
                case BACKSPACE:
                    cli.backspace( );
                    break;
                case ENTER:
                    if ( !cli.available( ) ) {
                        return;
                    }
                    String[] inputWords = cli.getLastLine( ).getText( ).toLowerCase( ).split( " " );
                    MarkovQueue queue = new MarkovQueue( inputWords.length - 2 );

                    for ( String s : inputWords ) {
                        queue.addLast( s );
                    }
                    String result = markovChains.get( queue.getOrder( ) - 1 ).generateSentence( queue );
                    if ( result.equals( "nothing" ) ) {
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

    private void saveConfiguration () {
        for ( int i = 1; i < 10; i++ ) {
            MarkovChain chain = new MarkovChain( i );
            chain.train( loadText( "lacuna_lab_texts.txt" ) );
            markovChains.add( chain );
            System.out.println( "Training chain with order " + i );
        }

        for ( MarkovChain chain : markovChains ) {
            String fileName = "lacuna_chain-" + chain.getOrder( ) + ".data";
            try {
                ObjectOutputStream obj_out = new ObjectOutputStream(
                        new FileOutputStream( fileName )
                );
                obj_out.writeObject( chain );
            } catch ( FileNotFoundException e ) {
                e.printStackTrace( );
            } catch ( IOException e ) {
                e.printStackTrace( );
            }
            System.out.println( "Saved markov chain to " + fileName );
        }

    }

    private void loadConfiguration () {
        try {
            for ( int i = 1; i < 10; i++ ) {
                String fileName = "lacuna_chain-" + i + ".data";
                FileInputStream f_in = new FileInputStream(fileName);
                ObjectInputStream obj_in = new ObjectInputStream (f_in);
                Object obj = obj_in.readObject();

                if (obj instanceof MarkovChain )
                {
                    markovChains.add( (MarkovChain) obj );
                }

                System.out.println( "Loaded from " + fileName + ". With order " + markovChains.get( markovChains.size() - 1 ).getOrder() );
            }
        } catch ( FileNotFoundException e ) {
            e.printStackTrace( );
        } catch ( ClassNotFoundException e ) {
            e.printStackTrace( );
        } catch ( IOException e ) {
            e.printStackTrace( );
        }
        System.out.println( "Loaded markov chain from " + markovJsonFileName );
    }


}
