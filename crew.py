from crewai import Agent, Crew, Task, LLM, Process
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import SerperDevTool, ScrapeWebsiteTool, DirectoryReadTool, FileWriterTool, FileReadTool
from dotenv import load_dotenv
from content import Content

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
        
    @agent
    def content_creator_social_media(self) -> Agent:
        return Agent(
            config=self.agents_config["content_creator_social_media"],
            tools=[
                SerperDevTool(),
                ScrapeWebsiteTool(),
                DirectoryReadTool("resources/drafts"),
                FileWriterTool(),
                FileReadTool()
            ],
            inject_date=True,
            llm=llm,
            allow_delegation=True,
            max_iterations=30,
            max_rpm=3
        )
        
    @agent
    def content_writer_blogs(self) -> Agent:
        return Agent(
            config=self.agents_config["content_writer_blogs"],
            tools=[
                SerperDevTool(),
                ScrapeWebsiteTool(),
                DirectoryReadTool("resources/drafts"),
                FileWriterTool(),
                FileReadTool()
            ],
            inject_date=True,
            llm=llm,
            allow_delegation=True,
            max_iterations=5,
            max_rpm=3
        )
        
    @agent
    def seo_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["seo_specialist"],
            tools=[
                SerperDevTool(),
                ScrapeWebsiteTool(),
                DirectoryReadTool("resources/drafts"),
                FileWriterTool(),
                FileReadTool()
            ],
            inject_date=True,
            llm=llm,
            allow_delegation=True,
            max_iterations=3,
            max_rpm=3
        )
        
    @task
    def market_research(self) -> Task:
        return Task(
            config=self.tasks_config["market_research"],
            agent=self.head_of_marketing()
        )
        
    @task
    def prepare_marketing_strategy(self) -> Task:
        return Task(
            config=self.tasks_config["prepare_marketing_strategy"],
            agent=self.head_of_marketing()
        )