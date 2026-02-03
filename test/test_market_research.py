from datetime import datetime
import pytest
from crew import MarketingCrew
import os
from crewai import Crew, Process

#Test Market Research Task Configuration
def test_market_research_task_config():
    crew = MarketingCrew()
    assert "market_research" in crew.tasks_config
    task = crew.market_research()
    assert task.agent == crew.head_of_marketing()

#Test Prepare Marketing Strategy Task Execution
def test_prepare_marketing_strategy_task():
    
    test_dir = "test_data/resources"
    os.makedirs(test_dir, exist_ok=True)
    test_path = os.path.join(test_dir, "test__market_research.md")

    # Clean up old test files if they exist
    if os.path.exists(test_path):
        os.remove(test_path)

    # Define inputs for the placeholders in tasks.yaml
    inputs = {
        "product_name": "Test Excel Tool",
        "market_research_path": test_path, # Test-specific path
        "product_description": "A tool for testing",
        "target_audience": "Testers",
        "budget": "100 USD",
        "current_date": datetime.now().strftime("%Y-%m-%d")
    }
    
    #Initialize Crew with test directory
    crew = MarketingCrew(drafts_dir=test_dir)
    
    mini_crew = Crew(
        agents=[crew.head_of_marketing()],
        tasks=[crew.market_research()],
        process=Process.sequential
    )
    
    mini_crew.kickoff(inputs=inputs)
    
    # Check if the file exists on the disk
    assert os.path.exists(test_path), f"The markdown report was not created at {test_path}."
    
    # Check if the file has actual content
    with open(test_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
        assert len(content) > 0, "The market research file was created but it is empty."
        # Verify the content contains key expected sections
        assert "Analysis" in content or "Competitor" in content