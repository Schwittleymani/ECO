package oracle;

import processing.core.PApplet;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;
import java.util.logging.*;

/**
 * Created by raminsoleymani on 03/04/16.
 */
public class OracleLogger {

    static final String nl = System.getProperty("line.separator");
    SimpleDateFormat dateFormatter = new SimpleDateFormat("mm/dd/yyyy_HH:mm:ss");
    String completeLoggerFileName = "conversation.log";
    String sessionLoggerFileName = "session.log";

    Logger allknowingLogger = Logger.getLogger("complete");

    PApplet parent;

    public OracleLogger(PApplet parent) {

        this.parent = parent;
        try {
            FileHandler handler = new FileHandler(completeLoggerFileName,true);
            handler.setFormatter(new OracleFormatter());
            allknowingLogger.setUseParentHandlers(false);
            allknowingLogger.addHandler(handler);

            FileHandler sessionhandler = new FileHandler(sessionLoggerFileName,false);
            sessionhandler.setFormatter(new WebFormatter());
            allknowingLogger.addHandler(sessionhandler);

            removeLoggerGarbage();

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    private void removeLoggerGarbage() {
        File file = new File(parent.sketchPath());
        File[] files = file.listFiles();
        Arrays.stream(files)
                .filter(f -> {
                    String name = f.getName();
                    boolean readyToDie = (name.startsWith(completeLoggerFileName)
                        && name.length() > completeLoggerFileName.length()) // "conversation.log".length
                        || (name.startsWith(sessionLoggerFileName)
                            && name.length() > sessionLoggerFileName.length());
                    return readyToDie;
                })
                .forEach(f -> f.deleteOnExit());
    }

    public void logInput(String input) {
        allknowingLogger.severe("u:::" + input);
    }

    public void logResponse(String response,boolean oracle_or_server) {
        allknowingLogger.severe((oracle_or_server ?"o" : "web")+":::" + response);
    }

    public void log(String input, String result) {
        allknowingLogger.severe("u:::" + input);
        allknowingLogger.severe("o:::" + result);
    }

    class OracleFormatter extends Formatter {
            @Override
            public String format(LogRecord record) {
                String dateString  = dateFormatter.format(new Date());
                return dateString + ":::"+ record.getMessage() + nl;
            }
    }

    class WebFormatter extends Formatter {
        @Override
        public String format(LogRecord record) {
            return "|||"+ record.getMessage() + nl;
        }
    }
}
