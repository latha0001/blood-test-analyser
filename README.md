# Blood Test Report Analyzer API

A FastAPI-based application that uses AI agents to analyze blood test reports and provide comprehensive health insights. The system employs CrewAI with multiple specialized agents to verify, analyze, and provide recommendations based on uploaded blood test reports.

## Important Disclaimer

**This application is for educational and informational purposes only. It does not provide medical advice, diagnosis, or treatment recommendations. Always consult with qualified healthcare professionals for medical advice and interpretation of your blood test results.**

## Bugs Fixed

### Critical Issues Identified and Resolved:

1. **Inappropriate Agent Behavior**
   - **Problem**: Original agents were designed to provide misleading medical advice, make up facts, and ignore safety protocols
   - **Fix**: Completely rewrote all agents with professional, evidence-based roles focused on accurate analysis

2. **Dangerous Task Descriptions**
   - **Problem**: Tasks encouraged fabricating medical information and providing unreliable health advice
   - **Fix**: Redesigned all tasks to follow medical best practices and emphasize the need for professional consultation

3. **Poor Error Handling**
   - **Problem**: Minimal error handling could lead to crashes and poor user experience
   - **Fix**: Added comprehensive error handling, logging, and validation throughout the application

4. **File Processing Issues**
   - **Problem**: Basic file handling without proper validation or cleanup
   - **Fix**: Added file type validation, size limits, proper cleanup, and robust PDF processing

5. **Missing Documentation**
   - **Problem**: No proper API documentation or setup instructions
   - **Fix**: Added comprehensive README with setup instructions, API documentation, and usage examples

6. **Security Vulnerabilities**
   - **Problem**: No file upload restrictions or input validation
   - **Fix**: Added file type validation, size limits, input sanitization, and CORS configuration

7. **Inconsistent Task Structure**
   - **Problem**: Tasks had unclear objectives and unreliable outputs
   - **Fix**: Restructured tasks with clear descriptions, expected outputs, and proper agent assignments

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Serper API key (optional, for web search functionality)

### Installation

1. **Clone or download the project files**

2. **Navigate to the python directory**
   bash
   cd python

3. **Create a virtual environment**
   bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate

4. **Install dependencies**
   bash
   pip install -r requirements.txt
   

5. **Set up environment variables**
   bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env file and add your API keys
   OPENAI_API_KEY=your_openai_api_key_here
   SERPER_API_KEY=your_serper_api_key_here


6. **Create data directory**
   bash
   mkdir data
   

### Running the Application

1. **Start the FastAPI server**
   bash
   python main.py
   
   Or using uvicorn directly:
   bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload

2. **Access the application**
   - API: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## API Documentation

### Endpoints

#### `GET /`
Health check endpoint that returns basic service information.

**Response:**
json
{
  "message": "Blood Test Report Analyzer API is running",
  "version": "1.0.0",
  "status": "healthy"
}

#### `GET /health`
Detailed health check with endpoint information.

**Response:**
json
{
  "status": "healthy",
  "service": "Blood Test Report Analyzer",
  "version": "1.0.0",
  "endpoints": {
    "analyze": "/analyze - POST - Upload and analyze blood test reports",
    "health": "/health - GET - Service health status"
  }
}

#### `POST /analyze`
Main endpoint for analyzing blood test reports.

**Parameters:**
- `file` (required): PDF file containing the blood test report
- `query` (optional): Specific question or analysis request

**Example Request:**
bash
curl -X POST "http://localhost:8000/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@blood_test_report.pdf" \
  -F "query=What are my cholesterol levels and what do they mean?"


**Response:**
json
{
  "status": "success",
  "query": "What are my cholesterol levels and what do they mean?",
  "analysis": "Detailed analysis of the blood test report...",
  "file_processed": "blood_test_report.pdf",
  "file_size_bytes": 245760,
  "processing_id": "uuid-string"
}

### Error Responses

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Invalid file type or empty file
- `500 Internal Server Error`: Processing errors or system failures

Example error response:
json
{
  "detail": "Only PDF files are supported. Please upload a PDF blood test report."
}

## Architecture

### Agents

1. **Medical Analyst**: Analyzes blood test reports and provides evidence-based insights
2. **Report Verifier**: Validates document authenticity and extracts key information
3. **Health Advisor**: Provides general health recommendations while emphasizing professional consultation

### Tasks

1. **Document Verification**: Ensures uploaded files are legitimate blood test reports
2. **Blood Report Analysis**: Comprehensive analysis of blood markers and values
3. **Health Guidance**: General recommendations and guidance for next steps

### Tools

1. **BloodTestReportTool**: PDF processing and text extraction
2. **HealthAnalysisTool**: Blood marker analysis and interpretation
3. **ReportValidationTool**: Document validation and quality assessment

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Required for AI agent functionality
- `SERPER_API_KEY`: Optional for web search capabilities
- `DEBUG`: Enable debug mode (default: True)
- `LOG_LEVEL`: Logging level (default: INFO)
- `MAX_FILE_SIZE_MB`: Maximum upload file size (default: 10MB)

### File Upload Limits

- Maximum file size: 10MB
- Supported formats: PDF only
- Files are automatically cleaned up after processing

## Testing

### Manual Testing

1. **Test the health endpoint**
   bash
   curl http://localhost:8000/health
   

2. **Test file upload with a sample PDF**
   bash
   curl -X POST "http://localhost:8000/analyze" \
     -F "file=@sample_blood_test.pdf" \
     -F "query=Analyze my blood test results"
   

### Using the Interactive Docs

1. Navigate to http://localhost:8000/docs
2. Click on the `/analyze` endpoint
3. Click "Try it out"
4. Upload a PDF file and enter a query
5. Click "Execute" to test the API

## Security Considerations

- File type validation (PDF only)
- File size limits (10MB maximum)
- Input sanitization for queries
- Automatic cleanup of uploaded files
- CORS configuration for web access
- No storage of sensitive medical data

## Usage Examples

### Basic Analysis
python
import requests

url = "http://localhost:8000/analyze"
files = {"file": open("blood_test.pdf", "rb")}
data = {"query": "Summarize my blood test results"}

response = requests.post(url, files=files, data=data)
print(response.json())


### Specific Query
python
files = {"file": open("blood_test.pdf", "rb")}
data = {"query": "Are my cholesterol levels normal? What should I do about them?"}

response = requests.post(url, files=files, data=data)
analysis = response.json()["analysis"]
print(analysis)


## Limitations

- Only supports PDF files
- Requires OpenAI API access
- Analysis is for informational purposes only
- Not a substitute for professional medical advice
- Limited to English language reports
- Requires clear, readable PDF text (not scanned images)
