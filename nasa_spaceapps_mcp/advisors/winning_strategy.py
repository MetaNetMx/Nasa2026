from typing import Dict, Any, List
from .nasa_data_catalog import get_resources_for_challenge

JUDGING_CRITERIA: Dict[str, Dict[str, Any]] = {
    "Impact": {
        "weight": "20%",
        "score_scale": "1 (Minimal) to 5 (Outstanding)",
        "definition": "How much does this project solve a real-world problem on Earth or in space? Does it have broad reach, inspire others, or have potential to change the world?",
        "winning_tactics": [
            "Quantify your impact (e.g. 'Reduces communication dependency for Mars crew from 22 mins to 0 mins on edge')",
            "Clearly define the target user (e.g. Artemis astronauts, forest fire dispatchers, smallholder farmers)",
            "Demonstrate scalability from a hackathon proof-of-concept to real-world deployment."
        ]
    },
    "Creativity": {
        "weight": "20%",
        "score_scale": "1 (Conventional) to 5 (Groundbreaking)",
        "definition": "Originality and innovation of the proposed solution. Does it challenge conventional methods or present an inventive combination of ideas?",
        "winning_tactics": [
            "Introduce an unexpected synthesis (e.g. blending edge AI with NASA physiological models or sensor cross-calibration)",
            "Do not build a generic landing page; create an active interactive simulation, tool, or engine",
            "Highlight what is novel compared to existing commercial or academic tools."
        ]
    },
    "Validity": {
        "weight": "20%",
        "score_scale": "1 (Speculative) to 5 (Scientifically & Technically Feasible)",
        "definition": "Is the solution grounded in sound scientific principles and technically feasible? Is there a working demo, prototype, or code?",
        "winning_tactics": [
            "Ground every formula, calculation, and threshold in peer-reviewed NASA technical reports or standard measures",
            "Provide functional, working code (GitHub repo) with clear installation and verification instructions",
            "Include realistic constraints (radiation tolerance, bandwidth limits, sensor noise, ephemeris uncertainty)."
        ]
    },
    "Relevance": {
        "weight": "20%",
        "score_scale": "1 (Tangential) to 5 (Exemplary Alignment)",
        "definition": "Does the project directly answer the challenge prompt and make meaningful, rigorous use of NASA and space agency open data?",
        "winning_tactics": [
            "Explicitly name every NASA dataset, satellite mission, and API used (e.g., FIRMS MOD14/VIIRS, LOLA DEM, OSDR/LSDA)",
            "Explain exactly how the data was transformed, cleaned, harmonized, or visualized",
            "Answer all core questions posed in the challenge 'Objectives' section."
        ]
    },
    "Presentation": {
        "weight": "20%",
        "score_scale": "1 (Confusing) to 5 (Inspiring & Professional)",
        "definition": "Clarity of communication, storytelling, concise executive summary, high-quality demonstration, and visual polish.",
        "winning_tactics": [
            "Keep the 30-second elevator pitch punchy, problem-centric, and jargon-free",
            "Include a 2-minute video demo or interactive live web application link",
            "Structure the project page using clean headings: The Problem, Our Solution, NASA Data Integration, How It Works, and Future Horizons."
        ]
    }
}

GLOBAL_AWARDS = [
    {"name": "Best Use of Data", "focus": "The solution that best makes space data accessible, or leverages it to a unique application."},
    {"name": "Best Use of Technology", "focus": "The solution that exemplifies the most innovative and impactful use of technology."},
    {"name": "Galactic Impact", "focus": "The solution with the most potential to improve life on Earth or in the universe."},
    {"name": "Best Mission Concept", "focus": "The solution with the most plausible concept and design for space exploration."},
    {"name": "Most Inspirational", "focus": "The solution that captures our hearts and minds with boundless curiosity."},
    {"name": "Best Use of Storytelling", "focus": "The solution that best communicates a story about space or Earth science through art or narrative."},
    {"name": "Local Impact", "focus": "The solution with the greatest potential to solve a local community problem."},
    {"name": "Global Nominee", "focus": "Projects chosen by local leads to advance to global judging round (top ~1-2 per location)."}
]

def recommend_best_challenge(skills: List[str], domain_interest: str, team_size: int = 4) -> Dict[str, Any]:
    """Analyze team background and recommend the top 2026 challenge for maximum winning probability."""
    domain_norm = domain_interest.lower()
    skills_norm = [s.lower() for s in skills]
    
    recommendations = []
    
    if any(k in domain_norm for k in ["health", "astronaut", "medicine", "biology", "human", "ai"]) or any(k in " ".join(skills_norm) for k in ["health", "human", "software", "ai"]):
        recommendations.append({
            "challenge_slug": "health-monitoring-software",
            "title": "Create Health Monitoring Software for Astronauts on Space Missions",
            "target_award": "Best Mission Concept or Galactic Impact",
            "match_reason": "High relevance for long-duration Artemis and Mars transit missions; judges love autonomous edge-computing solutions that solve real astronaut survival challenges.",
            "winning_strategy": "Build an offline-capable visual dashboard that monitors vitals, evaluates Spaceflight-Associated Neuro-ocular Syndrome (SANS) and radiation dose, and provides autonomous clinical guidance during 22-minute communication blackouts."
        })
        
    if any(k in domain_norm for k in ["fire", "wildfire", "earth", "climate", "gis", "satellite", "data"]) or any(k in " ".join(skills_norm) for k in ["earth", "gis", "remote sensing", "data science"]):
        recommendations.append({
            "challenge_slug": "modis-and-viirs-hot-spots",
            "title": "Harmonization of MODIS and VIIRS Hot Spots",
            "target_award": "Best Use of Data or Best Use of Technology",
            "match_reason": "Directly tackles a critical multi-decade sensor gap in NASA FIRMS active fire tracking (MODIS 1km vs VIIRS 375m); tangible impact on disaster response.",
            "winning_strategy": "Implement a mathematical point spread function (PSF) normalizer with an interactive burning activity calendar that fire chiefs and climate scientists can immediately use."
        })
        
    if any(k in domain_norm for k in ["moon", "lunar", "artemis", "navigation", "landing", "orbit"]) or any(k in " ".join(skills_norm) for k in ["space", "moon", "physics", "3d"]):
        recommendations.append({
            "challenge_slug": "lunar-landing-site-navigator",
            "title": "Lunar Landing Site Navigator",
            "target_award": "Best Mission Concept or Best Use of Technology",
            "match_reason": "Directly supports the NASA Artemis campaign targeting the Lunar South Pole; strong visual appeal with 3D DEMs and LOLA datasets.",
            "winning_strategy": "Combine LOLA slope hazard analysis (<12 deg), permanent shadow volatile maps, and solar illumination ephemerides from JPL Horizons."
        })

    if not recommendations:
        # Default top high-impact challenge
        recommendations.append({
            "challenge_slug": "health-monitoring-software",
            "title": "Create Health Monitoring Software for Astronauts on Space Missions",
            "target_award": "Best Mission Concept",
            "match_reason": "Universal appeal, rich NASA Human Research Program open resources, and immense real-world value for the next decade of deep space exploration.",
            "winning_strategy": "Focus on autonomous health decision-making for astronauts with interactive body mapping and microgravity countermeasure protocols."
        })
        
    return {
        "status": "success",
        "recommended_challenges": recommendations,
        "team_composition_advice": f"For a team of {team_size}, assign 1 Lead Data/Scientific Researcher, 1 Backend/Algorithm Engineer, 1 Frontend/UI/UX Designer, and 1 Storyteller/Pitch Lead."
    }

def generate_solution_blueprint(challenge_slug: str, project_name: str, core_idea: str) -> Dict[str, Any]:
    """Generate an end-to-end technical and scientific blueprint tailored to NASA judging criteria."""
    nasa_res = get_resources_for_challenge(challenge_slug)
    
    return {
        "project_name": project_name,
        "challenge_slug": challenge_slug,
        "challenge_title": nasa_res.get("title", challenge_slug),
        "directorate": nasa_res.get("nasa_mission_directorate", "NASA Science Mission Directorate"),
        "core_idea": core_idea,
        "winning_edge": nasa_res.get("winning_project_angle"),
        "nasa_datasets_to_cite": [d["name"] for d in nasa_res.get("datasets", [])],
        "architecture_layers": {
            "data_ingestion": "Ingest and cache open datasets via REST/GraphQL (NASA OSDR, FIRMS, PDS, Horizons)",
            "processing_engine": "Statistical normalization, physiological hazard scoring, or geospatial spatial indexing",
            "ui_ux_interface": "Interactive visual dashboard with responsive charts, clickable anatomical/geospatial maps, and offline execution capability",
            "edge_autonomy": "Zero-dependency local execution enabling operation without ground-link connectivity"
        },
        "rubric_checklist": {
            "Impact": "Demonstrates measurable benefit for NASA astronauts, space mission planners, or Earth disaster managers.",
            "Creativity": "Synthesizes multi-sensor telemetry with automated clinical decision trees or sensor harmonization.",
            "Validity": "Built with actual NASA open data schemas, verified algorithms, and open-source runnable code.",
            "Relevance": "Answers all objectives outlined in the 2026 challenge statement.",
            "Presentation": "High-fidelity UI, clear README, 2-minute demonstration video outline, and pitch deck slides."
        }
    }

def format_submission_pitch(
    project_title: str,
    challenge_title: str,
    summary: str,
    nasa_data: List[str],
    tech_stack: List[str],
    demo_url: str = "",
    repo_url: str = ""
) -> Dict[str, Any]:
    """Generate an official submission markdown document conforming to NASA Space Apps Project Submission Guide."""
    md_pitch = f"""# {project_title} - NASA Space Apps Challenge 2026 Submission

**Challenge:** {challenge_title}  
**Live Demo:** {demo_url or '[Pending Deployment / Localhost]'}  
**Source Code Repository:** {repo_url or '[GitHub Repository Link]'}  

---

## 1. Project Summary & Elevator Pitch
{summary}

## 2. The Real-World Space Problem
In deep space missions and modern Earth observation, critical decisions must often be made with extreme latency, vast datasets, and sensor inconsistencies. Our solution bridges this gap by delivering an intelligent, scientifically validated system that operates autonomously at the point of need.

## 3. How We Addressed the Challenge
Our multidisciplinary approach combines:
1. **Direct NASA Data Integration:** Rigorous parsing and synthesis of official space agency repositories.
2. **Autonomous Analytics Engine:** Scientific calculations grounded in NASA technical standards.
3. **Intuitive Visual Interface:** A user-centric, responsive dashboard designed for rapid situational awareness.

## 4. NASA Open Data & Space Agency Resources Used
{chr(10).join(f"- **{d}**" for d in nasa_data)}

## 5. Technology Stack & Architecture
- **Core Engine:** {', '.join(tech_stack) if tech_stack else 'Python, FastAPI, Modern Web Standards'}
- **Data Protocols:** Model Context Protocol (MCP), GraphQL, REST APIs
- **Visualization:** Interactive Geospatial / Biometric Visual Dashboards

## 6. Demonstration & Future Roadmap
- **Current Prototype:** Working software demonstration featuring end-to-end data ingestion, calculation, and visual reporting.
- **Future Development:** Hardware telemetry integration, flight certification testing, and expansion to additional space agency missions.

---
*Developed for the NASA International Space Apps Challenge 2026.*
"""
    return {
        "title": project_title,
        "submission_markdown": md_pitch
    }
