from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ChallengeSummary(BaseModel):
    id: str = Field(description="Base64 encoded ID of the challenge")
    title: str = Field(description="Title of the challenge")
    slug: str = Field(description="URL slug of the challenge")
    url: str = Field(description="Full URL on spaceappschallenge.org")
    skills: List[str] = Field(default_factory=list, description="Skill domains associated with the challenge")
    categories: List[str] = Field(default_factory=list, description="Categories (e.g. Beginner, Intermediate, Advanced)")
    excerpt: str = Field(description="Brief summary/excerpt of the challenge")

class NASADataResource(BaseModel):
    title: str = Field(description="Name of the NASA or space agency dataset/resource")
    description: str = Field(description="Summary of the dataset and how to use it")
    url: Optional[str] = Field(default=None, description="Direct URL to dataset or documentation")

class ChallengeDetail(ChallengeSummary):
    background: str = Field(description="Scientific & operational background from NASA")
    objectives: str = Field(description="Specific mission goals and challenge prompt")
    considerations: str = Field(description="Potential considerations, target audience, and suggested features")
    nasa_data_and_resources: str = Field(description="Curated NASA and space agency data sources")
    parsed_resources: List[NASADataResource] = Field(default_factory=list, description="Structured resource links")

class EventSummary(BaseModel):
    id: str
    name: str
    displayName: str
    slug: str
    status: int
    startDate: str
    endDate: str
    url: str

class TeamSummary(BaseModel):
    id: str
    title: str
    excerpt: Optional[str] = None
    projectSubmitted: bool = False
    location: Optional[str] = None
    country: Optional[str] = None

class ProjectSummary(BaseModel):
    id: str
    name: str
    summary: Optional[str] = None
    demoLink: Optional[str] = None
    projectLink: Optional[str] = None

class JudgingRubric(BaseModel):
    criteria: Dict[str, str] = Field(description="The 5 official scoring pillars (1 to 5 points each)")
    award_categories: List[Dict[str, str]] = Field(description="Official Global Award categories")
    evaluation_levels: List[str] = Field(description="Stages from Local judging to Executive Global Judging")
    winning_tips: List[str] = Field(description="Actionable advice for high score in all criteria")

class ProjectBlueprint(BaseModel):
    challenge_title: str
    challenge_slug: str
    project_name: str
    tagline: str
    real_world_problem: str
    nasa_data_integration: List[str]
    technical_architecture: Dict[str, Any]
    user_experience: str
    alignment_with_judging_rubric: Dict[str, str]
    hackathon_execution_roadmap: List[str]

class SubmissionPitch(BaseModel):
    project_title: str
    short_description: str
    detailed_description: str
    space_agency_data_used: List[str]
    technologies_used: List[str]
    demo_instructions: str
    future_development: str
