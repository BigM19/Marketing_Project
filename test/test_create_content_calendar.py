from datetime import datetime
import os
import pytest
from crew import MarketingCrew
from pathlib import Path
from crewai import Crew, Process

#Test Market Research Task Configuration
def test_create_content_calendar_task_config():
    crew = MarketingCrew()
    assert "create_content_calendar" in crew.tasks_config
    task = crew.create_content_calendar()
    assert task.agent == crew.content_creator_social_media()
    
#Test Prepare Marketing Strategy Task Execution
def test_create_content_calendar_task():
    
    test_dir = Path("test_data/resources")
    test_dir.mkdir(parents=True, exist_ok=True)
    test_path = (test_dir / "test_content_calendar.md")
    test_marketing_strategy_path = (test_dir / "test_marketing_strategy.md")

    # Clean up old test files if they exist
    if test_path.exists():
        test_path.unlink()
        
    assert test_marketing_strategy_path.exists(), "Cannot create content calendart without marketing strategy file."

    # Define inputs for the placeholders in tasks.yaml
    inputs = {
        "product_name": "Test Excel Tool",
        "marketing_strategy_path": test_marketing_strategy_path.as_posix(),
        "content_calendar_path": test_path.as_posix(),
        "product_description": "A tool for testing",
        "target_audience": "Testers",
        "current_date": datetime.now().strftime("%Y-%m-%d")
    }
    
    #Initialize Crew with test directory
    crew = MarketingCrew(drafts_dir=test_dir)
    
    mini_crew = Crew(
        agents=[crew.content_creator_social_media()],
        tasks=[crew.create_content_calendar()],
        process=Process.sequential,
        verbose=True
    )
    
    mini_crew.kickoff(inputs=inputs)
    
    # Check if the file exists on the disk
    assert test_path.exists(), f"The markdown report was not created at {test_path}."
    
    # Check if the file has actual content
    with open(test_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
        assert len(content) > 0, "The content calendar file was created but it is empty."
        # Verify the content contains key expected sections
        assert "Content Calendar" in content, "The content calendar does not contain the expected header."