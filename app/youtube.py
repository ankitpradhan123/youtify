from agno.agent import Agent
from agno.tools.youtube import YouTubeTools
from agno.models.groq import Groq
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Optional

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

class ContentGenerator:

    youtube_url: Optional[str] = None

    def __init__(self, youtube_url: str) -> None:
        self.youtube_url = youtube_url

    def generate_docs_from_transcript(self) -> Optional[list[Document]]:
        youtube_tool = YouTubeTools()
        video_captions = youtube_tool.get_youtube_video_captions(url=self.youtube_url)
        if ("No captions found for video" or "Error getting captions for video") in video_captions:
            return None
        document = Document(video_captions)
        document = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0,
                                                  add_start_index=True).split_documents([document])
        return document

    def generate_blog_post(self, document: list[Document]) -> str:
        blog_prompt = """Correct
        all the grammatical errors and spelling errors in a the content provided by the user and shorten the content.
        Write the blog post based on the content provided.
        """
        blog_agent = Agent(
            model=Groq(id="llama-3.1-8b-instant", temperature=0.2),
            debug_mode=False,
            description=blog_prompt,
            instructions=["Output should be only the correct content",
                          "Don't include any extra information",
                          "The output should be in blog format",
                          "eliminate the sentences like 'In this video', 'as demonstrated in the video' and such similar sentences and use something meaningful",
                          "eliminate the sentences like 'Thanks for watching' and use something meaningful",
                          "eliminate the sentences like subscribe our channel from the blog post",
                          "eliminate the sentences like subscribe our channel from the blog post",
                          "use '#' before the Title of the blog",
                          "use '##' before sub-heading",
                          "use '###' before sub-sub heading if there are any",
                          "use '-' before list items",
                          'There should be only one title ']
        )
        blog_content = ""
        for doc in document:
            run_response = blog_agent.run(doc.page_content)
            if blog_content != "":
                blog_content = blog_content + "\n" + run_response.content
            else:
                blog_content = blog_content + run_response.content
        return blog_content

    def generate_linkedin_post(self, document: list[Document]) -> str:
        linkedin_prompt = """Read the summary provided by the user and convert it into the form of linkedin post within 3000 characters
        """
        linkedin_agent = Agent(
            model=Groq(id="gemma2-9b-it"),
            debug_mode=False,
            description=linkedin_prompt,
            instructions=["Add emojis",
                          "Output should only contain the proper linkedin post",
                          "Summary should not be more than 3000 characters",
                          "don't add '*' in any sentence",
                          "Add 'youtube link in the comment section' sentence at the end"])

        summary = self.get_summary(document)
        linkedin_post_content = linkedin_agent.run(summary).content
        return linkedin_post_content

    def get_summary(self,document: list[Document]) -> str:
        summary_prompt = """" Convert the content into a short summary and trim all the unnecessary words
        """
        summary_agent = Agent(
            model=Groq(id="gemma2-9b-it"),
            debug_mode=False,
            description=summary_prompt)

        summary = ""
        for doc in document:
            response = summary_agent.run(doc.page_content).content
            summary = summary + response

        return summary