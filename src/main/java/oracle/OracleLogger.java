package oracle;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.logging.*;

/**
 * Created by raminsoleymani on 03/04/16.
 */
public class OracleLogger {

    static final String nl = System.getProperty("line.separator");
    SimpleDateFormat dateFormatter = new SimpleDateFormat("mm/dd/yyyy_HH:mm:ss");

    Logger allknowingLogger = Logger.getLogger("complete");

    public OracleLogger() {

        try {
            FileHandler handler = new FileHandler("conversation.log",true);
            handler.setFormatter( new OracleFormatter());
            allknowingLogger.setUseParentHandlers(false);
            allknowingLogger.addHandler(handler);

            FileHandler sessionhandler = new FileHandler("session.log",false);
            sessionhandler.setFormatter(new WebFormatter());
            allknowingLogger.addHandler(sessionhandler);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void log(String input, String result) {
        allknowingLogger.severe("u:::" + input);
        allknowingLogger.severe("o:::" + result);
    }

    public void close() {
        for( Handler h : allknowingLogger.getHandlers() ) {
            h.flush();
            h.close();
        }
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