import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Load environment variables from .env file
load_dotenv()

# Check if necessary API keys are set
# It's a good practice to validate keys at the start.
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("OPENAI_API_KEY not found in .env file. Please add it.")
if "SERPER_API_KEY" not in os.environ:
    print("Warning: SERPER_API_KEY not found. Web search capabilities will be limited.")
    # You can decide to raise an error or continue with limited functionality.
    search_tool = None
else:
    search_tool = SerperDevTool()

# 1. Define the Agents
# This agent is responsible for researching the given topic.
researcher = Agent(
  role='Senior Research Analyst',
  goal='Uncover groundbreaking technologies and trends about {topic}',
  backstory="""You are a world-class research analyst. Your expertise lies in
  identifying emerging trends and gathering in-depth information. You are
  known for your meticulous work and ability to provide concise, relevant data.""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool] if search_tool else []
)

# Content Writer Agent - Takes researcher output and creates blog posts
content_writer = Agent(
  role='Senior Content Writer',
  goal='Transform research findings into compelling, SEO-optimized blog posts about {topic}',
  backstory="""You are an expert content writer with over 10 years of experience in 
  creating engaging blog posts and articles. You excel at taking complex research 
  data and transforming it into reader-friendly content that drives engagement. 
  You understand SEO best practices, content structure, and how to craft compelling 
  narratives that keep readers engaged from start to finish. Your writing style is 
  clear, authoritative, and accessible to both technical and non-technical audiences.""",
  verbose=True,
  allow_delegation=False
)

# 2. Define a function to create and run the crew
def create_content_crew(topic: str):
    """
    Creates and kicks off the CrewAI crew to generate a blog post.
    
    Args:
        topic (str): The topic for the blog post.

    Returns:
        str: The generated blog post content.
    """
    # Define Tasks for the agents
    task1 = Task(
      description=f"""Conduct a comprehensive analysis of the latest trends
      and key information about {topic}. Identify key players, innovations, and
      potential future developments. Your final answer must be a full analysis report.""",
      expected_output=f"A detailed report summarizing the key findings about {topic}.",
      agent=researcher
    )

    task2 = Task(
      description=f"""Using the research report from the researcher, write an engaging and SEO-optimized
      blog post about {topic}. The post should be easy to read, informative, and
      have a clear structure with a catchy title, introduction, main body, and a conclusion.
      It should be at least 500 words long and incorporate the research findings naturally.""",
      expected_output=f"A well-written blog post about {topic} in markdown format.",
      agent=content_writer
    )

    # 3. Instantiate the Crew
    crew = Crew(
      agents=[researcher, content_writer],
      tasks=[task1, task2],
      process=Process.sequential,  # Tasks will be executed one after the other
      verbose=True # Verbosity level for logging
    )

    # 4. Kick off the crew's work
    print(f"🚀 Kicking off the content creation crew for topic: {topic}")
    result = crew.kickoff()
    print("✅ Crew execution finished.")
    return result

# Example of how to run it directly (for testing)
if __name__ == '__main__':
    test_topic = "The Future of AI in Software Development"
    generated_content = create_content_crew(test_topic)
    print("\n\n--- Generated Blog Post ---")
    print(generated_content)