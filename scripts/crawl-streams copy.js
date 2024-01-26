const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    // const VIEWPORT = { width: 1360, height: 780};
    // await page.setViewport(VIEWPORT);
    await page.goto('http://127.0.0.1:5173/');
    //   await page.screenshot({ path: './tmp/example.png' });

    const client = await page.target().createCDPSession()
    await client.send('Page.setDownloadBehavior', {
    behavior: 'allow',
    downloadPath: './tmp',
    })


    const el = await page.$('#btn-spectate');

    // await page.screenshot({ path: './tmp/tmp.png' });
    await el.click();

    const readLoop = async() => {
        const res = await page.waitForSelector('video');
        // console.log(res);
        const vidsHandle = await page.$$('video');
        // await new Promise(function(resolve) { 
        //         setTimeout(resolve, 1000)
        // });

        await vidsHandle[0].screenshot({ path: './tmp/0.png'});
        // vidsHandle.forEach(async (vidHandle, i) => {
        //     await vidHandle.screenshot({ path: './tmp/'+i+'.png'});
        //     //await V
        // })
        
        return readLoop() // run the loop again
    }
    
    // invoke it for infinite callbacks without any delays at all
    await readLoop();

    await browser.close();
})();
