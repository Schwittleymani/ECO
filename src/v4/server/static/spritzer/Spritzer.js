// Inspired by http://jsfiddle.net/vKZLn/1/

var Spritzer = function (el) {
    el.classList.add('spritzed')

    var offsetLeft = 300;

    el.style.padding = (parseInt(window.getComputedStyle(el)['font-size']) / 1.3) + 'px'

	//el.appendChild(document.createElement("div"))

    this.playing = true

    this.currentTimer = null

    function processWord(word) {
        console.log(word)
        var center = Math.floor(word.length / 2),
            letters = word.split('')
        return letters.map(function(letter, idx) {
            if (idx === center)
                return '<span class="highlight">' + letter + '</span>'
            return letter;
        }).join('')
    }

    function positionWord() {
        var wordEl = el.firstElementChild,
            highlight = wordEl.firstElementChild
        
        var centerOffsetX = (highlight.offsetWidth / 2) + highlight.offsetLeft,
            centerOffsetY = (highlight.offsetHeight / 2) + highlight.offsetTop
        
        wordEl.style.left = (offsetLeft - centerOffsetX) + 'px'
        wordEl.style.top = (60 - centerOffsetY) + 'px'
    }

    var currentWord = 0,
        delay
    
    var displayNextWord = function() {
        var word = this.words[currentWord++]
        if (typeof word == 'undefined') {
            return
        }
        // WTB> nlp.js...
        var hasPause = /^\(|[,\.\)]$/.test(word)
        
        // XSS?! :(
       	window.el = el
        el.firstElementChild.innerHTML = word
        positionWord()

        if (currentWord == this.words.length) {
            currentWord = 0, delay
        }
        this.currentTimer = setTimeout(displayNextWord, delay * (hasPause ? 2 : 1))
    }.bind(this)

    this.render = function(text, wpm) {
        text = text.replace(/(\r\n|\n|\r)/gm,"");
        text = text.replace(/ {2,}/g, ' ');
        console.log(text)
        //this.words = text.replace(/^\s+|\s+|\n$/,"")
        this.words = text.split(" ")
        console.log(this.words)
        this.words = this.words.map(processWord)
        console.log(this.words)
        delay = 60000 / wpm

        this.playing = true
        clearTimeout(this.currentTimer)
        displayNextWord()
    }

    this.play = function() {
        this.playing = true
        displayNextWord()
    }

    this.pause = function() {
        this.playing = false
        clearTimeout(this.currentTimer)
    }

    this.toggle = function() {
        if (this.playing)
            this.pause()
        else
            this.play()
    }
}