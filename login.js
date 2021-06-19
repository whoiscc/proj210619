const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        userDataDir: 'data',
        headless: false,
    });
})();
