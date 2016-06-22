package oracle;

import processing.core.PApplet;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.util.*;

/**
 * Created by mrzl on 16.06.2016.
 */
public class Settings{
    public static int MAX_INPUT_WORDS;
    public static int MIN_ANSWER_DELAY_COUNT, MAX_ANSWER_DELAY_COUNT;

    public static int CLI_PADDING_TOP, CLI_PADDING_LEFT;
    public static int CLI_LINE_HEIGTH, CLI_TEXT_SIZE, CLI_MAX_LINE_WIDTH;
    public static int CLI_RESET_DELAY_MILLIS, CLI_MAX_INPUT_CHARACTERS;

    public static int CLI_BORDER_X, CLI_BORDER_Y, CLI_BORDER_WIDTH, CLI_BORDER_HEIGHT;

    public static int CHARACTER_DELAY_TIMEOUT;

    public static ArrayList< String > RANDOM_ANSWERS = new ArrayList<>();

    public Settings() {
        Properties properties = new Properties();
        try {
            properties.load( new FileInputStream( "data" + File.separator + "config.properties" ) );
        } catch ( IOException e ) {
            e.printStackTrace();
        }

        MAX_INPUT_WORDS = Integer.parseInt( properties.getProperty( "MAX_INPUT_WORDS" ) );
        MIN_ANSWER_DELAY_COUNT = Integer.parseInt( properties.getProperty( "MIN_ANSWER_DELAY_COUNT" ) );
        MAX_ANSWER_DELAY_COUNT = Integer.parseInt( properties.getProperty( "MAX_ANSWER_DELAY_COUNT" ) );
        CLI_PADDING_TOP = Integer.parseInt( properties.getProperty( "CLI_PADDING_TOP" ) );
        CLI_PADDING_LEFT = Integer.parseInt( properties.getProperty( "CLI_PADDING_LEFT" ) );
        CLI_LINE_HEIGTH = Integer.parseInt( properties.getProperty( "CLI_LINE_HEIGTH" ) );
        CLI_TEXT_SIZE = Integer.parseInt( properties.getProperty( "CL_TEXT_SIZE" ) );
        CLI_MAX_LINE_WIDTH = Integer.parseInt( properties.getProperty( "CLI_MAX_LINE_WIDTH" ) );
        CLI_RESET_DELAY_MILLIS = Integer.parseInt( properties.getProperty( "CLI_RESET_DELAY_MILLIS" ) );
        CLI_MAX_INPUT_CHARACTERS = Integer.parseInt( properties.getProperty( "CLI_MAX_INPUT_CHARACTERS" ) );

        CHARACTER_DELAY_TIMEOUT = Integer.parseInt( properties.getProperty( "CHARACTER_DELAY_TIMEOUT" ) );

        CLI_BORDER_X = Integer.parseInt( properties.getProperty( "CLI_BORDER_X" ) );
        CLI_BORDER_Y = Integer.parseInt( properties.getProperty( "CLI_BORDER_Y" ) );
        CLI_BORDER_WIDTH = Integer.parseInt( properties.getProperty( "CLI_BORDER_WIDTH" ) );
        CLI_BORDER_HEIGHT = Integer.parseInt( properties.getProperty( "CLI_BORDER_HEIGHT" ) );

        try {
            String[] customAnswers = PApplet.loadStrings( new FileInputStream( "data" + File.separator + "answers.txt" ) );
            RANDOM_ANSWERS.addAll( Arrays.asList( customAnswers ) );
        } catch ( FileNotFoundException e ) {
            e.printStackTrace();
        }
    }

    public static void printIps() {
        System.out.println( "*** Networks interfaces:" );
        String ip;
        try {
            Enumeration< NetworkInterface > interfaces = NetworkInterface.getNetworkInterfaces();
            while ( interfaces.hasMoreElements() ) {
                NetworkInterface iface = interfaces.nextElement();
                // filters out 127.0.0.1 and inactive interfaces
                if( iface.isLoopback() || !iface.isUp() )
                    continue;

                Enumeration< InetAddress > addresses = iface.getInetAddresses();
                while ( addresses.hasMoreElements() ) {
                    InetAddress addr = addresses.nextElement();
                    ip = addr.getHostAddress();
                    System.out.println( iface.getDisplayName() + " " + ip );
                }
            }
        } catch ( SocketException e ) {
            throw new RuntimeException( e );
        }
        System.out.println( "******" );
    }

    public static int maxIndex( List< Integer > list ) {
        Integer i = 0, maxIndex = -1, max = null;
        for ( Integer x : list ) {
            if( ( x != null ) && ( ( max == null ) || ( x > max ) ) ){
                max = x;
                maxIndex = i;
            }
            i++;
        }
        return maxIndex;
    }
}
