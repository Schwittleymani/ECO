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

        if ( getText().length() > CLI.inputPreChars.length()  ) { // -1 is magic shit
            remove( size( ) - 1 );
        }
    }

    public boolean limitReached() {
        return size() >= CHAR_LIMIT;
    }

    public String getText(boolean cutPreChars) {
        if(cutPreChars)
            return String.join( "", this ).substring(CLI.inputPreChars.length());
        else
            return getText();
    }
}