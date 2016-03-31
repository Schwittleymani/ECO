package oracle.cli;

import processing.core.PApplet;

/**
 * Created by mrzl on 01.04.2016.
 */
public class CLILine extends Line {

    public CLILine ( PApplet p ) {
        super( p );
    }

    public void backspace () {
        if ( size() > 2 ) {
            remove( size( ) - 1 );
        }
    }

}