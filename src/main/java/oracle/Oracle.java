package oracle;

import gifAnimation.Gif;
import http.requests.PostRequest;
import oracle.cli.CLI;
import oracle.gif.GifDisplayer;
import oracle.web.Webserver;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import processing.core.PApplet;


import java.awt.event.KeyEvent;
import java.io.File;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by mrzl on 31.03.2016.
 * <p>
 * This is the main starting point for the Electronic Chaos Oracle (ECO)
 */

public class Oracle extends PApplet{
    public CLI cli;
    Webserver server;
    OracleLogger logger;
    public Settings settings;

    long millisLastInteraction;

    boolean startWebserver = true;
    private ArrayList< MarkovManager > markovs;

    GifDisplayer gifDisplayer;
    List<Gif> testGifs = new ArrayList<Gif>();

    public static void main( String[] args ) {
        PApplet.main( "oracle.Oracle" );
    }

    public void settings() {
        size( 640, 480, P2D );
        logger = new OracleLogger();

        //fullScreen( P2D, SPAN );

        settings = new Settings();

        millisLastInteraction = System.currentTimeMillis();

        if( startWebserver ){
            server = new Webserver( this );
            Settings.printIps();
        }
    }


    public void setup() {
        gifDisplayer = new GifDisplayer(this);
        gifDisplayer.getGiyGifsAsnyc(new String[]{"dog","king"},4);

        imageMode(CENTER);

        cli = new CLI( this );
       // loadMarkovs();

        noCursor();
    }

    private void loadMarkovs() {
        String[] files = loadStrings( "authors.txt" );

        markovs = new ArrayList<>();

                /*
        for ( String author : files ) {
            MarkovManager m = new MarkovManager();
            m.train( "text" + File.separator + "oraclev2" + File.separator + author, author, true );
            markovs.add( m );
        }
            */

        for ( String author : files ) {
            MarkovManager m = new MarkovManager();
            m.load( author );
            markovs.add( m );
        }

    }

    public void draw() {
        background( 0 );
        cli.draw();

        if(gifDisplayer.getAsyncGifysAvailable()) {
            testGifs = gifDisplayer.getAsyncGifys();
            testGifs.stream().forEach(Gif::play);
        }
        if(testGifs.size() > 0)
            image( testGifs.get((frameCount/5) % testGifs.size()), mouseX, mouseY );


        if( System.currentTimeMillis() > millisLastInteraction + Settings.CLI_RESET_DELAY_MILLIS ){
            cli.reset();
        }
    }

    public void keyPressed() {
        millisLastInteraction = System.currentTimeMillis();

        if( cli.isActive() ){
            key = 0;
            return;
        }

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

                    String inputText = cli.getLastLine().getText( true ).trim();
                    while ( inputText.startsWith( "." ) ||
                            inputText.startsWith( "," ) ||
                            inputText.startsWith( ";" ) ||
                            inputText.startsWith( ":" ) ||
                            inputText.startsWith( "-" ) ||
                            inputText.startsWith( "_" ) ) {
                        // removing some leading special characters
                        inputText = inputText.substring( 1 );
                    }

                    inputText = inputText.trim();

                    String result = remoteRequest( inputText );

                    int delayMillis = cli.finish( result );
                    if( startWebserver ){
                        server.sendTexts( inputText, result, delayMillis );
                    }

                    System.out.println( "u:::" + inputText );

                    /*
                    String result;

                    ArrayList< Integer > markovDepths = new ArrayList<>();
                    ArrayList< String > answers = new ArrayList<>();
                    ArrayList< String > authors = new ArrayList<>();

                    for ( MarkovManager m : markovs ) {
                        int depth = m.getMarkovDepthOrder( m.strip( inputText ) );
                        String answer = m.getAnswer( inputText );
                        markovDepths.add( depth );
                        answers.add( answer );
                        authors.add( m.getAuthorName() );
                    }

                    // if the depth of the selected answer is 0, that means
                    // there was no proper answer of any author
                    int index = Settings.maxIndex( markovDepths );
                    result = answers.get( index );
                    String authorName = authors.get( index );
                    if( markovDepths.get( index ) == 0 ){
                        authorName = "pre_defined_answer";
                    }

                    // debugging
                    result = markovs.get( 0 ).getAnswer( inputText );

                    int delayMillis = cli.finish( result );
                    if( startWebserver ){
                        server.sendTexts( inputText, result, delayMillis );
                    }
                    //if( result.contains( "lacuna" ) ){
                    //    cli.startEmojiEasterEgg();
                    //}
                    //} catch ( Exception e ) {
                    //    e.printStackTrace();
                    //    cli.finish( "oh", calculateDelayByResponseWordCount( inputWordsString.split( " " ).length ) );
                    //}

                    logger.log( logger.USER, inputText );
                    logger.log( logger.ORACLE, "(" + authorName + ") " + result );

                    System.out.println( "o:::" + result );
                    System.out.println( "a:::" + authorName );

                    */
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

    private String remoteRequest( String text ) {
        text = text.replaceAll( "\\s+", "%20" );
        PostRequest post = new PostRequest( Settings.LYRIK_URL + text );

        post.addData( "inputS", "hello ECO" );
        try {
            long millis = millis();
            post.send();

            if( post != null ){
                println( "Reponse Content: " + post.getContent() );
                println( "Reponse Content-Length Header: " + post.getHeader( "Content-Length" ) );
                long millisDiff = millis() - millis;
                println( "That took " + millisDiff + "ms" );

                JSONParser json = new JSONParser();
                Object obj = json.parse( post.getContent() );
                JSONObject mainJson = (JSONObject ) (obj);
                String result = ( String ) mainJson.get("combined");

                System.out.println( "Received result: " + result );

                return result;
            }
        } catch ( Exception exc ) {
            exc.printStackTrace();
        }

        return "nothing";
    }

    public void webSocketServerEvent( String msg ) {
        server.webSocketServerEvent( msg );
    }

    public void intercept( String message ) {
        if( cli.interceptTypeNow( message ) ){
            logger.log( logger.INTERCEPTION, message );
        }
    }

}
