package oracle;

import oracle.cli.CLI;
import oracle.gif.GifDisplayer;
import oracle.lyrik.Lyrik;
import oracle.markov.Markov;
import oracle.web.Webserver;
import processing.core.PApplet;


import java.awt.event.KeyEvent;
import java.util.Optional;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by mrzl on 31.03.2016.
 * <p>
 * This is the main starting point for the Electronic Chaos Oracle (ECO)
 */

public class Oracle extends PApplet {
    public CLI cli;
    public Webserver server;
    OracleLogger logger;
    public Settings settings;

    long millisLastInteraction; // this timer should be part of a egg

    Lyrik lyrik;
    Markov markov;
    GifDisplayer gif;
    boolean useLyrik = true; // use lyrik in general
    boolean askMarkov = !useLyrik; // switched on when input arrived. set false after asking
    boolean startWebserver = true;
    boolean lyricRetry = true;

    long lyricRetryTimeoutStart;
    long lyricRetryTimout;
    //private String inputText;

    String lastInputText;
    String[] lastResults;

    public static void main(String[] args) {
        PApplet.main( "oracle.Oracle" );
    }

    public void settings() {
        size(640 * 2, 480, P3D);
        logger = new OracleLogger();

        settings = new Settings();

        if( Settings.FULLSCREEN ){
            fullScreen( SPAN );
        }

    }

    public void setup() {
        cli = new CLI(this);
        lyrik = new Lyrik();
        markov = new Markov(this);
        startWebserver(Settings.START_WEBSERVER);
        useLyrik = Settings.USE_LYRIK; // TODO connectivity check
        lyricRetry = useLyrik;
        lyricRetryTimout = Settings.LYRIC_RETRY_TIMEOUT;
        gif = new GifDisplayer(this);

        noCursor();
        imageMode(CENTER);
        millisLastInteraction = System.currentTimeMillis();
    }

    public void startWebserver(boolean startWS){
        startWebserver = startWS;
        if (startWS) {
            // TODO connectivity check
            server = new Webserver(this);
            Settings.printIps();
        }
    }

    public void draw() {
        background( 0 );

        gif.update();

        cli.draw();
        //println(frameCount);



        Optional<String[]> results = Optional.empty();

        if (useLyrik) {
            Lyrik.LyrikState lyrikState = lyrik.getState();
            if (lyrikState == Lyrik.LyrikState.DONE) {
                results = lyrik.getNewAnswer();

                lyrik.setState(Lyrik.LyrikState.IDLE);
                if (!results.isPresent()) {
                    askMarkov = true;
                    useLyrik = false; // switch lyrik off for now
                    lyricRetryTimeoutStart = System.currentTimeMillis();
                    System.out.println("Switching Lyrik off for now...");
                }
            }
        } else if(lyricRetry){
            if (System.currentTimeMillis() -  lyricRetryTimeoutStart > lyricRetryTimout){
                useLyrik = true;
                System.out.println("Retry Lyric next time");
            }
        }

        if (askMarkov) {
            println("local markov");
            results = markov.askLocalMarkov(lastInputText);
            askMarkov = false;
            if(!results.isPresent()){
                System.err.println( "even good old markov fails..." );
            }
        }
        if(results.isPresent()){
            lastResults = results.get();
            processAnswer();
        }


        if (System.currentTimeMillis() > millisLastInteraction + Settings.CLI_RESET_DELAY_MILLIS) {
            cli.reset();
            gif.reset();
        }

        if(millis() % 60 * 1000 == 0 ){
            String[] watchdogString = new String[] {""+System.currentTimeMillis()};
            saveStrings("watchdog.txt",watchdogString);
        }
    }


    public void keyPressed() {
        millisLastInteraction = System.currentTimeMillis();

        if (cli.isActive() || !cli.isReadyForInput()) {
            key = 0;
            return;
        }

        if (key == CODED) {
            switch (keyCode) {
                case KeyEvent.VK_F1:
                    cli.reset();
                    break;
            }
        } else {
            switch (key) {
                case BACKSPACE:
                    cli.backspace();
                    break;
                case ENTER:
                    if (!cli.available()) {
                        return;
                    }
                    processInput();
                    break;
                case TAB:
                case DELETE:
                    break;
                case ESC:
                    key = 0;
                    cli.reset();
                    break;
                default:
                    if (!cli.isActive()) {
                        cli.type(key);
                    }
                    break;
            }
        }
    }


    private void processInput() {
        String inputText = cli.getUserInput().trim();
        cli.setState(CLI.CliState.ORACLE_WAITING);
        lastInputText = removeSpecialCharacters(inputText );
        println( lastInputText );


        boolean useMarkovAnyways = random( 1 ) < Settings.USE_MARKOV_CHANCE;
        System.out.println( "Using Markov anyways = " + useMarkovAnyways + " chance " + Settings.USE_MARKOV_CHANCE);

        if (useLyrik && !useMarkovAnyways) {
            lyrik.askLyrikAsync(lastInputText);
        } else { // good old local markov chain
            // just set the flag here so we gonna have it in the next draw
            askMarkov = true;
        }

        if (startWebserver) {
            server.sendInput(lastInputText); // TODO why commented out. remove 3. parameter
        }

    }

    private void processAnswer() {

        String result = lastResults[0];
        String logResult = lastResults[1];

        logger.log(logger.USER, lastInputText);
        logger.log(logger.ORACLE, logResult);

        System.out.println("u:::" + lastInputText);
        System.out.println("o:::" + logResult );

        cli.finish(result);

        if (startWebserver) { // TODO that should come back...
            server.sendResult(result, cli.getDelayTimeout());
        }

        // only using first 4 words of answer as giphy keywords
        String[] words = result.split( " ");
        String keywords = "";
        int max = 4;
        for( int i = 0; i < words.length && i < max; i++ ) {
            keywords += words[i] + " ";
        }
        System.out.println( "SEARCHING GIPHY FOR " + keywords );

        gif.result(keywords);

        // jesus easter egg....

        //if( result.contains( "lacuna" ) ){
        //    cli.startEmojiEasterEgg();
        //}
        //} catch ( Exception e ) {
        //    e.printStackTrace();
        //    cli.finish( "oh", calculateDelayByResponseWordCount( inputWordsString.split( " " ).length ) );
        //}

    }

    /*

            cli.startThinkingState();
        String[] textSplit = text.split("\\s+");
        gif.getGiyGifsAsnyc(textSplit,1);

     */

    private String removeSpecialCharacters(String input) {
        Pattern p = Pattern.compile("\\W*");
        Matcher matcher = p.matcher(input);
        matcher.find();
        if (matcher.start() == 0) {
            return matcher.replaceFirst("");
        } else
            return input;
    }

    public void webSocketServerEvent(String msg) {
        server.webSocketServerEvent(msg);
    }

    public void intercept(String message) {
        if (cli.interceptTypeNow(message)) {
            logger.log(logger.INTERCEPTION, message);
        }
    }

}
