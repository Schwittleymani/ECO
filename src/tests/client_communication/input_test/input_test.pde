
import http.requests.*;

/*
  Test the eco python server
 
 */
void setup() {
  while (true) {
    println("*********************");
    String text = "show me what you got!";
    //PostRequest post = new PostRequest("http://localhost:8090/input");
    PostRequest post = new PostRequest("http://lyrik.ddns.net:8090/input");
    post.addData("inputS", text);
    try {
      long millis = millis();
      post.send();
      println("sending...");
      
      println("Reponse Content: " + post.getContent());
      if (post != null) {
        println("Reponse Content-Length Header: " + post.getHeader("Content-Length"));
        long millisDiff = millis() - millis;
        println("That took " + millisDiff + "ms");
      }
    } 
    catch(Exception exc) {
      exc.printStackTrace();
    }
    delay(5000);
  }
}