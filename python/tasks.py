from crewai import Task
from agents import medical_analyst, report_verifier, health_advisor
from tools import search_tool, BloodTestReportTool

# Task to verify and analyze blood test report
analyze_blood_report = Task(
    description="""
    Analyze the uploaded blood test report to address the user's query: {query}
    
    Steps to follow:
    1. Read and parse the blood test report from the file path: {file_path}
    2. Identify key blood markers and their values
    3. Compare values against normal reference ranges
    4. Identify any values that are outside normal ranges
    5. Provide a clear, structured analysis of the findings
    6. Address the specific user query if provided
    
    Focus on providing accurate, factual information based on the actual report data.
    """,
    
    expected_output="""
    A comprehensive blood test analysis report containing:
    
    1. **Report Summary**: Brief overview of the blood test type and date
    2. **Key Findings**: List of important blood markers and their values
    3. **Values Outside Normal Range**: Any abnormal results with explanations
    4. **General Observations**: Overall health indicators from the blood work
    5. **Recommendations**: Suggest consulting with healthcare provider for interpretation
    
    Format the response in clear, easy-to-understand language while maintaining medical accuracy.
    Include specific values and reference ranges where available.
    """,
    
    agent=medical_analyst,
    tools=[BloodTestReportTool.read_data_tool],
    async_execution=False,
)

# Task to verify document authenticity
verify_document = Task(
    description="""
    Verify that the uploaded document is a legitimate blood test report and extract basic information.
    
    Check for:
    1. Presence of medical laboratory information
    2. Patient information (anonymized for privacy)
    3. Test dates and reference ranges
    4. Laboratory values and units
    5. Overall document structure and format
    
    File path to analyze: {file_path}
    """,
    
    expected_output="""
    Document verification report including:
    - Document type confirmation
    - Presence of key medical report elements
    - Data quality assessment
    - Any issues or concerns with the document format
    """,
    
    agent=report_verifier,
    tools=[BloodTestReportTool.read_data_tool],
    async_execution=False,
)

# Task to provide health recommendations
provide_health_guidance = Task(
    description="""
    Based on the blood test analysis, provide general health and wellness recommendations.
    
    Consider the user's query: {query}
    
    Provide guidance on:
    1. General lifestyle factors that may influence blood test results
    2. Nutritional considerations (general, not specific medical advice)
    3. When to seek medical consultation
    4. Follow-up testing recommendations
    
    Always emphasize that this is general information and not a substitute for professional medical advice.
    """,
    
    expected_output="""
    Health guidance report containing:
    
    1. **General Recommendations**: Lifestyle and wellness suggestions
    2. **Nutritional Considerations**: General dietary guidance
    3. **Medical Consultation**: When and why to consult healthcare providers
    4. **Follow-up**: Suggested timeline for retesting if applicable
    5. **Important Disclaimer**: Clear statement about the limitations of this analysis
    
    All recommendations should be general in nature and emphasize the importance of professional medical consultation.
    """,
    
    agent=health_advisor,
    tools=[BloodTestReportTool.read_data_tool],
    async_execution=False,
)