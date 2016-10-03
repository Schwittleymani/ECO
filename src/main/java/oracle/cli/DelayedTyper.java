package oracle.cli;

import oracle.Settings;
import oracle.web.OracleWebsocketServer;

/**
 * Created by mrzl on 09.04.2016.
 */
public class DelayedTyper{
    private CLI cli;

    private String textToType;


    private long delayTimeout;
    private long timeoutStart;
    private long characterDelayStart;
    private long characterDelayTimeout = Settings.CHARACTER_DELAY_TIMEOUT;



    enum TyperState{
        IDLE,WAITING,WRITING,DONE
    }

    private TyperState state = TyperState.IDLE;

    public DelayedTyper( CLI cli ) {
        textToType = "";
        this.cli = cli;
    }

    public void addText( String text ) {
        textToType += text;
    }

    public void startTimout(long millis) {
        timeoutStart = System.currentTimeMillis();
        delayTimeout = millis;
        state = TyperState.WAITING;
    }

    public void addDelay( long millis ) {
        delayTimeout += millis;
        System.out.println("delayedtyper.adddelay "+ millis);
        state = TyperState.WAITING;
    }


    /*public boolean isInitDelay() {
        return System.currentTimeMillis() - initDelayStartMillis < initDelayMillis;
    }*/

    /**
     * @return whether a new line should be set
     */
    public TyperState update() {
        //System.out.println("Typer: "+","+state);
        long now = System.currentTimeMillis();;
        switch (state){
            case IDLE:
                break;
            case WAITING:
                if(now - timeoutStart > delayTimeout) {
                    state = TyperState.WRITING;
                }
                break;
            case WRITING:
                if(now - characterDelayStart > characterDelayTimeout) {
                    type(textToType.charAt(0));
                    textToType = textToType.substring(1, textToType.length());
                    characterDelayStart = now;
                    if(isEmpty()) {
                        state = TyperState.DONE;
                    }
                }
                break;
        }
        return state;
    }

    // user input
    public void type( char key ) {
        cli.getLastLine().add(""+key);
        if(cli.getLastLine().limitReached() ) {
            cli.newLine();
            cli.wordLineSplit();
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

    public void setIdle() {
        if(state == TyperState.DONE){
            state = TyperState.IDLE;
        } else {
            System.err.println("strage that you call DelayedTyper.setIdle again...");
        }
    }
}
