import asyncio
from pyppeteer import launch
import time
import os
import glob
from PIL import Image
import numpy as np
import torch
import argparse

import tools.HRNet_Facial_Landmark_Detection.lib.models as models
from tools.HRNet_Facial_Landmark_Detection.lib.config import config, update_config
from tools.HRNet_Facial_Landmark_Detection.lib.core.evaluation import decode_preds

import matplotlib.pyplot as plt


async def shiftFiles():
    fnames = sorted(glob.glob("./tmp/*"), key=lambda x: int(x.split('\\')[-1].split('.png')[0]))

    for fname in fnames:
        idx_ = int(fname.split('\\')[-1].split('.png')[0])-1
        fname_ = f"./tmp\\{idx_}.png"
        os.rename(fname, fname_)

async def crawl(page, idx):
    # await page.screenshot({'path': 'example.png', 'fullPage': True})
    await page.waitForSelector('video')

    vidsHandle = await page.JJ('video')

    # time.sleep(0.01)
    await vidsHandle[0].screenshot({ 'path': f'./tmp/{idx}.png'})

async def compute_EAR(model, im):
    im_ = im.astype(np.float32)
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    im_ = (im_ / 255.0 - mean) / std
    im_ = torch.from_numpy(im_).permute(2,0,1).unsqueeze(0)
    # breakpoint()
    # t = time.time()
    output = model(im_)
    # print(f"[HRNet] {fname} - Elapsed time = {time.time()-t}")
    score_map = output.data.cpu()
    preds = decode_preds(score_map, torch.tensor([[128.0,128.0]]), torch.tensor([1.28]), [64, 64])

    idx=0
    left_idx = [60,61,62,63,64,65,66,67]
    left_coords = np.zeros((8,2))
    for x,y in preds[0]:
        x, y = int(x), int(y)
        if idx in left_idx:
            left_coords[left_idx.index(idx)] = [x,y]
            # cv2.circle(frame, (x,y), 1, (0, 0, 255), 2)
        idx = idx+1
    left_coords_min = left_coords.min(axis=0).astype(int)
    left_coords_max = left_coords.max(axis=0).astype(int)
    left_w, left_h = left_coords_max-left_coords_min

    ## compute EAR 
    p1 = left_coords[0]; p2 = left_coords[1]; p3 = left_coords[3]; p4 = left_coords[4]; p5=left_coords[5]; p6=left_coords[7]
    EAR_ratio = (np.linalg.norm(p2-p6) + np.linalg.norm(p3-p5))/(2*np.linalg.norm(p1-p4))

    left_coords_start = left_coords_min-(int(left_w*0.25), int(left_h*0.5))
    left_coords_end = left_coords_max+(int(left_w*0.25), int(left_h*0.5))
    MIN_HEIGHT_RESIZE = 16
    if left_coords_end[1]-left_coords_start[1] < MIN_HEIGHT_RESIZE:
        left_coords_end[1] = left_coords_start[1]+int(MIN_HEIGHT_RESIZE/2)
        left_coords_start[1] = left_coords_start[1]-int(MIN_HEIGHT_RESIZE/2)
    left_coords_start = tuple(left_coords_start)
    left_coords_end = tuple(left_coords_end)
    eye_im = im[left_coords_start[1]:left_coords_end[1],left_coords_start[0]:left_coords_end[0],:]
    # breakpoint()
    return EAR_ratio

async def main():
    browser = await launch(executablePath='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
    page = await browser.newPage()
    await page.goto('http://localhost:5173/') #('http://127.0.0.1:5173/')
    
    # await page.screenshot({'path': 'example.png', 'fullPage': True})
    client = await page.target.createCDPSession()
    await client.send('Page.setDownloadBehavior', {
        'behavior': 'allow',
        'downloadPath': './tmp',
    })
    el = await page.J('#btn-spectate')
    await el.click()

    # while True: await page.screenshot({'path': 'example.png', 'fullPage': True})
    ### HRNet init
    HRNET_BASE_DIR = './tools/HRNet_Facial_Landmark_Detection'
    parser = argparse.ArgumentParser(description='Real-time webcam demo')
    parser.add_argument('--cfg', help='experiment configuration filename', type=str,
                        default=f'{HRNET_BASE_DIR}/experiments/wflw/face_alignment_wflw_hrnet_w18.yaml')
    parser.add_argument('--model-file', help='model parameters', type=str,
                        default=f'{HRNET_BASE_DIR}/hrnetv2_pretrained/HR18-WFLW.pth')

    args = parser.parse_args()
    update_config(config, args)

    config.defrost()
    config.MODEL.INIT_WEIGHTS = False
    config.freeze()
    model = models.get_face_alignment_net(config)

    # load model
    state_dict = torch.load(args.model_file, map_location=torch.device('cpu'))
    model.load_state_dict(state_dict)
    model.eval()

    seq_len=20
    EAR_arr = np.full((1, seq_len), np.nan)
    idx = 0

    while True:
        if (idx == seq_len):
            await shiftFiles()
            os.remove('./tmp\\-1.png')
            idx = seq_len - 1

        ### crawl
        await crawl(page, idx) #page.screenshot({'path': 'example.png', 'fullPage': True})
        
        ### eye landmarks extraction -> compute EAR -> store in EAR_arr
        im = Image.open(f'./tmp\\{idx}.png').convert('RGB')
        im = np.array(im.resize((640, 480), Image.BICUBIC))
        # breakpoint()
        ear_ratio = await compute_EAR(model, im)
        # breakpoint()
        print(ear_ratio)

        idx = idx+1

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())