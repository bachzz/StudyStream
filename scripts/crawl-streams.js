const puppeteer = require('puppeteer');

const fs = require('fs');


async function shiftFileNames(){
    var fnames = fs.readdirSync('./tmp/0');

    fnames.sort((a,b) => { 
        if(parseInt(a.split('.png')[0]) < parseInt(b.split('.png')[0])) { return -1; }
        if(parseInt(a.split('.png')[0]) > parseInt(b.split('.png')[0])) { return 1; }
        return 0;
    } )
    // console.log(fnames);
    // fnames.forEach(fname => { 
    for (const fname of fnames){
        // console.log(fname + ' - ' + fname_);
        var fname_ = (parseInt(fname.split('.png')[0]) - 1).toString() + '.png';
        fs.renameSync('./tmp/0/'+fname, './tmp/0/'+fname_, () => {}); 
        // console.log(fname + ' - ' + fname_);
    }; 
}

// shiftFileNames();





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

    var idx = 0;
    const readLoop = async() => {
        const res = await page.waitForSelector('video');
        // console.log(res);
        const vidsHandle = await page.$$('video');
        
        // await new Promise(function(resolve) { 
        //         setTimeout(resolve, 100)
        // });

        if (idx==600){
            await shiftFileNames();
            fs.unlinkSync('./tmp/0/-1.png');
            idx = 599;
        }
        
        await vidsHandle[0].screenshot({ path: './tmp/0/'+idx+'.png'});
        
        idx = idx+1;
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
