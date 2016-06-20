package oracle;

import oracle.cli.CLI;
import oracle.web.Webserver;
import processing.core.PApplet;

import java.awt.event.KeyEvent;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.util.ArrayList;
import java.util.Enumeration;

/**
 * Created by mrzl on 31.03.2016.
 *
 * This is the main starting point for the Electronic Chaos Oracle (ECO)
 */

public class Oracle extends PApplet{
    public CLI cli;
    public Webserver server;
    OracleLogger logger;
    Settings settings;

    long millisLastInteraction;

    boolean startWebserver = true;
    private ArrayList< MarkovManager > markovs;

    public static void main(String[] args) {
        PApplet.main("oracle.Oracle");
    }

    public void settings() {
        size(640, 480);
        logger = new OracleLogger(this);




        //fullScreen( 1 );
        settings = new Settings();

        millisLastInteraction = System.currentTimeMillis();

        if( startWebserver ){
            server = new Webserver( this );
            printIps();
        }
    }

    public void setup() {

        cli = new CLI( this );
        loadMarkovs();

        noCursor();
    }

    private void loadMarkovs() {
        String[] files = loadStrings("authors.txt");

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
        background(0);
        cli.draw();


        if( System.currentTimeMillis() > millisLastInteraction + Settings.CLI_RESET_DELAY_MILLIS ){
            cli.reset();
        }
    }

    public void keyPressed() {
        millisLastInteraction = System.currentTimeMillis();

        if (cli.isActive())
            return;

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

                    String inputText = cli.getLastLine().getText(true).trim();
                    while (inputText.startsWith(".") ||
                            inputText.startsWith(",") ||
                            inputText.startsWith(";") ||
                            inputText.startsWith(":") ||
                            inputText.startsWith("-") ||
                            inputText.startsWith("_")) {
                        // removing some leading special characters
                        inputText = inputText.substring(1);
                    }

                        inputText = inputText.trim();
                    System.out.println( inputText );

                        String result;

                        ArrayList< Integer > markovDepths = new ArrayList<>();
                        ArrayList< String > answers = new ArrayList<>();

                        for ( MarkovManager m : markovs ) {
                            int depth = m.getMarkovDepthOrder( m.strip( inputText ) );
                            String answer = m.getAnswer( inputText );
                            markovDepths.add( depth );
                            answers.add( answer );
                        }

                        result = answers.get( Settings.maxIndex( markovDepths ) );

                        int delayMillis =  cli.finish( result );
                        if (startWebserver) {
                            server.sendTexts(inputText, result, delayMillis);
                        }
                        //if( result.contains( "lacuna" ) ){
                        //    cli.startEmojiEasterEgg();
                        //}
                        //} catch ( Exception e ) {
                        //    e.printStackTrace();
                        //    cli.finish( "oh", calculateDelayByResponseWordCount( inputWordsString.split( " " ).length ) );
                        //}

                        logger.log( inputText, result );
                        System.out.println( result );

                    //if( result.contains( "lacuna" ) ){
                    //    cli.startEmojiEasterEgg();
                    //}
                    //} catch ( Exception e ) {
                    //    e.printStackTrace();
                    //    cli.finish( "oh", calculateDelayByInputLength( inputText.split( " " ).length ) );
                    //}

                    logger.log(inputText, result);
                    System.out.println(result);
                    break;
                case TAB:
                case DELETE:
                    break;
                case ESC:
                    key = 0;
                    cli.reset();
                    break;
                default:
                    if (!cli.inputLimitReached() && !cli.isActive()) {
                        cli.type(key);
                    }
                    break;
            }
        }
    }

    public void printIps() {
        System.out.println("*** Networks interfaces:");
        String ip;
        try {
            Enumeration<NetworkInterface> interfaces = NetworkInterface.getNetworkInterfaces();
            while (interfaces.hasMoreElements()) {
                NetworkInterface iface = interfaces.nextElement();
                // filters out 127.0.0.1 and inactive interfaces
                if (iface.isLoopback() || !iface.isUp())
                    continue;

                Enumeration<InetAddress> addresses = iface.getInetAddresses();
                while (addresses.hasMoreElements()) {
                    InetAddress addr = addresses.nextElement();
                    ip = addr.getHostAddress();
                    System.out.println(iface.getDisplayName() + " " + ip);
                }
            }
        } catch (SocketException e) {
            throw new RuntimeException(e);
        }
        System.out.println("******");
    }




    public void webSocketServerEvent(String msg) {
        server.webSocketServerEvent(msg);
    }


}
