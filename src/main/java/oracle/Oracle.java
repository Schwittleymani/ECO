package oracle;

import oracle.cli.CLI;
import oracle.markov.MarkovChain;
import oracle.web.Webserver;
import processing.core.PApplet;

import java.awt.event.KeyEvent;
import java.io.File;
import java.util.ArrayList;
import java.util.Collections;

/**
 * Created by mrzl on 31.03.2016.
 */
public class Oracle extends PApplet{
    private CLI cli;
    private MarkovManager markov;
    private ArrayList< MarkovManager > markovs;

    OracleLogger logger;
    Settings settings;

    long millisLastInteraction;

    boolean startWebserver;
    Webserver server;
    private boolean intercept;

    public void settings() {
        size( 640, 480 );
        logger = new OracleLogger( this );

        //fullScreen( 1 );
        settings = new Settings();

        millisLastInteraction = System.currentTimeMillis();
        if( startWebserver ){
            server = new Webserver( this );
        }
    }

    public void setup() {
        cli = new CLI( this );
        //markov = new MarkovManager();

        //markov.train( "text" + File.separator + "oraclev2" + File.separator + "v4_combined.txt", true );

        ArrayList< String > files = new ArrayList<>();
        files.add( "admin_medosch.txt" );
        files.add( "allan_watts.txt" );
        files.add( "benjamin_bratton.txt" );
        files.add( "cynthia_goodman.txt" );
        files.add( "domenic_quaranta.txt" );
        files.add( "drunvalo_melchizedek.txt" );
        files.add( "errki_hutamo.txt" );
        files.add( "espen_aarseth.txt" );
        files.add( "friedrich_kittler.txt" );
        files.add( "gene_youngblood.txt" );
        files.add( "harold_cohen.txt" );
        files.add( "jasia_reichardt.txt" );
        files.add( "john_thackara.txt" );
        files.add( "jussi_parikka.txt" );
        files.add( "katherine_hayles.txt" );
        files.add( "lev_manovich.txt" );
        files.add( "lisaa_gitelman.txt" );
        files.add( "lucien_sfez.txt" );
        files.add( "marilyn_raffaele.txt" );
        files.add( "michael_benedikt.txt" );
        files.add( "minna_tarkka.txt" );
        files.add( "naom_chomsky.txt" );
        files.add( "neil_whitehead-michael_wesch.txt" );
        files.add( "nick_bostrom.txt" );
        files.add( "peter_weibel.txt" );
        files.add( "pierre_levy.txt" );
        files.add( "roman_verostko.txt" );
        files.add( "sherry_turkle.txt" );
        files.add( "sissel_marie_tonn.txt" );
        files.add( "wark_mckenzie.txt" );
        files.add( "wjt_mitchell.txt" );

        markovs = new ArrayList<>();

        for ( String author : files ) {
            MarkovManager m = new MarkovManager();
            m.train( "text" + File.separator + "oraclev2" + File.separator + author, false );
            markovs.add( m );
        }

        //markov.load();
        noCursor();
    }

    public void draw() {
        background( 0 );
        cli.draw();

        if( System.currentTimeMillis() > millisLastInteraction + Settings.CLI_RESET_DELAY_MILLIS ){
            cli.reset();
        }
    }

    public void keyPressed() {
        millisLastInteraction = System.currentTimeMillis();

        if( cli.isActive() )
            return;

        if( key == CODED ){
            switch ( keyCode ) {
                case KeyEvent.VK_F1:
                    cli.reset();
                    break;
            }
        } else {
            switch ( key ) {
                case BACKSPACE:
                    cli.backspace();
                    break;
                case ENTER:
                    if( !cli.available() ){
                        return;
                    }

                    String inputWordsString = cli.getLastLine().getText( true ).trim();
                    while ( inputWordsString.startsWith( "." ) ||
                            inputWordsString.startsWith( "," ) ||
                            inputWordsString.startsWith( ";" ) ||
                            inputWordsString.startsWith( ":" ) ||
                            inputWordsString.startsWith( "-" ) ||
                            inputWordsString.startsWith( "_" ) ) {
                        // removing some leading special characters
                        inputWordsString = inputWordsString.substring( 1 );
                    }
                    inputWordsString = inputWordsString.trim();
                    System.out.println( inputWordsString );
                    if( intercept ){
                        server.sendInput( inputWordsString );
                        logger.logInput( inputWordsString );
                        cli.waitForAnswer();
                        return;
                    } else {
                        String result = null;
                        //try {

                        ArrayList< Integer > markovDepths = new ArrayList<>();

                        for ( MarkovManager m : markovs ) {
                            int depth = m.getMarkovDepthOrder( m.strip( inputWordsString ) );
                            markovDepths.add( depth );
                            System.out.println( "depth: " + depth );
                            System.out.println( m.getAnswer( inputWordsString ) );
                        }

                        Collections.sort( markovDepths );

                        result = markovs.get(markovDepths.get(markovDepths.size() - 1 ) ) .getAnswer( inputWordsString );
                        cli.finish( result );
                        /*
                        int count = 0;
                        int randomMarkovId = ( int ) random( markovs.size() );
                        result = markovs.get( randomMarkovId ).getAnswer( inputWordsString );
                        while ( result.equals( "nothing" ) && count < 50 ) {
                            System.out.println( "No answer from this markov. Trying new one. " + count );
                            randomMarkovId = ( int ) random( markovs.size() );
                            result = markovs.get( randomMarkovId ).getAnswer( inputWordsString );

                            count++;
                        }

                        if( count == 50 ){
                            result = markovs.get( 0 ).getRandomAnswer();
                        }


                        */


                        //result = markov.getAnswer( inputWordsString );

                        //if( result.contains( "lacuna" ) ){
                        //    cli.startEmojiEasterEgg();
                        //}
                        //} catch ( Exception e ) {
                        //    e.printStackTrace();
                        //    cli.finish( "oh", calculateDelayByResponseWordCount( inputWordsString.split( " " ).length ) );
                        //}


                        logger.log( inputWordsString, result );
                        System.out.println( result );
                    }
                    break;
                case TAB:
                case DELETE:
                    break;
                case ESC:
                    key = 0;
                    cli.reset();
                    break;
                default:
                    if( !cli.inputLimitReached() && !cli.isActive() ){
                        cli.type( key );
                    }
                    break;
            }
        }
    }

    public boolean intercept() {
        if( intercept )
            return true;
        intercept = true;
        return false;


    }

    public void responseFromTheWeb( String response ) {
        if( response.contains( "lacuna" ) ){
            cli.startEmojiEasterEgg();
        }
        intercept = false;
        logger.logResponse( response, false );
        System.out.println( response );
        cli.finishFromWeb( response );
    }

    public static void main( String[] args ) {
        PApplet.main( "oracle.Oracle" );
    }
}
