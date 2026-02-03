from crewai import Agent, Crew, Task, LLM, Process
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import SerperDevTool, DirectoryReadTool, FileWriterTool, FileReadTool
from dotenv import load_dotenv
from content import Content
from datetime import datetime

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
        
    @task 
    def create_content_calendar(self) -> Task:
        return Task(
            config=self.tasks_config["create_content_calendar"],
            agent=self.content_creator_social_media()
        )
        
    @task
    def prepare_post_drafts(self) -> Task:
        return Task(
            config=self.tasks_config["prepare_post_drafts"],
            agent=self.content_creator_social_media(),
            output_pydantic=Content
        )
        
    @task
    def prepare_scripts_for_reels(self) -> Task:
        return Task(
            config=self.tasks_config["prepare_scripts_for_reels"],
            agent=self.content_creator_social_media(),
            output_pydantic=Content
        )
        
    @task
    def content_research_for_blogs(self) -> Task:
        return Task(
            config=self.tasks_config["content_research_for_blogs"],
            agent=self.content_writer_blogs()
        )
        
    @task
    def draft_blogs(self) -> Task:
        return Task(
            config=self.tasks_config["draft_blogs"],
            agent=self.content_writer_blogs(),
            output_pydantic=Content
        )
        
    @task
    def seo_optimization(self) -> Task:
        return Task(
            config=self.tasks_config["seo_optimization"],
            agent=self.seo_specialist(),
            output_pydantic=Content
        )
        
    @crew
    def marketing_crew(self) -> Crew:
        """Creates the marketing crew with all agents and tasks."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=True, 
            planning_llm=llm,
            max_rpm=3
        )
        
if __name__ == "__main__":
    inputs = {
        "product_name": "AI Powered Excel Automation Tool",
        "target_audience": "Small and Medium Enterprises (SMEs)",
        "product_description": "A tool that automates repetitive tasks in Excel using AI, saving time and reducing errors.",
        "budget": "Rs. 50,000",
        "current_date": datetime.now().strftime("%Y-%m-%d"),
    }
    crew = MarketingCrew()
    crew.marketing_crew().kickoff(inputs=inputs)
    print("Marketing crew has been successfully created and run.")