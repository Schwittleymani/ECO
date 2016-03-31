package oracle.cli;

import processing.core.PApplet;

import java.util.ArrayList;

/**
 * Created by mrzl on 01.04.2016.
 */
public class Line extends ArrayList< String > {

    private PApplet parent;
    public int x, y;

    public Line( PApplet p ){
        super();
        this.parent = p;
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