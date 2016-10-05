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
    private float LINE_PREFIX_WIDTH;

    private ArrayList< Line > lines = new ArrayList<>();
    private ArrayList< Line > hiddenLines = new ArrayList<>(); // for edge case of endless writer...
    private Oracle oracle;

    private PFont font;

    private String result; // bot or intercept

    public enum CliState{
        USER_INPUT,
        ORACLE_WAITING,
        ORACLE_WRITING
    }

    public CliState state = CliState.USER_INPUT;
    public long startTimeInState;

    private Jesus jesus;
    private BlinkingRectangle blinker;
    private DelayedTyper delayedTyper;

    BoxValues margin,padding;
    protected int textSize;
    protected int lineHeight;
    int maximumNumberOfLines;

    public CLI( Oracle p ) {

        this.oracle = p;
        this.font = p.createFont( "data" + File.separator + "Glass_TTY_VT220.ttf", Settings.CLI_TEXT_SIZE );
        this.oracle.textFont( this.font );


        this.margin = new BoxValues(Settings.CLI_MARGIN_TOP,Settings.CLI_MARGIN_BOTTOM,
                Settings.CLI_MARGIN_LEFT,Settings.CLI_MARGIN_RIGHT, p.width, p.height);
        this.padding = new BoxValues(Settings.CLI_PADDING_TOP,Settings.CLI_PADDING_BOTTOM,
                Settings.CLI_PADDING_LEFT,Settings.CLI_PADDING_RIGHT, margin.width, margin.height);

        jesus = new Jesus( p );
        blinker = new BlinkingRectangle( p, this );
        delayedTyper = new DelayedTyper( this );

        lineHeight = Settings.CLI_LINE_HEIGTH;
        textSize = Settings.CLI_TEXT_SIZE;
        oracle.textSize(textSize);

        LINE_PREFIX_WIDTH = getTextWidth(LINE_PREFIX_CHARS);
        setupWidth();
        maximumNumberOfLines = (int)padding.height / Settings.CLI_LINE_HEIGTH;
        reset();
    }

    public void setupWidth() {
        // limit for the input line
        String widthTestString = "";
        do {
            widthTestString += "a";
        } while ( oracle.textWidth( widthTestString ) < padding.width);
        Line.CHAR_LIMIT = widthTestString.length();
       // System.out.println("debug: Line Limit: "+Line.CHAR_LIMIT);
    }


    public String getUserInput() {
        int lineIndex = lines.size() - 1;
        Line line = lines.get(lineIndex);
        String userInput = "";
        while(line.lineType == Line.LineType.USER_LINE) {
            userInput = line.getText() + userInput;
            lineIndex--;
            if(lineIndex >= 0) {
                line = lines.get(0);
            }
            else { // only for the edges case of an endless writer...
                line = hiddenLines.get(hiddenLines.size() + lineIndex);
            }
        }
        // USER_START line
        userInput = line.getText() + userInput;
        return userInput;
    }


    public void draw() {
        //System.out.println("CLI state: "+state);
        oracle.fill( 0, 255, 0 );
        oracle.pushMatrix();
        oracle.translate(margin.left,margin.top);

        // BORDER
        oracle.pushStyle();
        oracle.noFill();
        oracle.stroke( 0, 255, 0 );
        oracle.strokeWeight( 5 );
        oracle.rect( 0,0, margin.width,margin.height );
        oracle.popStyle();

        jesus.drawBeforeEaster();

        pushLinesUp();
        oracle.pushMatrix();
        oracle.translate(padding.left, padding.top);

        // test draw of the padding
        //oracle.pushStyle();
        //oracle.noFill();
        //oracle.stroke( 255, 0 , 0 );
        //oracle.strokeWeight( 1 );
        //oracle.rect( 0,0, padding.width, padding.height );
        //oracle.popStyle();

        for(int li = 0; li < lines.size(); li++){
            oracle.pushMatrix();
            oracle.translate(0,(li + 1) * lineHeight);
            Line line = lines.get(li);
            if(line.lineType != Line.LineType.USER_START)
                oracle.translate(LINE_PREFIX_WIDTH,0);
            line.draw();
            if(li == lines.size() - 1) {
                //System.out.println("CLI"+","+state);
                blinker.draw(state == CliState.ORACLE_WAITING);
            }
            oracle.popMatrix();
        }

        // types the text in delayed manner
        try {

            DelayedTyper.TyperState typerState= delayedTyper.update();
            if(typerState == DelayedTyper.TyperState.WRITING
                    && state != CliState.ORACLE_WRITING){
                setState(CliState.ORACLE_WRITING);
            }
            if(typerState == DelayedTyper.TyperState.DONE){
                setState(CliState.USER_INPUT);
            }

        } catch (NullPointerException e ){
            // hacky, but i dont understand the problem.
            e.printStackTrace();
            delayedTyper = new DelayedTyper( this );
            reset();
        }

        oracle.popMatrix();
        oracle.popMatrix();


        jesus.drawAfterEaster();
    }

    private void pushLinesUp() {
        if(lines.size() >= maximumNumberOfLines) {
            Line removed = lines.remove(0);
            if(state == CliState.USER_INPUT) {
                hiddenLines.add(removed);
            }
            return;
        }
    }

    public void backspace() {
        if( state == CliState.USER_INPUT ) {
            // should be true anyway, since cli.isActive() is in the oracle keypressed
            if(getLastLine().backspace()) {
               if(getLastLine().lineType == Line.LineType.USER_LINE) {
                   lines.remove(lines.size() - 1);
               }
            }
            //wordLineSplit();  didnt work really... yet
            OracleWebsocketServer.sendTypingBackspace();
        }
    }

    public long finish( String answer ) {
        state = CliState.ORACLE_WAITING;
        result = answer;
        delayedTyper.addText( answer );
        int words = answer.split( " " ).length;
        long delayMillis = calculateDelayByResponseWordCount( words );
        System.out.println("finnish-Calculated delay"+","+delayMillis);
        delayMillis -= (System.currentTimeMillis() - startTimeInState);
        System.out.println("finnish-down to"+","+delayMillis);

        delayedTyper.startTimout( delayMillis );
        return delayMillis;
    }

    // maybe just set state :)
    public void setState(CliState state) {
        this.state = state;
        if(state == CliState.USER_INPUT){
            newLine( Line.LineType.USER_START );
            state = CliState.USER_INPUT;
            delayedTyper.setIdle();
        } else if(state == CliState.ORACLE_WAITING){
            // not sure if this is ever called...
            startTimeInState = System.currentTimeMillis();
            newLine(Line.LineType.BOT_LINE);
        } else if(state == CliState.ORACLE_WRITING){
            oracle.server.finnish(result);
        }
    }

    public long calculateDelayByResponseWordCount( int length ) {
        int inputDelayMaxWords = 30;
        return ( int ) PApplet.map(
                PApplet.min(length,inputDelayMaxWords),
                1, inputDelayMaxWords,
                Settings.MIN_ANSWER_DELAY_COUNT, Settings.MAX_ANSWER_DELAY_COUNT );
    }

    public void type( char c ) {
        if( state == CliState.USER_INPUT ){
            // should be true anyway, since cli.isActive() is in the oracle keypressed
            delayedTyper.type( c );
            OracleWebsocketServer.sendTyping( c );
        }
    }

    public void newLine() {
        if(state == CliState.USER_INPUT)
            newLine(Line.LineType.USER_LINE);
        else
            newLine(Line.LineType.BOT_LINE);
    }


    public void newLine( Line.LineType type ) {
        //currentY += Settings.CLI_LINE_HEIGTH;
        Line newLine = new Line( this.oracle, type );
        lines.add( newLine );
        if( type == Line.LineType.USER_START){
            for(Character c : LINE_PREFIX_CHARS.toCharArray())
                delayedTyper.type(c);
        }
        if(type == Line.LineType.USER_START) {
            hiddenLines.clear();
        }
    }

    public Line getLastLine() {
        return lines.get( lines.size() - 1 );
    }

    public void reset() {
        lines.clear();
        newLine(Line.LineType.USER_START);
        // mayeb set typer state as well.
        state = CliState.USER_INPUT;
    }

    public boolean available() {
        return getUserInput().split( " " ).length >
                PREF_WORD_LEN && delayedTyper.isEmpty();
    }

    public void startEmojiEasterEgg() {
        jesus.start( Jesus.EASTEREGG_TYPE.EMOJI, 10 );
    }

    public int getTextWidth( String text ) {
        return ( int ) oracle.textWidth( text );
    }

    public int getTextSize() {
        return Settings.CLI_TEXT_SIZE;
    }

    public boolean isActive() {
        return !delayedTyper.isEmpty();
    }

    public boolean isReadyForInput() {
        return state == CliState.USER_INPUT;
    }

    public void suspendTyper( int millis ) {
        delayedTyper.addDelay( millis );
        System.out.println( "cli.suspendTyper: " + millis );
    }

    public boolean interceptTypeNow( String content ) {
        if( state == CliState.ORACLE_WAITING){
            delayedTyper.typeNow( content );
            result = content;
            return true;
        } else {
            return false;
        }
    }

    public void wordLineSplit() {
        if(lines.size() == 1)
            return;
        Line last = lines.get(lines.size() - 1);
        Line sndLast = lines.get(lines.size() - 2);
        String text = sndLast.getText() + last.getText() ;
        String[] words = text.split(" ");
        //System.out.println(Arrays.toString(words));
        String txtFor2ndLast = "";
        String txtForLastLine = "";
        int w = 0;
        for(; w < words.length; w++) {
            if(txtFor2ndLast.length() + words[w].length() + 1 < sndLast.limit()){
                txtFor2ndLast += words[w] + " ";
            } else {
                // might be the bizarre edge case that somebody wants to be funny
                // not typing any spaces...
                if(w == 0 || w == 2 && sndLast.lineType == Line.LineType.USER_START) {
                    int firstPartLength = oracle.min(words[w].length(),sndLast.limit());
                    String wordSplit1 = words[w].substring(0,firstPartLength);
                    String wordSplit2 = words[w].substring(firstPartLength);
                    txtFor2ndLast += wordSplit1;
                    txtForLastLine = wordSplit2;
                } else
                    break;
            }

        }
        for(; w < words.length; w++) {
            txtForLastLine += words[w] + (w < words.length - 1 ? " " : "");
        }
        sndLast.setText(txtFor2ndLast);
        last.setText(txtForLastLine);
    }

    public void typeNow() {
        delayedTyper.typeNow();
    }

    public long getDelayTimeout(){
        return delayedTyper.getDelayTimeout();
    }
}

