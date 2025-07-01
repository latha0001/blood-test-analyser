import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Creating search tool
search_tool = SerperDevTool()

class BloodTestReportTool:
    @staticmethod
    def read_data_tool(path='data/sample.pdf'):
        """
        Tool to read and extract data from a PDF blood test report
        
        Args:
            path (str): Path to the PDF file containing the blood test report
            
        Returns:
            str: Extracted text content from the blood test report
        """
        try:
            # Check if file exists
            if not os.path.exists(path):
                logger.error(f"File not found: {path}")
                return f"Error: File not found at path: {path}"
            
            # Check file size (basic validation)
            file_size = os.path.getsize(path)
            if file_size == 0:
                logger.error(f"File is empty: {path}")
                return f"Error: File is empty: {path}"
            
            if file_size > 10 * 1024 * 1024:  # 10MB limit
                logger.error(f"File too large: {path}")
                return f"Error: File size exceeds 10MB limit: {path}"
            
            # Load and process PDF
            logger.info(f"Loading PDF from: {path}")
            loader = PyPDFLoader(file_path=path)
            docs = loader.load()
            
            if not docs:
                logger.error("No documents loaded from PDF")
                return "Error: Could not extract any content from the PDF file"
            
            # Extract and clean content
            full_report = ""
            for i, doc in enumerate(docs):
                content = doc.page_content.strip()
                if content:
                    # Clean up formatting
                    content = content.replace('\n\n\n', '\n\n')
                    content = content.replace('\t', ' ')
                    # Remove excessive whitespace
                    lines = [line.strip() for line in content.split('\n') if line.strip()]
                    content = '\n'.join(lines)
                    
                    full_report += f"--- Page {i+1} ---\n{content}\n\n"
            
            if not full_report.strip():
                logger.error("No readable content found in PDF")
                return "Error: No readable text content found in the PDF file"
            
            logger.info(f"Successfully extracted {len(full_report)} characters from PDF")
            return full_report.strip()
            
        except Exception as e:
            logger.error(f"Error processing PDF {path}: {str(e)}")
            return f"Error reading PDF file: {str(e)}"

class HealthAnalysisTool:
    @staticmethod
    def analyze_blood_markers(report_content):
        """
        Analyze blood markers from report content
        
        Args:
            report_content (str): Raw text content from blood test report
            
        Returns:
            dict: Structured analysis of blood markers
        """
        try:
            # This is a placeholder for more sophisticated analysis
            # In a real implementation, you would parse specific blood markers
            analysis = {
                "status": "analyzed",
                "content_length": len(report_content),
                "contains_medical_data": any(term in report_content.lower() for term in 
                    ['hemoglobin', 'glucose', 'cholesterol', 'white blood cell', 'red blood cell', 
                     'platelet', 'hematocrit', 'mcv', 'mch', 'mchc']),
                "report_preview": report_content[:500] + "..." if len(report_content) > 500 else report_content
            }
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing blood markers: {str(e)}")
            return {"status": "error", "message": str(e)}

class ReportValidationTool:
    @staticmethod
    def validate_medical_report(content):
        """
        Validate if the content appears to be a legitimate medical report
        
        Args:
            content (str): Text content to validate
            
        Returns:
            dict: Validation results
        """
        try:
            medical_keywords = [
                'laboratory', 'lab', 'blood', 'test', 'result', 'reference', 'range',
                'normal', 'abnormal', 'high', 'low', 'patient', 'specimen', 'collected'
            ]
            
            blood_test_markers = [
                'hemoglobin', 'hgb', 'hematocrit', 'hct', 'glucose', 'cholesterol',
                'triglycerides', 'hdl', 'ldl', 'wbc', 'rbc', 'platelet', 'mcv', 'mch'
            ]
            
            content_lower = content.lower()
            
            medical_score = sum(1 for keyword in medical_keywords if keyword in content_lower)
            blood_test_score = sum(1 for marker in blood_test_markers if marker in content_lower)
            
            validation = {
                "is_medical_document": medical_score >= 3,
                "is_blood_test": blood_test_score >= 2,
                "medical_keyword_count": medical_score,
                "blood_marker_count": blood_test_score,
                "confidence_score": min(100, (medical_score + blood_test_score) * 10)
            }
            
            return validation
            
        except Exception as e:
            logger.error(f"Error validating report: {str(e)}")
            return {"is_medical_document": False, "is_blood_test": False, "error": str(e)}