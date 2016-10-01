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
        float textWidth = parent.textWidth( cli.getLastLine().getText() );
        parent.pushMatrix();
        parent.translate( textWidth, - cli.lineHeight);
        if( doRotate ) {
            // rotates the blinking square when its thinking
            float blockHeight = cli.getTextSize() + 10 * parent.noise( parent.frameCount * 0.01f );
            PVector centerOfBlinkingBox = new PVector(  parent.textWidth( cli.getLastLine().getText() ) + ( cursorBlockWidth / 2 ),  ( blockHeight / 2 ) );
            parent.translate( centerOfBlinkingBox.x, centerOfBlinkingBox.y );
            //parent.rotate( ( parent.frameCount ) );
            //parent.translate( -centerOfBlinkingBox.x, -centerOfBlinkingBox.y );
        }
        parent.pushStyle();
        parent.strokeWeight( 2 );

        int textColor = ( parent.millis() % ( 255 * 4 ) ) / 4;
        parent.stroke( 0, textColor, 0 );

        if( parent.random( 1 ) < 0.04f ){
            parent.noFill();
        }
        parent.rect(0, 0 ,
                cursorBlockWidth, cli.getTextSize() + 10 * parent.noise( parent.frameCount * 0.01f ) );

        parent.popStyle();
        parent.popMatrix();
    }
}
