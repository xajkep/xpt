const fs = require('fs');
const webdriver = require('selenium-webdriver');
const chromedriver = require('chromedriver');
const argv = require('minimist')(process.argv.slice(2));

const url = argv.url;


let CTX = {
    
    'chrome_capabilities': false,
    'driver': false,

    /**
     * Set options
     */
    set_options: function() {

        CTX['chrome_capabilities'] = webdriver.Capabilities.chrome();
        CTX['chrome_capabilities'].set('chromeOptions', {
            args: [
                '--headless', 
                '--disable-web-security', 
                '--disable-xss-auditor',

                // performance tunings
                '--mute-audio',
                '--safebrowsing-disable-auto-update',
                '--safebrowsing-disable-download-protection',
                '--disable-canvas-aa',
                '--disable-accelerated-2d-canvas',
                '--disable-accelerated-jpeg-decoding',
                '--disable-accelerated-mjpeg-decode',
                '--disable-accelerated-video-decode',
                '--disable-composited-antialiasing',
                '--disable-d3d11',
                '--disable-default-apps',
                '--disable-threaded-animation',
                '--disable-threaded-scrolling',
                '--disable-checker-imaging',
                '--disable-image-animation-resync',
            ]
        });


            
        CTX['driver'] = new webdriver.Builder()
            .forBrowser('chrome')
            .withCapabilities(CTX['chrome_capabilities'])
            .build();
    },



    /**
     * Interact with DOM
     */
    interact: function() {
        // Click on the first <XXX> tag element found
        var html_tags = [
            'div', 
            'a', 
            'p', 
            'input', 
            'img', 
            'video', 
            'button', 
            'x',
        ];

        for (var i = 0; i < html_tags.length; i++) {
            let element = CTX['driver'].findElement({
                tagName: html_tags[i],
            })
            
            // click on element
            element.click().then(null, function(e) {

            });
        }

        CTX['driver'].switchTo().alert().then(
            function() {
                console.log("alert detected 1337");
            },
            function() {
                console.log("nope");
            }
        );


        // there is bug in selenium-webdriver 4.0.0 
        // bugfix came from here: https://github.com/SeleniumHQ/selenium/issues/6824
        // CTX['driver'].quit();
        setTimeout(function () {
            CTX['driver'].quit()
        }, 100);

    },

    /**
     * Main
     */
    run: function() {
        CTX.set_options();

        CTX['driver'].get(url);
        
        CTX.interact();
    },
}

try {
    CTX.run(url);
} catch(err) {
    console.debug(err);
}