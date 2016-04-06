package oracle.ostern;

import processing.core.PApplet;

/**
 * Created by mrzl on 07.04.2016.
 */
public class EmojiEasterEgg extends EasterEgg {

    public EmojiEasterEgg ( PApplet parent, float durationSeconds ) {
        super( parent, durationSeconds );
    }

    @Override
    public void drawBefore () {
        if ( isRunning( ) ) {
            // before text
            parent.noStroke( );
            parent.fill( 0, 0, 255 );
            parent.rect( parent.random( 0, parent.width ), parent.random( 0, parent.width ), parent.random( 0, parent.width ), parent.random( 0, parent.width ) );
        }
    }

    @Override
    public void drawAfter () {
        if ( isRunning( ) ) {
            // after text
            parent.noStroke( );
            parent.fill( 255, 0, 0 );
            parent.rect( parent.random( 0, parent.width ), parent.random( 0, parent.width ), parent.random( 0, parent.width ), parent.random( 0, parent.width ) );
        }
    }
}
