import http.requests.*;

/*
  Test the eco python server

*/
void setup() {
  while (true) {
    println("*********************");
    PostRequest post = new PostRequest("http://localhost:8090/input");
    post.addData("inputS", "hello ECO");
    try {
    post.send();
    println("Reponse Content: " + post.getContent());
    if (post != null) 
      println("Reponse Content-Length Header: " + post.getHeader("Content-Length"));
    } catch(Exception exc) {
       exc.printStackTrace(); 
    }
    delay(30000);
  }
}