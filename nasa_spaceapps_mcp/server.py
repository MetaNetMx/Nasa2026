import asyncio
import json
from typing import List, Dict, Any, Optional
from mcp.server.mcpserver import MCPServer
from .client import SpaceAppsClient
from .advisors.winning_strategy import (
    JUDGING_CRITERIA,
    GLOBAL_AWARDS,
    recommend_best_challenge,
    generate_solution_blueprint,
    format_submission_pitch
)
from .advisors.nasa_data_catalog import get_resources_for_challenge

# Initialize Space Apps client and MCP Server
client = SpaceAppsClient()
mcp_server = MCPServer(
    name="nasa-spaceapps-2026-mcp",
    title="NASA International Space Apps Challenge 2026 MCP Server",
    description="Official Model Context Protocol server for NASA Space Apps Challenge 2026. Provides challenge exploration, live GraphQL intelligence, NASA open dataset integration, and winning project strategy generation.",
    version="2.0.0"
)

# =====================================================================
# TOOLS: CHALLENGE INTELLIGENCE & EXPLORATION
# =====================================================================

@mcp_server.tool()
def list_challenges(skill: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all 14 official NASA International Space Apps Challenge 2026 challenges.
    Filterable by skill (e.g. 'Software', 'Human Exploration', 'Earth Science') or category.
    """
    challenges = client.get_all_challenges_2026()
    filtered = []
    for ch in challenges:
        if skill and not any(skill.lower() in s.lower() for s in ch.get("skills", [])):
            continue
        if category and not any(category.lower() in c.lower() for c in ch.get("categories", [])):
            continue
        filtered.append({
            "id": ch["id"],
            "title": ch["title"],
            "slug": ch["slug"],
            "skills": ch.get("skills", []),
            "categories": ch.get("categories", []),
            "excerpt": ch.get("excerpt", ""),
            "url": ch["url"]
        })
    return filtered

@mcp_server.tool()
def get_challenge_detail(identifier: str) -> Dict[str, Any]:
    """
    Get full in-depth dossier for any 2026 NASA Space Apps challenge by slug or title keyword.
    Returns Background, Objectives, Potential Considerations, and NASA Data & Resources.
    """
    ch = client.get_challenge_detail(identifier)
    if not ch:
        return {"error": f"Challenge '{identifier}' not found in 2026 catalog"}
    return ch

@mcp_server.tool()
def search_challenges(query: str) -> List[Dict[str, Any]]:
    """
    Search challenges by keyword across titles, scientific background, mission objectives, and skills.
    Examples: 'fire', 'astronaut', 'radar', 'moon', 'agriculture', 'SPHEREx'.
    """
    matches = client.search_challenges(query)
    return [{
        "title": m["title"],
        "slug": m["slug"],
        "skills": m.get("skills", []),
        "excerpt": m.get("excerpt", ""),
        "url": m["url"]
    } for m in matches]

@mcp_server.tool()
def get_challenge_nasa_resources(identifier: str) -> Dict[str, Any]:
    """
    Get curated NASA open data repositories, satellite missions, and APIs specifically
    mapped to a challenge (e.g. FIRMS, Earthdata, OSDR/LSDA, PDS, LOLA, Horizons).
    """
    ch = client.get_challenge_detail(identifier)
    slug = ch["slug"] if ch else identifier
    return get_resources_for_challenge(slug)

# =====================================================================
# TOOLS: HACKATHON WINNING STRATEGY & PROJECT BLUEPRINTING
# =====================================================================

@mcp_server.tool()
def recommend_challenge(skills: List[str], domain_interest: str, team_size: int = 4) -> Dict[str, Any]:
    """
    Hackathon strategy advisor: Analyzes team strengths and interests to recommend
    the highest-probability winning challenge with target award category and competitive edge.
    """
    return recommend_best_challenge(skills, domain_interest, team_size)

@mcp_server.tool()
def generate_project_solution_architecture(challenge_slug: str, project_name: str, core_idea: str) -> Dict[str, Any]:
    """
    Generate an end-to-end technical, scientific, and architectural blueprint for a hackathon
    project specifically designed to maximize scores across NASA's 5 official judging criteria.
    """
    return generate_solution_blueprint(challenge_slug, project_name, core_idea)

@mcp_server.tool()
def get_judging_rubric_and_criteria() -> Dict[str, Any]:
    """
    Retrieve official NASA Space Apps judging criteria (Impact, Creativity, Validity,
    Relevance, Presentation scored 1 to 5), Global Award categories, and winning tactics.
    """
    return {
        "scoring_pillars": JUDGING_CRITERIA,
        "global_award_categories": GLOBAL_AWARDS,
        "advice_from_global_judges": [
            "Clearly ground your solution in official NASA or space agency open data.",
            "Build an interactive visual prototype or runnable demonstration rather than static slides.",
            "Keep the elevator pitch concise (under 200 words) and laser-focused on the real problem solved."
        ]
    }

@mcp_server.tool()
def generate_submission_pitch(
    project_title: str,
    challenge_title: str,
    summary: str,
    nasa_data_used: List[str],
    tech_stack: List[str],
    demo_url: str = "",
    repo_url: str = ""
) -> Dict[str, Any]:
    """
    Generate an official submission markdown pitch conforming to the NASA Space Apps
    Project Submission Guide structure (Overview, Problem, Solution, Data Used, Tech Stack, Roadmap).
    """
    return format_submission_pitch(
        project_title,
        challenge_title,
        summary,
        nasa_data_used,
        tech_stack,
        demo_url,
        repo_url
    )

# =====================================================================
# TOOLS: LIVE COMMUNITY INTELLIGENCE (TEAMS, PROJECTS, EVENTS)
# =====================================================================

@mcp_server.tool()
def search_teams(query: str = "", limit: int = 10) -> List[Dict[str, Any]]:
    """
    Live query across 74,000+ teams registered for the NASA International Space Apps Challenge.
    Search by team name, location, or keyword.
    """
    return client.search_teams(query, first=limit)

@mcp_server.tool()
def get_team_detail(team_id: str) -> Dict[str, Any]:
    """
    Get full details for a specific team by base64 ID (roster, project status, looking-for skills, location).
    """
    return client.get_team_detail(team_id)

@mcp_server.tool()
def search_projects(query: str = "", limit: int = 10) -> List[Dict[str, Any]]:
    """
    Live query across 31,000+ projects submitted to NASA Space Apps hackathons.
    Useful for benchmarking winning concepts and exploring prior approaches.
    """
    return client.search_projects(query, first=limit)

@mcp_server.tool()
def get_project_detail(project_id: str) -> Dict[str, Any]:
    """
    Get detailed submission file for a project (summary, solution details, demo link, code repository, AI tools used).
    """
    return client.get_project_detail(project_id)

@mcp_server.tool()
def list_local_events(limit: int = 15) -> List[Dict[str, Any]]:
    """
    List local hackathon events, hosting cities, countries, and registration counts across 2,050+ locations.
    """
    return client.get_locations(first=limit)

@mcp_server.tool()
def get_official_guide(guide_name: str) -> Dict[str, Any]:
    """
    Retrieve official Space Apps participant guides:
    Options: 'project-submission-guide', 'judging-awards-guide', 'team-formation-guide', 'participant-faqs'.
    """
    guides = client.get_official_guides()
    norm = guide_name.lower().strip()
    for k, v in guides.items():
        if norm in k or k in norm:
            return {"guide": k, "title": v.get("title"), "url": v.get("url"), "content_preview": v.get("content", "")[:3500]}
    return {"error": f"Guide '{guide_name}' not found. Available: {list(guides.keys())}"}

# =====================================================================
# TOOLS: REAL-WORLD NASA PROBLEM SOLVERS
# =====================================================================

@mcp_server.tool()
def solve_astronaut_health_problem(
    visual_acuity_logmar: float = 0.05,
    intraocular_pressure_mmhg: float = 17.5,
    optic_disc_elevation_um: float = 140.0,
    cumulative_dose_mgy: float = 95.0,
    daily_radiation_ugy_hr: float = 65.0,
    solar_particle_event_alert: bool = False,
    daily_exercise_hours: float = 2.2,
    sleep_hours: float = 6.8,
    cabin_pco2_mmhg: float = 1.8
) -> Dict[str, Any]:
    """
    Execute real-time autonomous clinical decision support for Challenge #4
    ('Create Health Monitoring Software for Astronauts on Space Missions').
    Evaluates SANS (vision degradation), radiation dose, cardiovascular deconditioning, and prescribes countermeasures.
    """
    # Import the local clinical engine
    try:
        from ..winning_solutions.astronaut_health_monitor.clinical_engine import AstronautHealthEngine
    except (ImportError, ValueError):
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent / "winning_solutions" / "astronaut_health_monitor"))
        from clinical_engine import AstronautHealthEngine

    telemetry = {
        "visual_acuity_logmar": visual_acuity_logmar,
        "intraocular_pressure_mmhg": intraocular_pressure_mmhg,
        "optic_disc_elevation_um": optic_disc_elevation_um,
        "cumulative_dose_mgy": cumulative_dose_mgy,
        "daily_ambient_rate_ugy_hr": daily_radiation_ugy_hr,
        "spe_alert": solar_particle_event_alert,
        "daily_exercise_hours": daily_exercise_hours,
        "sleep_hours": sleep_hours,
        "cabin_pco2_mmhg": cabin_pco2_mmhg
    }
    return AstronautHealthEngine.full_astronaut_assessment(telemetry)

@mcp_server.tool()
def harmonize_modis_viirs(
    raw_modis_detections: int = 150,
    raw_viirs_detections: int = 480,
    mean_viirs_frp_mw: float = 8.5
) -> Dict[str, Any]:
    """
    Execute active fire sensor harmonization for Challenge #8 ('Harmonization of MODIS and VIIRS Hot Spots').
    Calculates detection probability curve matching and sensor-invariant fire intensity score.
    """
    try:
        from ..winning_solutions.modis_viirs_harmonizer.harmonizer import ModisViirsHarmonizer
    except (ImportError, ValueError):
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent / "winning_solutions" / "modis_viirs_harmonizer"))
        from harmonizer import ModisViirsHarmonizer

    prob = ModisViirsHarmonizer.calculate_modis_detection_probability(mean_viirs_frp_mw)
    harmonized_viirs_count = raw_viirs_detections * prob
    total_harmonized = raw_modis_detections + harmonized_viirs_count
    
    return {
        "input": {
            "raw_modis_1km_detections": raw_modis_detections,
            "raw_viirs_375m_detections": raw_viirs_detections,
            "mean_frp_mw": mean_viirs_frp_mw
        },
        "harmonization_results": {
            "modis_detection_probability_at_frp": prob,
            "harmonized_viirs_equivalent": round(harmonized_viirs_count, 1),
            "sensor_invariant_fire_index": round(total_harmonized, 1),
            "raw_sum_before_harmonization": raw_modis_detections + raw_viirs_detections,
            "overcount_bias_mitigated_percent": round((1.0 - (total_harmonized / (raw_modis_detections + raw_viirs_detections))) * 100, 1)
        },
        "scientific_rationale": "VIIRS 375m pixel sensitivity detects sub-kilometer small fires that fail MODIS 1km saturation threshold. Scaling VIIRS counts by empirical MODIS detection probability P(FRP) eliminates artificial decadal trend jumps in FIRMS fire calendars."
    }

# =====================================================================
# RESOURCES: STANDARDIZED MCP RESOURCES
# =====================================================================

@mcp_server.resource("spaceapps://2026/challenges")
def resource_all_challenges() -> str:
    """JSON catalog of all 14 official 2026 NASA Space Apps challenges."""
    return json.dumps(client.get_all_challenges_2026(), indent=2)

@mcp_server.resource("spaceapps://2026/challenges/{slug}")
def resource_challenge_dossier(slug: str) -> str:
    """In-depth dossier for a specific 2026 challenge."""
    ch = client.get_challenge_detail(slug)
    return json.dumps(ch or {"error": f"Challenge '{slug}' not found"}, indent=2)

@mcp_server.resource("spaceapps://2026/judging-rubric")
def resource_judging_rubric() -> str:
    """Official NASA Space Apps evaluation rubric and global award categories."""
    return json.dumps({
        "criteria": JUDGING_CRITERIA,
        "global_awards": GLOBAL_AWARDS
    }, indent=2)

@mcp_server.resource("spaceapps://2026/events")
def resource_events() -> str:
    """Annual NASA Space Apps Challenge events."""
    return json.dumps(client.get_events(), indent=2)

# =====================================================================
# PROMPTS: GUIDED AGENT WORKFLOWS
# =====================================================================

@mcp_server.prompt("brainstorm_winning_solution")
def prompt_brainstorm_solution(challenge_slug: str, team_background: str) -> str:
    """Interactive prompt for brainstorming a high-scoring project concept."""
    return f"""You are an elite NASA researcher and Space Apps Challenge mentor.
The team has the following background: {team_background}
They want to compete in challenge: {challenge_slug}

Please provide:
1. An executive-level problem definition highlighting a real gap in current space or Earth operations.
2. A unique solution concept that combines at least two official NASA datasets/APIs.
3. An edge-computing or interactive software architecture.
4. Alignment strategies for the 5 judging criteria: Impact, Creativity, Validity, Relevance, Presentation.
5. Specific NASA open datasets to cite."""

@mcp_server.prompt("review_submission_draft")
def prompt_review_submission(draft_markdown: str) -> str:
    """Evaluator prompt to score a project draft against NASA's 5 official scoring pillars."""
    return f"""You are an official NASA Space Apps Challenge judge.
Review the following project submission draft:

{draft_markdown}

Evaluate and provide a score from 1 to 5 for each criterion:
- Impact (1-5)
- Creativity (1-5)
- Validity (1-5)
- Relevance to Challenge & NASA Data (1-5)
- Presentation & Storytelling (1-5)

Provide 3 concrete, high-leverage recommendations to increase the score before submission."""
