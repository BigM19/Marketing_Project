import pytest
from crew import MarketingCrew
from content import ContentList

def test_head_of_marketing_config():
    crew = MarketingCrew()
    assert "head_of_marketing" in crew.agents_config
    head_of_marketing = crew.head_of_marketing()
    assert head_of_marketing.role.strip() == "Head of Marketing"
    assert head_of_marketing.allow_delegation is True
    assert head_of_marketing.max_rpm == 3
    
def test_market_research_task():
    crew = MarketingCrew()
    assert "market_research" in crew.tasks_config
    task = crew.market_research()
    assert task.agent == crew.head_of_marketing()
