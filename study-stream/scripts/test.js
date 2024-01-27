const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('http://127.0.0.1:5173/');
    //   await page.screenshot({ path: './tmp/example.png' });

    const client = await page.target().createCDPSession()
    await client.send('Page.setDownloadBehavior', {
    behavior: 'allow',
    downloadPath: './tmp',
    })

    // // page.on('console', msg => console.log(msg.text()));
    // // page.evaluate(() => console.log('hello'));
    // page.on('console', async msg => {
    //     const args = await msg.args()
    //     args.forEach(async (arg) => {
    //       const val = await arg.jsonValue()
    //       // value is serializable
    //       if (JSON.stringify(val) !== JSON.stringify({})) console.log(val)
    //       // value is unserializable (or an empty oject)
    //       else {
    //         if (typeof arg._remoteObject !== 'undefined'){
    //             const { type, subtype, description } = arg._remoteObject
    //             console.log(`type: ${type}, subtype: ${subtype}, description:\n ${description}`)
    //         } else console.log('arg._remoteObject undefined', arg);
    //       }
    //     })
    //   });

    const el = await page.$('#btn-spectate');

    await el.click();
    // await page.evaluate(async() => {
    //     await new Promise(function(resolve) { 
    //            setTimeout(resolve, 5000)
    //     });
    // });

    const readLoop = async() => {
        const res = await page.waitForSelector('video');
        console.log(res);
        const videoHandle = await page.$('video');
        await videoHandle.screenshot({ path: './tmp/1.png' });

        // const html = await page.content();
        // cant = await readOdds(html);
        // await page.screenshot({ path: './tmp/0.png' });

        // var vids = await page.$('video')
        // console.log(vids);
        // await page.$$eval('video', elHandles => elHandles.forEach((el) => {
        //     console.log(el);
        // }))

        // await page.evaluate(() => {
        //     // console.log('hello');
        //     var vids = document.querySelectorAll('video');
        //     var canvas = document.createElement('canvas');
        //     canvas.width = 640;
        //     canvas.height = 480;
        //     var ctx = canvas.getContext('2d');
        //     console.log(vids['0']);
        //     // ctx.drawImage(vids[0], 0, 0, canvas.width, canvas.height);

        //     // var image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
        //     // console.log(image);
            
        //     // var link = await page.$('#link-0');
        //     // link.setAttribute('download', '0.png');
        //     // link.setAttribute('href', image);
        //     // link.click();
        // });

        // var canvas = document.createElement('canvas'); //await page.$$('canvas');
        // console.log(canvas);

        // const vids = await page.$$('video');
        // const canvas = await page.$$('canvas');
        // for (const [i, vid] of vids.entries()){
        //     // const html = await page.content();
        //     // var canvas = document.createElement('canvas');
        //     // const canvas = await page.$('#canvas0');
        //     var ctx = await canvas[i].evaluate( el => el.getContext('2d') );
        //     ctx.drawImage(vid, 0, 0, canvas[i].width, canvas[i].height);

        //     var image = canvas[i].toDataURL("image/png").replace("image/png", "image/octet-stream");
        //     console.log(image);
        // }

        // var canvas = document.createElement('canvas');
        // canvas.width = 640;
        // canvas.height = 480;
        // var ctx = canvas.getContext('2d');
        // ctx.drawImage(vids[0], 0, 0, canvas.width, canvas.height);

        // var image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");

        // var link = await page.$('#link-0');
        // link.setAttribute('download', '0.png');
        // link.setAttribute('href', image);
        // link.click();

        return readLoop() // run the loop again
    }
    
    // invoke it for infinite callbacks without any delays at all
    await readLoop();

    await browser.close();
})();
