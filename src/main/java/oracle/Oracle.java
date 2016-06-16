package oracle;

import oracle.cli.CLI;
import oracle.web.Webserver;
import processing.core.PApplet;

import java.awt.event.KeyEvent;
import java.io.File;

/**
 * Created by mrzl on 31.03.2016.
 */
public class Oracle extends PApplet{
    private CLI cli;
    private MarkovManager markov;

    OracleLogger logger;
    Settings settings;

    long millisLastInteraction;

    boolean startWebserver;
    Webserver server;
    private boolean intercept;

    public void settings() {
        size( 640, 480 );
        logger = new OracleLogger( this );

        fullScreen( 1 );
        settings = new Settings();

        millisLastInteraction = System.currentTimeMillis();
        if( startWebserver ){
            server = new Webserver( this );
        }
    }

    public void setup() {
        cli = new CLI( this );
        markov = new MarkovManager();

        //markov.trainAndExport( "romantic_kamasutra.txt" );
        markov.trainAndExport( "text" + File.separator + "oraclev2" + File.separator + "v4_combined.txt" );
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
                        result = markov.getAnswer( inputWordsString );

                        cli.finish( result );
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
