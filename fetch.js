const puppeteer = require('puppeteer');
const fs = require('fs/promises');

(async () => {
    const browser = await puppeteer.launch({
        userDataDir: 'data',
        // headless: false,
    });
        
    const page = await browser.newPage();
    
    async function fetchListPage() {
        console.log(`fetch list page: ${page.url()}`);
        await page.waitForTimeout(1000);  // fixme
        await page.waitForSelector('a.practice');
        const buttonList = await page.$$('a.practice');
        // console.log(buttonList.length);
        for (button of buttonList) {
            // console.log(await button.evaluate(node => node.innerHTML));
            await button.click();
            await page.waitForTimeout(1000);  // fixme
            await fetchPassagePage();
            // break;
        }
    }
    
    async function fetchPassagePage() {
        const pages = await browser.pages();
        const page = pages[pages.length - 1];
        await page.bringToFront();
        console.log(`fetch passage page: ${page.url()}`);
        await page.waitForSelector('#arcScrollContent');
        const article = await page.$('#arcScrollContent');
        const html = await article.evaluate(node => node.innerHTML);
        const title = await page.$eval('div.header-top p', node => node.innerText);
        console.log(title);
        
        await fs.writeFile(`articles/${title}.html`, html);
        // console.log(html);
        page.close();
    }
    
    await page.goto('https://tpo.xdf.cn/practice/read');
    await page.waitForSelector('span.item-nav-link');
    const buttonList = await page.$$('span.item-nav-link');
    // console.log(buttonList.length);
    let i = 0;
    for (button of buttonList) {
        await Promise.all([
            button.click(),
            page.waitForNavigation(),
        ]);
        await fetchListPage();
        // break;
        await page.bringToFront();
    }

    browser.close();    
})();
