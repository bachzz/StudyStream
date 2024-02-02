# StudyStream

Stream your learning with performance analysis 
<div><video controls src="https://github.com/bachzz/StudyStream/assets/22543582/dc37ae21-59ac-4bba-8e83-652d768c1d7b" muted="true"></video></div>

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
