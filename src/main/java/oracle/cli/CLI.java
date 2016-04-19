package oracle.cli;

import oracle.ostern.Jesus;
import processing.core.PApplet;
import processing.core.PFont;

import java.io.File;
import java.util.ArrayList;

/**
 * Created by mrzl on 31.03.2016.
 */
public class CLI {
    public static final String LINE_PREFIX_CHARS = "[ ] ";
    private static final int PREF_WORD_LEN = LINE_PREFIX_CHARS.split(" ").length;

    private ArrayList<Line> lines = new ArrayList<>();
    private PApplet parent;
    private PFont font;

    private Jesus jesus;
    private BlinkingRectangle blinker;
    private DelayedTyper delayedTyper;

    private int maxLineWidth = 540;
    private int textSize = 20;

    private int currentY;
    int lineHeight = 30;
    int paddingTop = 25;
    int paddingLeft = 15;

    public CLI(PApplet p) {
        this.parent = p;
        this.font = p.createFont("data" + File.separator + "Glass_TTY_VT220.ttf", textSize);
        this.parent.textFont(this.font);

        jesus = new Jesus(p);
        blinker = new BlinkingRectangle(p, this);
        delayedTyper = new DelayedTyper(this);

        reset();

        parent.textSize(textSize);
        setupWidth();
    }

    public void setupWidth() {
        // limit for the input line
        String widthTestString = "";
        do {
            widthTestString += "a";
        } while (parent.textWidth(widthTestString) < maxLineWidth);
        Line.CHAR_LIMIT = widthTestString.length();
    }

    public void draw() {
        parent.fill(0, 255, 0);

        jesus.drawBeforeEaster();

        pushLinesUp();
        lines.forEach(Line::draw);

        // draws blinking square, rotating or not
        blinker.draw(delayedTyper.isInitDelay());

        // types the text in delayed manner
        if (delayedTyper.update()) {
            newLine(true);
        }

        jesus.drawAfterEaster();
    }

    private void pushLinesUp() {
        int moveUp = 1;
        for (; moveUp > 0; moveUp--) {
            if (lines.get(lines.size() - (moveUp)).y > parent.height)
                break;
        }
        for (int i = 0; i < moveUp; i++) {
            lines.remove(0);
        }
        resetYs();
    }

    void resetYs() {
        currentY = paddingTop;
        for (Line line : lines) {
            line.y = currentY;
            currentY += lineHeight;
        }
    }

    public void backspace() {
        getLastLine().backspace();
    }

    public void finish(String answer, long delayMillis) {
        newLine();
        delayedTyper.addText(answer);
        delayedTyper.addDelay(delayMillis);
    }

    public void type(char c) {
        delayedTyper.type(c);
    }

    public void finishFromWeb(String answer) {
        delayedTyper.addText(answer);
        delayedTyper.addDelay(0);
    }

    // waits for the interception answer
    public void waitForAnswer() {
        newLine();
        delayedTyper.addDelay(Long.MAX_VALUE);
    }

    public void newLine() {
        newLine(false);
    }

    private void newLine(boolean addLinePrefix) {
        currentY += lineHeight;
        Line newLine = new Line(this.parent);
        newLine.setPos(paddingLeft, currentY);
        lines.add(newLine);
        if (addLinePrefix) {
            delayedTyper.type(LINE_PREFIX_CHARS);
        } else {
            // a little bit of more offset on the left
            newLine.setPos(paddingLeft + 40, currentY);
        }
    }

    public Line getLastLine() {
        return lines.get(lines.size() - 1);
    }

    public void reset() {
        lines.clear();

        currentY = paddingTop;
        Line line = new Line(this.parent);
        line.setPos(paddingLeft, currentY);
        lines.add(line);
        delayedTyper.type(LINE_PREFIX_CHARS);
    }

    public boolean available() {
        return getLastLine().getText().split(" ").length >
                PREF_WORD_LEN && delayedTyper.isEmpty();
    }

    public void startEmojiEasterEgg() {
        jesus.start(Jesus.EASTEREGG_TYPE.EMOJI, 10);
    }

    public int getMaxLineWidth() {
        return maxLineWidth;
    }

    public int getTextWidth(String text) {
        return (int) parent.textWidth(text);
    }

    public int getTextSize() {
        return textSize;
    }

    public boolean isActive() {
        return !delayedTyper.isEmpty();
    }

    public boolean inputLimitReached() {
        return getLastLine().getText(false).length() >= Line.CHAR_LIMIT;
    }
}

