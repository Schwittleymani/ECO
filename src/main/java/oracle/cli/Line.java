package oracle.cli;

import processing.core.PApplet;

import java.util.ArrayList;

/**
 * Created by mrzl on 01.04.2016.
 */
public class Line extends ArrayList< String > {

    private PApplet parent;
    public int x, y;
    public static int CHAR_LIMIT; // set by CLI

    public Line ( PApplet p ) {
        this.parent = p;
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

    public String getText () {
        return String.join( "", this );
    }

    public void draw() {
        parent.text( getText( ), x, y );
    }

    public void setPos( int x, int y ) {
        this.x = x;
        this.y = y;
    }

    public String toString() {
        return x + " " + y;
    }
}