package oracle.cli;

import processing.core.PApplet;
import processing.core.PFont;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.IntStream;

/**
 * Created by mrzl on 31.03.2016.
 */
public class CLI {
    private ArrayList< CLILine > lines = new ArrayList<>( );
    private PApplet parent;
    private PFont font;

    int textSize = 20;
    private int currentY;
    int lineHeight = 30;
    int paddingTop = 40;
    int paddingLeft = 50;
    int maxLineWidth = 540;
    float cursorBlockWidth;
    public static String inputPreChars = "[ ]";

    public CLI ( PApplet p ) {
        this.parent = p;
        this.font = p.createFont( "Glass_TTY_VT220.ttf", textSize );
        p.textFont( this.font );

        reset( );

        parent.textSize( textSize );
        cursorBlockWidth = parent.textWidth("a");
    }

    public void draw () {
        parent.fill( 0, 255, 0 );
        pushLinesUp( );
        lines.forEach( CLILine::draw );

        drawBlinkingLine( );
    }

    private void pushLinesUp() {
        int moveUp = 1;
        for(;moveUp > 0; moveUp--){
            if(lines.get(lines.size() - (moveUp)).y > parent.height)
                break;
        }
        for (int i=0; i < moveUp; i++ ) {
            lines.remove(0);
        }
        resetYs( );
    }

    void resetYs() {
        currentY = paddingTop;
        for(Line line : lines) {
            line.y = currentY;
            currentY += lineHeight;
        }

    }

    private void drawBlinkingLine () {
        parent.pushStyle( );
        parent.strokeWeight( 2 );

        int textColor = ( parent.millis( ) % ( 255 * 4 ) ) / 4;
        parent.stroke( 0, textColor, 0 );
        float textWidth = parent.textWidth( getLastLine( ).getText( ) );
        if(parent.random(1) < 0.04f) {
            parent.noFill();
        }
        parent.rect( 50 + textWidth, getLastLine( ).y - ( textSize ),
                cursorBlockWidth, textSize + 10 * parent.noise( parent.frameCount * 0.01f ) );


        parent.popStyle( );
    }

    public void type ( char key ) {
        getLastLine( ).add( new String( String.valueOf( key ) ) );
    }

    public void type (String string) {
        String[] words = string.split( " " );
        CLILine act = getLastLine( );
        float actWidth  = parent.textWidth(act.getText());
        for(int i=0; i < words.length; i++) {
            if(actWidth + parent.textWidth(words[i]) > maxLineWidth) {
                newLine();
                act = getLastLine( );
                actWidth  = parent.textWidth(act.getText());
            } else {
                act.add(words[i]+" ");
                actWidth  = parent.textWidth(act.getText());
            }
        }
    }

    public void backspace () {
        getLastLine( ).backspace( );
    }

    public void finish ( String answer ) {
        newLine( );
        type( answer );
        newLine( true );
    }

    private void newLine () {
        newLine(false);
    }

    private void newLine (boolean inputChars) {
        currentY += lineHeight;
        CLILine newLine = new CLILine(this.parent);
        newLine.setPos(paddingLeft, currentY);
        lines.add( newLine );
        if (inputChars) {
            type(inputPreChars);
        }
    }

    public CLILine getLastLine () {
        return lines.get( lines.size( ) - 1 );
    }

    public void reset () {
        lines.clear( );

        currentY = paddingTop;
        CLILine line = new CLILine( this.parent );
        line.setPos( paddingLeft, currentY );
        lines.add( line );
        type(inputPreChars);
    }

    public boolean available() {
        //parent.println( getLastLine( ) );
        //parent.println( getLastLine( ).toString( ).split( " " ).length );
        return getLastLine().getText().split(" ").length > inputPreChars.split(" ").length;
    }
}
