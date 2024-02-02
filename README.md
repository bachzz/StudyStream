# StudyStream

Stream your learning with performance analysis 
<div><video controls src="https://github.com/bachzz/StudyStream/assets/22543582/d139864f-4ce5-47f4-bc63-fbac3ffb1fec" muted="true"></video></div>

## **STUDY-STREAM**: Web GUI client

### Features
- video call: multiple users
- chat between users
- visualize attention score of user (currently: only 1st user)

### How to run
- go to `study-stream` folder
- install nodejs: https://nodejs.org/en/download/
- install yarn: `npm install --global yarn`
- install packages: `yarn install`
- run server: `yarn dev`

## **STREAM-ANALYZER**: Analyze user's facial video stream, returns attention score

### Features
- uses pyppeteer running daemon Chrome browser to crawl user's live video frames
- uses [HRNet](https://github.com/HRNet/HRNet-Facial-Landmark-Detection) to extract facial landmarks -> eye landmarks
- multi-threading: 
    - 1 thread to run daemon browser crawling frames -> computing EAR -> using pre-trained XGBoost model to predict attention score
    - 1 thread to communicate with Web GUI client: send results (attention score + EAR ratio)
- predicting attention score based on [Eye-Aspect-Ratio (EAR)](https://ieeexplore.ieee.org/document/9857021)

### How to run
- go to `stream-analyzer` folder
- add new conda environment and install packages: `conda env create --name study-stream --file environment.txt`
- activate environment: `conda activate study-stream`
- run analyzer: `python analyzer.py`
- `ctrl + C` to close

## TO-DO:

- improve attention prediction: no computing EAR ratio (set to 0 ?) when no face or no left eye
- analyzer: handle multiple users
- implement SVD-based approach
