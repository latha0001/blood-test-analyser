import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from tools import search_tool, BloodTestReportTool

# Loading LLM
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# Creating a Medical Analysis Agent
medical_analyst = Agent(
    role="Medical Report Analyst",
    goal="Analyze blood test reports and provide accurate, evidence-based medical insights for the query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a qualified medical professional with expertise in laboratory medicine and clinical pathology. "
        "You specialize in interpreting blood test results and identifying potential health concerns based on "
        "laboratory values. You provide accurate, evidence-based analysis while being careful not to provide "
        "direct medical advice that should come from a patient's personal physician. You always recommend "
        "consulting with healthcare providers for proper medical guidance."
    ),
    tools=[BloodTestReportTool.read_data_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)

# Creating a Report Verifier Agent
report_verifier = Agent(
    role="Medical Document Verifier",
    goal="Verify that uploaded documents are valid blood test reports and extract relevant medical information",
    verbose=True,
    memory=True,
    backstory=(
        "You are a medical records specialist with extensive experience in reviewing and validating "
        "laboratory reports. You can identify authentic blood test reports, extract key medical "
        "information, and flag any inconsistencies or missing data that might affect the analysis."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)

# Creating a Health Recommendations Agent
health_advisor = Agent(
    role="Health and Wellness Advisor",
    goal="Provide general health recommendations based on blood test analysis while emphasizing the need for professional medical consultation",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified health educator with knowledge of nutrition, lifestyle factors, and general wellness. "
        "You provide evidence-based general health recommendations while always emphasizing that specific "
        "medical advice should come from qualified healthcare providers. You focus on lifestyle modifications "
        "that may support overall health and wellness."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)