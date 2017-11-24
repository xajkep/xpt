const fs = require('fs');
const webdriver = require('selenium-webdriver')
const chromedriver = require('chromedriver')
const argv = require('minimist')(process.argv.slice(2));

const url = argv.url;

const chromeCapabilities = webdriver.Capabilities.chrome();
chromeCapabilities.set('chromeOptions', {args: ['--headless', '--disable-web-security', '--disable-xss-auditor']});

const driver = new webdriver.Builder()
    .forBrowser('chrome')
    .withCapabilities(chromeCapabilities)
    .build()

driver.get(url);

// Click on the first <XXX> tag element found
var html_tags = ['div', 'a', 'p', 'input', 'img', 'video', 'button', 'x'];
for(var i = 0; i < html_tags.length; i++) {
  driver.findElement({
    tagName: html_tags[i]
  }).click().then(null, function(e){});
}

driver.switchTo().alert().then(
    function() {
      console.log("alert detected 1337");
    },
    function() {
      console.log("nope");
    }
  );

driver.quit();