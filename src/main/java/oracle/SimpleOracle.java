package oracle;

import netP5.NetAddress;
import oscP5.OscMessage;
import oscP5.OscP5;

/**
 * Created by mrzl on 31.03.2016.
 */
public class SimpleOracle{

    public static String EXPORT_FILENAME_PREFIX = "romantic-order";
    public static int MAX_INPUT_WORDS = 4;
    private MarkovManager markov;

    OscP5 osc;
    NetAddress addr;

    public void setup() {
        markov = new MarkovManager();

        //markov.save( "romantic.txt" );
        markov.load();

        osc = new OscP5( this, 12000 );
        addr = new NetAddress( "127.0.0.1", 12001 );
    }

    public String getContinued( String message ) throws Exception {
        String inputWordsString = message.toLowerCase().trim();
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
        String result = markov.getAnswer( inputWordsString );
        return result;
    }

    public void oscEvent( OscMessage msg ) {
        if( msg.addrPattern().equals( "/get" ) ){
            String text = msg.get( 0 ).stringValue();
            String answer = null;
            System.out.println( "Request was: " + text );
            try {
                answer = getContinued( text );
                OscMessage oscReply = new OscMessage( "/answer" );
                oscReply.add( answer );
                osc.send( oscReply, addr );
                System.out.println( "Sending reply: " + answer );

            } catch ( Exception e ) {
                System.out.println( "No answer.. skipping." );
            }
        }
    }

    public static void main( String[] args ) {
        SimpleOracle oracle = new SimpleOracle();
        oracle.setup();
    }
}
