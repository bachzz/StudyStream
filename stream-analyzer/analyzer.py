## basic libs
import asyncio
from pyppeteer import launch
import time
import os
import glob
from PIL import Image
import numpy as np
import torch
import argparse

## HRNet - facial landmark libs
import tools.HRNet_Facial_Landmark_Detection.lib.models as models
from tools.HRNet_Facial_Landmark_Detection.lib.config import config, update_config
from tools.HRNet_Facial_Landmark_Detection.lib.core.evaluation import decode_preds

## classifier libs
from xgboost import XGBClassifier
import pickle

## other libs
from datetime import datetime
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from urllib.parse import urlparse, parse_qs

# Shared dictionary variable
data_json = {
    "data": []
}

# Lock for synchronizing access to the shared dictionary
dict_lock = threading.Lock()


########## SERVER's thread functions #############
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global shared_dict
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        with dict_lock:
            self.wfile.write(bytes(json.dumps(data_json), "utf8"))

def run_server(server_class=HTTPServer, handler_class=RequestHandler, port=3000):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd...')


    

########## ANALYZER's thread Functions #############

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


async def analyzer_loop():
    global data_json
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
    hrnet_model = models.get_face_alignment_net(config)

    ## load HRNet model
    state_dict = torch.load(args.model_file, map_location=torch.device('cpu'))
    hrnet_model.load_state_dict(state_dict)
    hrnet_model.eval()

    ## load XGBoost model
    xgb_model = pickle.load(open('./model/xgb_EAR.pkl', "rb"))

    ## json data output file
    data_json = {
        "data": []
    }
    max_num_results = 50

    ## init values
    seq_len=20
    EAR_arr = np.full((seq_len), np.nan)
    idx = 0
    id = 0

    while True:
        if (idx == seq_len):
            await shiftFiles()
            os.remove('./tmp\\-1.png')
            idx = seq_len - 1

        ## crawl
        await crawl(page, idx) #page.screenshot({'path': 'example.png', 'fullPage': True})
        
        ## eye landmarks extraction -> compute EAR -> store in EAR_arr
        im = Image.open(f'./tmp\\{idx}.png').convert('RGB')
        im = np.array(im.resize((640, 480), Image.BICUBIC))
        # breakpoint()
        EAR_cur = await compute_EAR(hrnet_model, im)
        print(f'\nEAR values = {EAR_arr}')

        EAR_arr[:-1] = EAR_arr[1:] ## shift EAR values
        EAR_arr[-1] = EAR_cur ## replace last value with current EAR
        
        ## model predict when EAR contains all valid values (when enough frames collected)
        if True not in np.isnan(EAR_arr):
            ## compute features
            q1_feat = np.quantile(EAR_arr, 0.25)
            q2_feat = np.quantile(EAR_arr, 0.5)
            q3_feat = np.quantile(EAR_arr, 0.75)
            mean_feat = np.mean(EAR_arr)
            sd_feat = np.std(EAR_arr)
            mad_feat = np.median(abs(EAR_arr - np.median(EAR_arr)))

            ## model predict with computed features
            x = np.array([[mean_feat, sd_feat, q1_feat, q2_feat, q3_feat, mad_feat]])
            score = xgb_model.predict_proba(x)[0][1]
            print(f'current batch - attention score = {score}')

            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            data = {'id':id, 'prob': '{:.2f}'.format(score), 'EAR_cur': '{:.2f}'.format(EAR_cur), 'time':date}


            ## if number of results > max_num_results -> shift data results -> avoid memory leak
            if len(data_json['data']) >= max_num_results:
                data_json['data'][:-1] = data_json['data'][1:] 
                data_json['data'][-1] = data
            else:
                data_json['data'].append(data)

            # print(data_json)
            # with open("prediction-data.json", 'w', encoding='utf-8') as fp:
            #     json.dump(data_json, fp, ensure_ascii=False)
            # with open("prediction-data.json", 'w') as fp:
            #     time.sleep(0.5)
            #     json.dump(data_json, fp)

        idx = idx+1
        id = id+1

    await browser.close()


# def update_results_dict():
#     # global shared_dict
#     # while True:
#     #     with dict_lock:
#     #         # Modify the shared dictionary here
#     #         shared_dict["key"] = "new value"
#     #         print("Dictionary modified:", shared_dict)
#     #     time.sleep(5)  # Modify every 5 seconds
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     future = asyncio.ensure_future(analyzer_loop())
#     loop.run_until_complete(future)

def start_async_loop():
    asyncio.run(analyzer_loop())


if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    # modifier_thread = threading.Thread(target=update_results_dict)

    server_thread.start()
    # modifier_thread.start()
    start_async_loop()

    server_thread.join()
    # modifier_thread.join()