package oracle.web;

import oracle.Oracle;
import processing.core.PApplet;
import processing.data.JSONObject;
import websockets.*;

/**
 * Created by raminsoleymani on 16/06/16.
 */

public class OracleWebsocketServer {


    final int USER_INPUT = 0;
    final int ORACLE_THINKS = 1;

    int state = USER_INPUT;

    static private OracleWebsocketServer me;
    WebsocketServer ws;
    String last_input = "";
    String last_result = "";

    Oracle oracle;

    public OracleWebsocketServer(Oracle oracle) {
        ws = new WebsocketServer(oracle, 8001, "/oracle");
        me = this;
        this.oracle = oracle;
    }

    public void sendTexts(String input,String result,long timeout) {
        JSONObject msg_obj = new JSONObject();
        msg_obj.setString("type", "texts");
        msg_obj.setString("input", input);
        last_input = input;
        msg_obj.setString("result", result);
        msg_obj.setLong("timeout", timeout);
        last_result = result;
        ws.sendMessage(msg_obj.toString());
    }

    void webSocketServerEvent(String msg) {
        PApplet.println(msg);
        try {
            JSONObject msg_obj = JSONObject.parse(msg);
            switch(msg_obj.getString("type")) {
                case "connect":
                    PApplet.println("client connected");
                    send_status();
                    break;
                case "answer":
                    interceptReceived(msg_obj.getString("content"));
                    PApplet.println("answer: "+msg_obj.getString("content"));
                    break;
                case "cancel":
                    cancel();
                    break;
                case "suspend":
                    suspend_timeout(msg_obj.getInt("time"));
                    break;
                default:
                    PApplet.println("unknown message: "+msg);
            }
        }
        catch(Exception exc) {
            PApplet.println("unknown message: "+msg);
        }
    }


    void send_status() {
        JSONObject msg_obj = new JSONObject();
        msg_obj.setString("type", "status");
        if (state == USER_INPUT) {
            msg_obj.setString("status", "USER_INPUT" );
        } else { // ORACLE THINKS... send user input, oracle thought and timeout
            msg_obj.setString("status", "ORACLE_THINKS" );
            msg_obj.setString("user_msg", last_input);
            msg_obj.setString("oracle_thought", last_result);
            msg_obj.setInt("timeout", 10); // TODO send correct remaining timeout
        }
        PApplet.println("sending",msg_obj);
        ws.sendMessage(msg_obj.toString());
    }

    // sent for std timeout
    static public void oracleThinksTimeout() {
        // thats why static references kindof suck...
        // this is null, when server has been started: Settings.START_WEBSERVER
        if(me != null) {
            oracleThinksTimeout(me.last_result);
        }
    }

    // sent when intercept done
    static public void oracleThinksTimeout(String message) {
        if(me != null) {
            JSONObject msg_obj = new JSONObject();
            msg_obj.setString("type", "oracleDone");
            msg_obj.setString("content", message);
            me.ws.sendMessage(msg_obj.toString());
        }
    }

    void suspend_timeout(int millis) {
        oracle.cli.suspendTyper(millis);
    }

    void interceptReceived(String message) {
        me.last_result = message;
        oracle.intercept(message);
        //System.out.println("intercept done");
    }

    static public void sendTyping(char character) {
        if(me != null) {
            JSONObject msg_obj = new JSONObject();
            msg_obj.setString("type", "typing");
            msg_obj.setString("content", "" + character);
            me.ws.sendMessage(msg_obj.toString());
        }
    }

    static public void sendTypingBackspace() {
        if(me != null) {
            JSONObject msg_obj = new JSONObject();
            msg_obj.setString("type", "typing_backspace");
            me.ws.sendMessage(msg_obj.toString());
        }
    }

    private void cancel() {
        oracle.cli.typeNow();
    }
}
