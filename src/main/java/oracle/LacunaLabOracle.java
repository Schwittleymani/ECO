package oracle;

import oracle.cli.CLI;
import oracle.web.Webserver;
import processing.core.PApplet;

import java.awt.event.KeyEvent;
import java.io.File;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.util.Enumeration;

/**
 * Created by mrzl on 31.03.2016.
 */
public class LacunaLabOracle extends PApplet {

    public static String EXPORT_FILENAME_PREFIX = "v2-order";
    public static int MAX_INPUT_WORDS = 2;
    public CLI cli;
    private MarkovManager markov;

    OracleLogger logger;

    long millisLastInteraction;
    long idleDelay = 5 * 60 * 1000; // 5 minutes

    boolean startWebserver = true;
    public Webserver server;


    public void settings() {
        size(640, 480);
        logger = new OracleLogger(this);

        //fullScreen( 1 );

        millisLastInteraction = System.currentTimeMillis();
        if (startWebserver) {
            server = new Webserver(this);
        }
    }

    public void setup() {
        cli = new CLI(this);
        markov = new MarkovManager();

        //markov.trainAndExport( "romantic_kamasutra.txt" );
        //markov.trainAndExport( "text" + File.separator + "oraclev2" + File.separator + "v3_combined.txt" );
        markov.load();
        noCursor();
        printIps();
    }

    public void draw() {
        background(0);
        cli.draw();

        if (System.currentTimeMillis() > millisLastInteraction + idleDelay) {
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
                    System.out.println(inputText);

                    String result = null;
                    //try {
                    result = markov.getAnswer(inputText);
                    int delayMillis = cli.finish(result);

                    if (startWebserver) {
                        server.sendTexts(inputText,result,delayMillis);
                        logger.logInput(inputText);
                    }

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


    public static void main(String[] args) {
        PApplet.main("oracle.LacunaLabOracle");
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
