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


    private static final String dateFormatString = "MM/dd/yyyy_HH:mm:ss";
    private SimpleDateFormat dateFormatter;

    static final String nl = System.getProperty("line.separator");

    public OracleLogger() {
        try {
            Logger allNowingLogger = Logger.getLogger("input");
            FileHandler handler = new FileHandler("conversation.log",true);
            dateFormatter = new SimpleDateFormat(dateFormatString);
            handler.setFormatter(new Formatter() {
                @Override
                public String format(LogRecord record) {
                    String dateString  = dateFormatter.format(new Date());
                    return dateString + ":::"+ record.getMessage() + nl;
                }
            });

            allNowingLogger.setUseParentHandlers(false);
            allNowingLogger.addHandler(handler);

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

}
