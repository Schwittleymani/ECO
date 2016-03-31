package oracle;

import processing.core.PApplet;

import java.util.ArrayList;

/**
 * Created by mrzl on 31.03.2016.
 */
public class CLI {

    private ArrayList< String > characters;
    private PApplet parent;

    public CLI( PApplet p ) {
        this.characters = new ArrayList<>( );
        this.parent = p;
    }

    void draw() {
        parent.fill( 0, 255, 0 );
        parent.textSize( 20 );
        parent.text( getText( ), 50, 40 );
        float textWidth = parent.textWidth( getText() );

        parent.pushStyle();
        parent.strokeWeight( 2 );
        int textColor = ( parent.millis() % (255*4)) / 4;
        parent.stroke( 0, textColor, 0 );
        parent.line(50 + textWidth + 5, 20, 50 + textWidth + 5, 45);
        parent.popStyle();
    }

    public void type( char key ) {
        characters.add( new String( String.valueOf( key ) ) );
    }

    public void clear() {
        characters.clear( );
    }

    public String getText() {
        return String.join( "", characters );
    }

    public void backspace() {
        if( characters.size() == 0 ) {
            return;
        }
        characters.remove( characters.size( ) - 1 );
    }
}
