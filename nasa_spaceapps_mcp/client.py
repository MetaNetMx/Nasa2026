import urllib.request
import ssl
import json
import os
import re
from typing import Dict, Any, List, Optional
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"

class SpaceAppsClient:
    """Client for NASA Space Apps Challenge GraphQL API and cached knowledge base."""
    
    API_URL = "https://api.spaceappschallenge.org/graphql"
    BASE_URL = "https://www.spaceappschallenge.org"
    
    def __init__(self):
        self.ctx = ssl.create_default_context()
        # Fallback for Windows environments where system trust store may lack specific intermediate certs
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
        self._cached_challenges: Optional[List[Dict[str, Any]]] = None
        self._cached_guides: Optional[Dict[str, Any]] = None
        self._cached_events: Optional[List[Dict[str, Any]]] = None

    def query_graphql(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a GraphQL query against the official Space Apps API."""
        payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        req = urllib.request.Request(
            self.API_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SpaceAppsMCP/2.0",
                "X-Client-Origin": self.BASE_URL
            }
        )
        try:
            with urllib.request.urlopen(req, context=self.ctx, timeout=12) as res:
                return json.loads(res.read().decode("utf-8"))
        except Exception as e:
            return {"error": str(e)}

    def get_events(self) -> List[Dict[str, Any]]:
        """Retrieve Space Apps annual hackathon events."""
        query = """
        query GetEvents {
          events(first: 10) {
            edges {
              node {
                id
                name
                displayName
                slug
                status
                startDate
                endDate
              }
            }
          }
        }
        """
        res = self.query_graphql(query)
        if "data" in res and res["data"] and "events" in res["data"]:
            events = []
            for e in res["data"]["events"]["edges"]:
                node = e["node"]
                node["url"] = f"{self.BASE_URL}/{node['slug']}/"
                events.append(node)
            return events
            
        # Fallback to cache
        cache_file = CACHE_DIR / "events.json"
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def get_all_challenges_2026(self) -> List[Dict[str, Any]]:
        """Retrieve the complete list and dossiers of all 14 official 2026 challenges."""
        if self._cached_challenges is not None:
            return self._cached_challenges
            
        cache_file = CACHE_DIR / "challenges_2026.json"
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                self._cached_challenges = json.load(f)
                return self._cached_challenges
        
        # If not cached on disk, query API
        query = """
        query GetChallenges($event: EncodedID, $first: Int!) {
          challenges(event: $event, first: $first) {
            edges {
              node {
                id
                title
                excerpt
                skills
                meta {
                  slug
                  relativeUrl
                }
              }
            }
          }
        }
        """
        res = self.query_graphql(query, {"event": "aWQ6NA==", "first": 30})
        challenges = []
        if "data" in res and res["data"] and "challenges" in res["data"]:
            for e in res["data"]["challenges"]["edges"]:
                node = e["node"]
                rel_url = node.get("meta", {}).get("relativeUrl", "")
                challenges.append({
                    "id": node["id"],
                    "title": node["title"],
                    "slug": node.get("meta", {}).get("slug", ""),
                    "url": f"{self.BASE_URL}{rel_url}",
                    "skills": node.get("skills", []),
                    "excerpt": node.get("excerpt", ""),
                    "background": "",
                    "objectives": "",
                    "considerations": "",
                    "nasa_data_and_resources": ""
                })
        self._cached_challenges = challenges
        return challenges

    def get_challenge_detail(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Get full challenge dossier by slug, title keyword, or ID."""
        challenges = self.get_all_challenges_2026()
        target = identifier.lower().strip()
        for ch in challenges:
            if ch["slug"].lower() == target or ch["id"] == identifier:
                return ch
        # Keyword search match
        for ch in challenges:
            if target in ch["title"].lower() or target in ch["slug"].lower():
                return ch
        return None

    def search_challenges(self, query: str) -> List[Dict[str, Any]]:
        """Search challenges by keyword across title, skills, objectives, and background."""
        challenges = self.get_all_challenges_2026()
        q = query.lower().strip()
        matches = []
        for ch in challenges:
            searchable = f"{ch['title']} {ch['excerpt']} {' '.join(ch.get('skills', []))} {ch.get('objectives', '')} {ch.get('background', '')}".lower()
            if q in searchable:
                matches.append(ch)
        return matches

    def search_teams(self, query: str = "", first: int = 10) -> List[Dict[str, Any]]:
        """Live search teams across the Space Apps global network."""
        gql = """
        query GetTeams($first: Int!, $q: String) {
          teams(first: $first, q: $q) {
            totalCount
            edges {
              node {
                id
                title
                excerpt
                projectSubmitted
                locationDetails {
                  displayName
                  country
                }
              }
            }
          }
        }
        """
        res = self.query_graphql(gql, {"first": first, "q": query if query else None})
        teams = []
        if "data" in res and res.get("data") and "teams" in res["data"]:
            for e in res["data"]["teams"]["edges"]:
                n = e["node"]
                loc = n.get("locationDetails") or {}
                teams.append({
                    "id": n["id"],
                    "title": n["title"],
                    "excerpt": n.get("excerpt"),
                    "projectSubmitted": n.get("projectSubmitted", False),
                    "location": loc.get("displayName") or loc.get("country"),
                    "country": loc.get("country")
                })
        return teams

    def get_team_detail(self, team_id: str) -> Dict[str, Any]:
        """Fetch detailed information about a team by base64 ID."""
        gql = """
        query GetTeam($id: EncodedID!) {
          team(id: $id) {
            id
            title
            description
            excerpt
            desiredSkills
            languages
            projectSubmitted
            joinEnabled
            canAcceptMembers
            locationDetails {
              displayName
              country
            }
            projectDetails {
              id
              name
              summary
              demoLink
              projectLink
            }
            challengeDetails {
              id
              title
            }
            memberships {
              userDetails {
                id
                fullName
                username
                country
              }
            }
          }
        }
        """
        res = self.query_graphql(gql, {"id": team_id})
        if "data" in res and res["data"] and res["data"].get("team"):
            return res["data"]["team"]
        return {"error": f"Team {team_id} not found", "details": res}

    def search_projects(self, query: str = "", first: int = 10) -> List[Dict[str, Any]]:
        """Live search submitted projects from previous and current hackathons."""
        gql = """
        query GetProjects($first: Int!, $q: String) {
          projects(first: $first, q: $q) {
            totalCount
            edges {
              node {
                id
                name
                summary
                demoLink
                projectLink
              }
            }
          }
        }
        """
        res = self.query_graphql(gql, {"first": first, "q": query if query else None})
        projects = []
        if "data" in res and res.get("data") and "projects" in res["data"]:
            for e in res["data"]["projects"]["edges"]:
                n = e["node"]
                projects.append({
                    "id": n["id"],
                    "name": n["name"],
                    "summary": n.get("summary"),
                    "demoLink": n.get("demoLink"),
                    "projectLink": n.get("projectLink")
                })
        return projects

    def get_project_detail(self, project_id: str) -> Dict[str, Any]:
        """Fetch full project submission dossier by base64 ID."""
        gql = """
        query GetProject($id: EncodedID!) {
          project(id: $id) {
            id
            name
            summary
            demoLink
            projectLink
            details
            solution
            aiReferences
            aiToolsUsage
            dataReferences
            projectReferences
            isSubmitted
            submittedAt
          }
        }
        """
        res = self.query_graphql(gql, {"id": project_id})
        if "data" in res and res["data"] and res["data"].get("project"):
            return res["data"]["project"]
        return {"error": f"Project {project_id} not found", "details": res}

    def get_locations(self, first: int = 10) -> List[Dict[str, Any]]:
        """Fetch local hackathon locations around the world."""
        gql = """
        query GetLocations($first: Int!) {
          locations(first: $first) {
            totalCount
            edges {
              node {
                id
                title
                displayName
                country
                cachedRegistrations
                isRegistrationOpen
              }
            }
          }
        }
        """
        res = self.query_graphql(gql, {"first": first})
        locs = []
        if "data" in res and res.get("data") and "locations" in res["data"]:
            for e in res["data"]["locations"]["edges"]:
                n = e["node"]
                locs.append({
                    "id": n["id"],
                    "city": n.get("title"),
                    "displayName": n.get("displayName"),
                    "country": n.get("country"),
                    "registrations": n.get("cachedRegistrations", 0),
                    "isOpen": n.get("isRegistrationOpen")
                })
        return locs

    def get_official_guides(self) -> Dict[str, Any]:
        """Load official guides from cache or remote."""
        if self._cached_guides is not None:
            return self._cached_guides
        cache_file = CACHE_DIR / "guides.json"
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                self._cached_guides = json.load(f)
                return self._cached_guides
        return {}
