# cv-score-be
Analyze CV vs JD and get a score along with details about the Candidate and if they are a good fit for the job.
Also, get skills of teh candidate that match and that are missing.

## Swagger
http://localhost:8000/docs

## Rename .env.example
Rename .env.example to .env and input your Gemini key

## Create Python environment
```sh
python -m venv cv-score-be-env
```
## Activate environment
```sh
source cv-score-be-env scripts/activate (windows)
```
```sh
source cv-score-be-env/bin/activate (mac/linux)
```

## Install dependencies (windows)
```sh
pip install -r requirements.txt
```

## Run Application (windows)
```sh
uvicorn main:app --reload
```
