package oracle.cli;

import processing.core.PApplet;
import processing.core.PVector;

/**
 * Created by mrzl on 09.04.2016.
 */
public class BlinkingRectangle{
    private PApplet parent;
    private CLI cli;

    private float cursorBlockWidth;

    public BlinkingRectangle( PApplet parent, CLI cli ) {
        this.parent = parent;
        this.cli = cli;

        cursorBlockWidth = parent.textWidth( "a" );
    }

    public void draw( boolean doRotate) {
        parent.pushMatrix();
        if( doRotate ) {
            // rotates the blinking square when its thinking
            float blockHeight = cli.getTextSize() + 10 * parent.noise( parent.frameCount * 0.01f );
            PVector centerOfBlinkingBox = new PVector( cli.getLastLine().x + parent.textWidth( cli.getLastLine().getText() ) + ( cursorBlockWidth / 2 ), cli.getLastLine().y - ( cli.getTextSize() ) + ( blockHeight / 2 ) );
            parent.translate( centerOfBlinkingBox.x, centerOfBlinkingBox.y );
            parent.rotate( ( parent.frameCount ) );
            parent.translate( -centerOfBlinkingBox.x, -centerOfBlinkingBox.y );
        }
        parent.pushStyle();
        parent.strokeWeight( 2 );

        int textColor = ( parent.millis() % ( 255 * 4 ) ) / 4;
        parent.stroke( 0, textColor, 0 );
        float textWidth = parent.textWidth( cli.getLastLine().getText() );
        if( parent.random( 1 ) < 0.04f ){
            parent.noFill();
        }
        parent.rect( cli.getLastLine().x + textWidth, cli.getLastLine().y - ( cli.getTextSize() ),
                cursorBlockWidth, cli.getTextSize() + 10 * parent.noise( parent.frameCount * 0.01f ) );


        parent.popStyle();
        parent.popMatrix();
    }
}
