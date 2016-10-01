package oracle.cli;

import processing.core.PApplet;

import java.util.ArrayList;

/**
 * Created by mrzl on 01.04.2016.
 */
public class Line extends ArrayList< String > {

    private PApplet parent;

    public static int CHAR_LIMIT; // set by CLI

    enum LineType {
        USER_START, USER_LINE, BOT_LINE
    }

    public LineType lineType;


    public Line ( PApplet p, LineType type ) {
        this.parent = p;
        this.lineType = type;
    }

    /**
     *
     * @return end reached?
     */
    public boolean backspace () {
        int limit = lineType == LineType.USER_START ? CLI.LINE_PREFIX_CHARS.length( ) : 0;
        if ( getText( ).length( ) >  limit) {
            remove( size( ) - 1 );
        }
        return getText().length() == limit;
    }

    public boolean limitReached () {
        //System.out.println(size() + "," + CHAR_LIMIT);
        int add = lineType != LineType.USER_START ? 4 : 0; // 4 magic number. length of "[ ] "
        return size() + add >= CHAR_LIMIT;
    }


    public String getText ( boolean cutPreChars ) {
        if ( cutPreChars )
            return String.join( "", this ).substring( CLI.LINE_PREFIX_CHARS.length( ) );
        else
            return getText( );
    }

    public String getText () {
        return String.join( "", this );
    }

    public void draw () {
        parent.text( getText( ), 0,0);
    }

    protected  void setText(String txt) {
        clear();
        for(char c :  txt.toCharArray()) {
            this.add(""+c);
        }
    }

}