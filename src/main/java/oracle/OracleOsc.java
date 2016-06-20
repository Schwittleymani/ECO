package oracle;

import netP5.NetAddress;
import oscP5.OscMessage;
import oscP5.OscP5;

import java.util.ArrayList;

/**
 * Created by mrzl on 31.03.2016.
 */
public class OracleOsc{

    OscP5 osc;
    NetAddress addr;
    Settings settings;

    private ArrayList< MarkovManager > markovs;

    public void setup() {
        settings = new Settings();

        osc = new OscP5( this, 12000 );
        addr = new NetAddress( "127.0.0.1", 12001 );

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

        /*
        for ( String author : files ) {
            MarkovManager m = new MarkovManager();
            m.train( "text" + File.separator + "oraclev2" + File.separator + author, author, false );
            markovs.add( m );
        }
        */
        for ( String author : files ) {
            MarkovManager m = new MarkovManager();
            m.load( author );
            markovs.add( m );
        }
    }

    public String getContinued( String message ) throws Exception {
        String inputWordsString = message.trim();
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

        String result = null;

        ArrayList< Integer > markovDepths = new ArrayList<>();
        ArrayList< String > answers = new ArrayList<>();

        for ( MarkovManager m : markovs ) {
            int depth = m.getMarkovDepthOrder( m.strip( inputWordsString ) );
            String answer = m.getAnswer( inputWordsString );
            markovDepths.add( depth );
            answers.add( answer );
        }

        result = answers.get( Settings.maxIndex( markovDepths ) );
        return result;
    }

    public void oscEvent( OscMessage msg ) {
        if( msg.addrPattern().equals( "/get" ) ){
            String text = msg.get( 0 ).stringValue();
            String threadId = msg.get( 1 ).stringValue();
            String answer = null;
            System.out.println( "Request was: " + text );
            try {
                answer = getContinued( text );
                OscMessage oscReply = new OscMessage( "/answer" );
                oscReply.add( answer );
                oscReply.add( threadId );
                osc.send( oscReply, addr );
                System.out.println( "Sending reply: " + answer );

            } catch ( Exception e ) {
                System.out.println( "No answer.. skipping." );
            }
        }
    }

    public static void main( String[] args ) {
        OracleOsc oracle = new OracleOsc();
        oracle.setup();
    }
}
