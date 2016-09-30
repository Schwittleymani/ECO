package oracle.gif;

import gifAnimation.Gif;
import oracle.Oracle;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.*;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Created by raminsoleymani on 30/09/16.
 */
public class GifDisplayer {

    Oracle oracle;
    String baseFolder = "gifs/";
    public Gify gify;




    public GifDisplayer(Oracle oracle) {
        this.oracle = oracle;
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
        List<String> gifs = gify.getSearchURLs(searchWords);
        StringJoiner joiner = new StringJoiner("_");
        Arrays.stream(searchWords).forEach(w -> joiner.add(w));
        List<String> gifPaths = gify.downloadGifs(joiner.toString(), gifs);
        gifPaths.stream().forEach(System.out::println);
        return gifPaths.stream().limit(number).map(path ->
                new Gif(oracle, path)).collect(Collectors.toList());
    }
}
