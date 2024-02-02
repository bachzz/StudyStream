# StudyStream

Stream your learning with performance analysis 

## **study-stream**: Web GUI client

- go to `study-stream` folder
- install nodejs: https://nodejs.org/en/download/
- install yarn: `npm install --global yarn`
- install packages: `yarn install`
- run server: `yarn dev`

## **stream-analyzer**: Analyze user's facial video stream, returns attention score

- go to `stream-analyzer` folder
- add new conda environment and install packages: `conda env create --name study-stream --file environment.txt`
- activate environment: `conda activate study-stream`
- run analyzer: `python analyzer.py`
- `ctrl + C` to close

## TO-DO:

- improve attention prediction: no computing EAR ratio (set to 0 ?) when no face or no left eye
- analyzer: handle multiple users