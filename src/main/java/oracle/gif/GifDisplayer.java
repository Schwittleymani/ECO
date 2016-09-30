package oracle.gif;

import gifAnimation.Gif;
import oracle.Oracle;

import java.io.File;
import java.util.*;
import java.util.List;

/**
 * Created by raminsoleymani on 30/09/16.
 */
public class GifDisplayer {

    Oracle oracle;
    String baseFolder = "gifs/";
    Gify gify;

    public boolean downloadGifys;

    //private boolean asynGifyRequestRunning = false;
    private boolean asyncGifysAvailable = false;
    private List<Gif> asyncGifys = new ArrayList<Gif>();


    public GifDisplayer(Oracle oracle) {
        this.oracle = oracle;
        downloadGifys = oracle.settings.DOWNLOAD_GIFY;
        gify = new Gify();
        gify.downloadFolder = oracle.sketchPath() + "/data/gifs/gify/";
    }

    public Gif getRandomCleanGif() {
        return getRandomGif("clean");
    }

    public Gif getRandomGif(String gifFolder) {
        File folder = new File(oracle.sketchPath() + "/data/gifs/" + gifFolder);
        String[] files = folder.list();
        Random rnd = new Random();
        System.out.println(gifFolder + "/" + files[rnd.nextInt(files.length)]);
        return new Gif(oracle, baseFolder + gifFolder + "/" + files[rnd.nextInt(files.length)]);
    }


    /**
     * @param searchWords
     * @param number      maximum number of gifs (-1) for all
     * @return a list of gifs
     */
    public List<Gif> getGiyGifs(String[] searchWords, int number) {
        List<String> gifs = gify.getSearchURLs(searchWords, number);

        //gifs.stream().forEach(System.out::println);
        if(downloadGifys) {
            StringJoiner joiner = new StringJoiner("_");
            Arrays.stream(searchWords).forEach(w -> joiner.add(w));
            gifs = gify.downloadGifs(joiner.toString(), gifs);
        }

        // this crap was nicer then the stream in the end cuz it allows to catch exceptions
        ArrayList<Gif> gg= new ArrayList<Gif>();
        int counter = 0;
        for(String s : gifs) {
            System.out.println(s);
            try {
                gg.add(new Gif(oracle, s));
                if (++counter == number) {
                    break;
                }
            } catch (NullPointerException damn) {
                System.out.println("missing gif"+ counter);
            }

        }
        return gg;
    }

    public void getGiyGifsAsnyc(String[] searchWords, int number) {
        Thread getGifysThread = new Thread(new Runnable() {
            List<Gif> gg;
            @Override
            public void run() {
                asyncGifysAvailable = false;
                asyncGifys = getGiyGifs(searchWords,number);
                asyncGifysAvailable = true;
            }
        });
        getGifysThread.start();
    }

    public boolean getAsyncGifysAvailable() {
        return asyncGifysAvailable;
    }

    public List<Gif> getAsyncGifys() {
        asyncGifysAvailable = false;
        return asyncGifys;
    }

}
