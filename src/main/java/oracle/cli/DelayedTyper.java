package oracle.cli;

import oracle.web.OracleWebsocketServer;

/**
 * Created by mrzl on 09.04.2016.
 */
public class DelayedTyper{
    private CLI cli;

    private String textToType;
    private long delayTimeout;
    private long timeoutStart;
    private boolean isWaiting;


    public DelayedTyper( CLI cli ) {
        textToType = "";
        this.cli = cli;
        //delayTimeout = System.currentTimeMillis();
        //initDelayStartMillis = System.currentTimeMillis();
    }

    public void addText( String text ) {
        textToType += text;
        isWaiting = true;
    }

    public void startTimout(long millis) {
        timeoutStart = System.currentTimeMillis();
        delayTimeout = millis;
    }

    public void addDelay( long millis ) {
        delayTimeout += millis;
        System.out.println("delayedtyper.adddelay "+ millis);
    }

    public boolean isWaiting() {
        if(isWaiting) {
            isWaiting = System.currentTimeMillis() - timeoutStart < delayTimeout;
            if(!isWaiting) {
                OracleWebsocketServer.oracleThinksTimeout();
            }
            return isWaiting;
        } else
            return false;
    }

    /*public boolean isInitDelay() {
        return System.currentTimeMillis() - initDelayStartMillis < initDelayMillis;
    }*/

    /**
     * @return whether a new line should be set
     */
    public boolean update() {
        if( !isEmpty() ){
            if( !isWaiting() ){
                type( textToType.charAt( 0 ) );
                textToType = textToType.substring( 1, textToType.length() );
                delayTimeout = System.currentTimeMillis();
            }
            if( isEmpty() ){
                // if last character was typed
                return true;
            }
        }
        return false;
    }

    public void type( char key ) {
        if( key == ' ' && cli.getLastLine().limitReachedOffset() ){
            cli.newLine();
        } else {
            cli.getLastLine().add( new String( String.valueOf( key ) ) );
        }
    }

    public void type( String string ) {
        String[] words = string.split( " " );
        Line act = cli.getLastLine();
        float actWidth = cli.getTextWidth( act.getText( false ) );
        for ( int i = 0; i < words.length; i++ ) {
            if( actWidth + cli.getTextWidth( words[ i ] ) > cli.getMaxLineWidth() ){
                cli.newLine();
                act = cli.getLastLine();
                actWidth = cli.getTextWidth( act.getText() );
            } else {
                act.add( words[ i ] + " " );
                actWidth = cli.getTextWidth( act.getText() );
            }
        }
    }

    public boolean isEmpty() {
        return textToType.isEmpty();
    }

    public String getText() {
        return textToType;
    }

    public void typeNow(String content) {
        textToType = content;
        typeNow();
    }

    public void typeNow() {
        System.out.println("delayedTimer.now");
        delayTimeout = 0;
    }

    public CLI.CliState getState() {
        if(isWaiting)
            return CLI.CliState.ORACLE_THINKING;
        else {
            if(isEmpty())
                return CLI.CliState.USER_INPUT;
            else
                return CLI.CliState.ORACLE_TYPING;
        }
    }
}
