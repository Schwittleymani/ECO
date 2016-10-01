package oracle.cli;


import oracle.Oracle;
import oracle.Settings;
import oracle.ostern.Jesus;
import oracle.web.OracleWebsocketServer;
import processing.core.PApplet;
import processing.core.PFont;

import java.io.File;
import java.util.ArrayList;

/**
 * Created by mrzl on 31.03.2016.
 */
public class CLI{
    public static final String LINE_PREFIX_CHARS = "[ ] ";
    private static final int PREF_WORD_LEN = LINE_PREFIX_CHARS.split( " " ).length;

    private ArrayList< Line > lines = new ArrayList<>();
    private Oracle parent;

    private PFont font;


    public enum CliState{
        USER_INPUT,
        ORACLE_THINKING,
        ORACLE_TYPING
    }

    public CliState state = CliState.USER_INPUT;

    private Jesus jesus;
    private BlinkingRectangle blinker;
    private DelayedTyper delayedTyper;

    private int currentY;

    BoxValues margin,padding;


    public CLI( Oracle p ) {

        this.parent = p;
        this.font = p.createFont( "data" + File.separator + "Glass_TTY_VT220.ttf", Settings.CLI_TEXT_SIZE );
        this.parent.textFont( this.font );

        this.margin = new BoxValues(Settings.CLI_MARGIN_TOP,Settings.CLI_MARGIN_BOTTOM,
                Settings.CLI_MARGIN_LEFT,Settings.CLI_MARGIN_RIGHT, p.width, p.height);
        this.padding = new BoxValues(Settings.CLI_PADDING_TOP,Settings.CLI_PADDING_BOTTOM,
                Settings.CLI_PADDING_LEFT,Settings.CLI_PADDING_RIGHT, margin.width, margin.height);

        jesus = new Jesus( p );
        blinker = new BlinkingRectangle( p, this );
        delayedTyper = new DelayedTyper( this );

        reset();

        parent.textSize( Settings.CLI_TEXT_SIZE );
        setupWidth();
    }

    public void setupWidth() {
        // limit for the input line
        String widthTestString = "";
        do {
            widthTestString += "a";
        } while ( parent.textWidth( widthTestString ) < Settings.CLI_MAX_LINE_WIDTH );
        Line.CHAR_LIMIT = widthTestString.length();
    }

    public void draw() {
        parent.fill( 0, 255, 0 );
        parent.pushMatrix();
        parent.translate(margin.left,margin.top);

        // BORDER
        parent.pushStyle();
        parent.noFill();
        parent.stroke( 0, 255, 0 );
        parent.strokeWeight( 5 );
        parent.rect( 0,0, margin.width,margin.height );
        parent.popStyle();

        jesus.drawBeforeEaster();

        pushLinesUp();
        parent.pushMatrix();
        parent.translate(padding.left, padding.top);

        parent.pushStyle();
        parent.noFill();
        parent.stroke( 255, 0 , 0 );
        parent.strokeWeight( 1 );
        parent.rect( 0,0, padding.width, padding.height );
        parent.popStyle();

        lines.forEach( Line::draw );

        // draws blinking square, rotating or not
        blinker.draw( delayedTyper.isWaiting() );

        // types the text in delayed manner
        if( delayedTyper.update() ){
            newLine( true );
        }

        state = delayedTyper.getState();
        //System.out.println(state.name());

        parent.popMatrix();
        parent.popMatrix();
        jesus.drawAfterEaster();
    }

    private void pushLinesUp() {
        // sidenote: the nice effect that the lines animate up is
        int moveUp = 1;
        for (; moveUp > 0; moveUp-- ) {
            if( lines.get( lines.size() - ( moveUp ) ).y > parent.height )
                break;
        }
        for ( int i = 0; i < moveUp; i++ ) {
            lines.remove( 0 );
        }
        resetYs();
    }

    void resetYs() {
        currentY = 0;//Settings.CLI_PADDING_TOP;
        for ( Line line : lines ) {
            line.y = currentY;
            currentY += Settings.CLI_LINE_HEIGTH;
        }
    }

    public void backspace() {
        if( state == CliState.USER_INPUT ) {
            // should be true anyway, since cli.isActive() is in the oracle keypressed
            getLastLine().backspace();
            OracleWebsocketServer.sendTypingBackspace();
        }
    }

    public int finish( String answer ) {
        newLine();
        delayedTyper.addText( answer );
        int words = answer.split( " " ).length;
        int delayMillis = calculateDelayByResponseWordCount( words );
        delayedTyper.startTimout( delayMillis );
        state = CliState.ORACLE_THINKING;
        return delayMillis;
    }


    public int calculateDelayByResponseWordCount( int length ) {
        int inputDelayMaxWords = 30;
        return ( int ) PApplet.map( PApplet.min( length, inputDelayMaxWords ), 1, inputDelayMaxWords, Settings.MIN_ANSWER_DELAY_COUNT, Settings.MAX_ANSWER_DELAY_COUNT );
    }

    public void type( char c ) {
        if( state == CliState.USER_INPUT ){
            // should be true anyway, since cli.isActive() is in the oracle keypressed
            delayedTyper.type( c );
            OracleWebsocketServer.sendTyping( c );
        }
    }


    public void newLine() {
        newLine( false );
    }

    private void newLine( boolean addLinePrefix ) {
        currentY += Settings.CLI_LINE_HEIGTH;
        Line newLine = new Line( this.parent );
        newLine.setPos( 0, currentY );
        lines.add( newLine );
        if( addLinePrefix ){
            delayedTyper.type( LINE_PREFIX_CHARS );
        } else {
            // a little bit of more offset on the left
            float extraPadding = parent.textWidth(LINE_PREFIX_CHARS);
            newLine.setPos( Settings.CLI_PADDING_LEFT + (int) extraPadding, currentY );
        }
    }

    public Line getLastLine() {
        return lines.get( lines.size() - 1 );
    }

    public void reset() {
        lines.clear();

        currentY = Settings.CLI_PADDING_TOP;
        Line line = new Line( this.parent );
        line.setPos( Settings.CLI_PADDING_LEFT, currentY );
        lines.add( line );
        delayedTyper.type( LINE_PREFIX_CHARS );
    }

    public boolean available() {
        return getLastLine().getText().split( " " ).length >
                PREF_WORD_LEN && delayedTyper.isEmpty();
    }

    public void startEmojiEasterEgg() {
        jesus.start( Jesus.EASTEREGG_TYPE.EMOJI, 10 );
    }

    public int getMaxLineWidth() {
        return Settings.CLI_MAX_LINE_WIDTH;
    }

    public int getTextWidth( String text ) {
        return ( int ) parent.textWidth( text );
    }

    public int getTextSize() {
        return Settings.CLI_TEXT_SIZE;
    }

    public boolean isActive() {
        return !delayedTyper.isEmpty();
    }

    public boolean inputLimitReached() {
        return getLastLine().getText( false ).length() >= Settings.CLI_MAX_INPUT_CHARACTERS;
    }

    public void suspendTyper( int millis ) {
        delayedTyper.addDelay( millis );
        System.out.println( "cli.suspendTyper: " + millis );
    }

    public boolean interceptTypeNow( String content ) {
        if( state == CliState.ORACLE_THINKING ){
            delayedTyper.typeNow( content );
            return true;
        } else {
            return false;
        }
    }

    public void typeNow() {
        delayedTyper.typeNow();
    }
}

