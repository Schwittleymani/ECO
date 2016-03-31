package oracle.cli;

import processing.core.PApplet;

import java.util.ArrayList;

/**
 * Created by mrzl on 31.03.2016.
 */
public class CLI {
    private ArrayList< CLILine > lines = new ArrayList<>( );
    private PApplet parent;

    int textSize = 20;
    int currentY;
    int lineHeight = 30;
    int paddingLeft = 50;
    int maxLineWidth = 540;

    public CLI ( PApplet p ) {
        this.parent = p;

        reset( );
        type( '$' );
        type( ' ' );
    }

    public void draw () {
        parent.textSize( textSize );
        parent.fill( 0, 255, 0 );

        lines.forEach( CLILine::draw );

        drawBlinkingLine( );
    }

    private void drawBlinkingLine () {
        parent.pushStyle( );
        parent.strokeWeight( 2 );

        int textColor = ( parent.millis( ) % ( 255 * 4 ) ) / 4;
        parent.stroke( 0, textColor, 0 );
        float textWidth = parent.textWidth( getLastLine( ).getText( ) );
        parent.line( 50 + textWidth + 5, getLastLine( ).y - ( textSize ), 50 + textWidth + 5, getLastLine( ).y + ( textSize / 2 ) );

        parent.popStyle( );
    }

    public void type ( char key ) {
        CLILine act = getLastLine( );
        act.add( new String( String.valueOf( key ) ) );
        if ( parent.textWidth( act.getText( ) ) >= maxLineWidth ) {
            newLine( );
        }
    }

    public void type ( String string ) {
        string.chars( ).forEachOrdered( c -> type( ( char ) c ) );
    }

    public void backspace () {
        getLastLine( ).backspace( );
    }

    public void finish ( String answer ) {
        newLine( );
        type( answer );
        newLine( );
    }

    private void newLine () {
        currentY += lineHeight;
        CLILine newLine = new CLILine( this.parent );
        newLine.setPos( paddingLeft, currentY );
        lines.add( newLine );
    }

    public CLILine getLastLine () {
        return lines.get( lines.size( ) - 1 );
    }

    public void reset () {
        lines.clear( );

        currentY = 40;
        CLILine line = new CLILine( this.parent );
        line.setPos( paddingLeft, currentY );
        lines.add( line );
    }
}
