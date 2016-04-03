package oracle.cli;

import processing.core.PApplet;

/**
 * Created by mrzl on 01.04.2016.
 */
public class CLILine extends Line {

    public static int CHAR_LIMIT; // set by CLI
    public CLILine ( PApplet p ) {
        super( p );
    }

    public void backspace () {
        if ( size() >= CLI.inputPreChars.length() ) {
            remove( size( ) - 1 );
        }
    }

    public boolean limitReached() {
        return size() >= CHAR_LIMIT;
    }

}