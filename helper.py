import PyPDF2 as pdf
import google.generativeai as genai
import json


 # Configure the Generative AI API
def config_gai(api_key):
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        raise Exception("Error setting API key: " + str(e))
    

 # Extract text from a PDF file
def extract_text_from_pdf(file_path):
    try:
        reader = pdf.PdfReader(file_path)
        if len(reader.pages) == 0:
            raise Exception("PDF file is empty")
        text = []
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text.append(extracted_text)
            else:
                raise Exception("Error extracting text from PDF")
        return text
    except Exception as e:
        raise Exception("Error extracting text from PDF: " + str(e))
    

 # Prepare the prompt for the Gemini model
def prepare_prompt(cv_text, job_description):
    if not cv_text or not job_description:
        raise Exception("CV text or job description is empty")
    
    prompt = """
    You are a professional Application Tracking System (ATS) software. Your job is to analyze a cv and a job description to determine if the cv is a good match for the job.
    You specialise in identifying key skills, experiences, and qualifications that are relevant to the job description for the following fields:
    - Software Engineering
    - Full-stack Development
    - Product Management
    - Project Management

    Evaluate the cv and job description below and provide a cv_score, summary, matching_keywords, and missing_keywords of the match between the two:

    CV:
    {cv_text}

    Job Description:
    {job_description}

    Provide a response in the following JSON format ONLY:
    {{
        "cv_score": "a floating number between 0 and 10",
        "summary": "detailed summary of the candidate"
        "matching_keywords": ["list of matching keywords"],
        "missing_keywords": ["list of missing keywords"]
    }}
    """
    return prompt.format(
        cv_text = cv_text,
        job_description = job_description
    )
    

 # Get a response from the Gemini model
def get_gai_response(prompt):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", generation_config={"response_mime_type": "application/json"})
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            raise Exception("Error while getting any response from Gemini")
        try:
            response_content = json.loads(response.text)
            required_fields = ["cv_score", "summary", "matching_keywords", "missing_keywords"]
            for field in required_fields:
                if field not in response_content:
                    raise ValueError("Missing field in response: " + field)
            return response.text
        
        except json.JSONDecodeError:
             # If the response is not valid JSON, try to extract the JSON part from the response
            import re
            json_pattern = re.compile(r"\{.*\}")
            json_match = json_pattern.search(json_pattern, response.text, re.DOTALL)
            if json_match:
                return json_match.group(0)
            else:
                raise ValueError("Error parsing JSON response")

    except Exception as e:
        raise Exception("Error getting response from Gemini model: " + str(e))
