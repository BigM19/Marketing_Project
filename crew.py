from typing import List
from crewai import Agent, Crew, Task, LLM, Process
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import SerperDevTool, ScrapeWebsiteTool, DirectoryReadTool, FileWriterTool, FileReadTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv

_ = load_dotenv()

llm = LLM(model="gemini/gemini-2.0-flash-lite", temperature=0.1)

@CrewBase
class MarketingCrew():
    "The marketing crew is repsonsible for creating and executing marketing strategies"
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def head_of_marketing(self) -> Agent:
        return Agent(
            config=self.agents_config["head_of_marketing"],
            tools=[
                SerperDevTool(),
                ScrapeWebsiteTool(),
                DirectoryReadTool("resources/drafts"),
                FileWriterTool(),
                FileReadTool()
            ],
            reasoning=True,
            inject_date=True,
            llm=llm,
            allow_delegation=True,
            max_rpm=3
        )