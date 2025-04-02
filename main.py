import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import File, Form
from fastapi.responses import JSONResponse
from helper import config_gai, extract_text_from_pdf, prepare_prompt, get_gai_response


app = FastAPI() # Create a FastAPI app


 # Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


load_dotenv() # Load environment variables from .env file


api_key = os.getenv("GOOGLE_API_KEY") # Get the API key from the environment variables


 # Create a route for the root URL
@app.get("/")
def read_root():
    return {"Hello": "World"}


 # Create a route to compute the CV score
@app.post("/compute_cvScore/")
# This commented function is used to test the prompt with Fastapi's Swagger implementation
# async def create_upload_file(jd: str = Form(...), cv: UploadFile = File(...)):

async def create_upload_file(request:Request):

    form = await request.form()
    cv_file = form.get("cv_file")
    cv_content = form.get("cv_content")
    jd_file = form.get("jd_file")
    jd_content = form.get("jd_content")

    # Display the form data for debugging
    print("cv_file", cv_file)
    print("cv_content", cv_content)
    print("jd_file", jd_file)
    print("jd_content", jd_content)
    
    if not api_key:
        return JSONResponse(content={"error": "API key not found"})
        
    try:
        config_gai(api_key)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})    
    
    try:
        cv_text = extract_text_from_pdf(cv_file.file) if (cv_content is None) else cv_content
        jd_text = extract_text_from_pdf(jd_file.file) if (jd_content is None) else jd_content
        input_prompt = prepare_prompt(cv_text, jd_text)
        response = get_gai_response(input_prompt)
        response_json = json.loads(response)
        return JSONResponse(content=response_json)   
    except Exception as e:
        return JSONResponse(content={"Error": str(e)})