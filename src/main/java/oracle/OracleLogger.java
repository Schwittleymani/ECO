package oracle;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.logging.FileHandler;
import java.util.logging.Formatter;
import java.util.logging.LogRecord;
import java.util.logging.Logger;

/**
 * Created by raminsoleymani on 03/04/16.
 */
public class OracleLogger {

    private final static Logger allNowingLogger = Logger.getLogger("input");

    private static final String dateFormatString = "mm/dd/yyyy HH:mm:ss";
    private SimpleDateFormat dateFormatter;

    public OracleLogger() {
        try {
            FileHandler handler = new FileHandler("conversation.log");
            handler.setFormatter(new Formatter() {
                @Override
                public String format(LogRecord record) {
                    String dateString  = dateFormatter.format(new Date(record.getMillis()));
                    return dateString + " "+ record.getMessage();
                }
            });
            allNowingLogger.addHandler(handler);

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

}
