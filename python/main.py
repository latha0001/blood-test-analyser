from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import logging
from typing import Optional

from crewai import Crew, Process
from agents import medical_analyst, report_verifier, health_advisor
from tasks import analyze_blood_report, verify_document, provide_health_guidance

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Blood Test Report Analyzer API",
    description="AI-powered blood test report analysis and health recommendations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_analysis_crew(query: str, file_path: str):
    """
    Run the medical analysis crew to process blood test report
    
    Args:
        query (str): User's specific question or request
        file_path (str): Path to the uploaded blood test report
        
    Returns:
        dict: Analysis results from the crew
    """
    try:
        logger.info(f"Starting analysis crew for query: {query}")
        
        # Create the medical analysis crew
        medical_crew = Crew(
            agents=[report_verifier, medical_analyst, health_advisor],
            tasks=[verify_document, analyze_blood_report, provide_health_guidance],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the crew with the provided inputs
        inputs = {
            'query': query,
            'file_path': file_path
        }
        
        result = medical_crew.kickoff(inputs)
        
        logger.info("Analysis crew completed successfully")
        return {
            "status": "success",
            "analysis": str(result),
            "crew_execution": "completed"
        }
        
    except Exception as e:
        logger.error(f"Error in analysis crew: {str(e)}")
        return {
            "status": "error",
            "message": f"Analysis failed: {str(e)}",
            "crew_execution": "failed"
        }

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Blood Test Report Analyzer API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": "Blood Test Report Analyzer",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/analyze - POST - Upload and analyze blood test reports",
            "health": "/health - GET - Service health status"
        }
    }

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(..., description="Blood test report PDF file"),
    query: str = Form(default="Please analyze my blood test report and provide a comprehensive summary", 
                     description="Specific question or analysis request")
):
    """
    Analyze uploaded blood test report and provide comprehensive health insights
    
    Args:
        file: PDF file containing the blood test report
        query: Specific question or analysis request from the user
        
    Returns:
        JSON response with analysis results
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF files are supported. Please upload a PDF blood test report."
        )
    
    # Generate unique filename to avoid conflicts
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        logger.info(f"Saving uploaded file: {file.filename}")
        with open(file_path, "wb") as f:
            content = await file.read()
            if len(content) == 0:
                raise HTTPException(status_code=400, detail="Uploaded file is empty")
            f.write(content)
        
        # Validate and clean query
        if not query or query.strip() == "":
            query = "Please analyze my blood test report and provide a comprehensive summary"
        
        query = query.strip()[:1000]  # Limit query length
        
        logger.info(f"Processing analysis for file: {file.filename}, Query: {query[:100]}...")
        
        # Run the analysis crew
        analysis_result = run_analysis_crew(query=query, file_path=file_path)
        
        if analysis_result["status"] == "error":
            raise HTTPException(status_code=500, detail=analysis_result["message"])
        
        return {
            "status": "success",
            "query": query,
            "analysis": analysis_result["analysis"],
            "file_processed": file.filename,
            "file_size_bytes": len(content),
            "processing_id": file_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing blood report: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"An unexpected error occurred while processing your blood report: {str(e)}"
        )
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup file {file_path}: {cleanup_error}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)