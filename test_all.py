import unittest
import asyncio
from nasa_spaceapps_mcp.client import SpaceAppsClient
from nasa_spaceapps_mcp.server import (
    mcp_server,
    list_challenges,
    get_challenge_detail,
    search_challenges,
    recommend_challenge,
    get_challenge_nasa_resources,
    generate_project_solution_architecture,
    solve_astronaut_health_problem,
    harmonize_modis_viirs
)
from winning_solutions.astronaut_health_monitor.clinical_engine import AstronautHealthEngine
from winning_solutions.modis_viirs_harmonizer.harmonizer import ModisViirsHarmonizer

class TestNASASpaceAppsMCP(unittest.TestCase):

    def setUp(self):
        self.client = SpaceAppsClient()

    def test_client_challenges_cache(self):
        challenges = self.client.get_all_challenges_2026()
        self.assertEqual(len(challenges), 14, "Should have exactly 14 official 2026 challenges")
        
        # Check specific known challenge
        health_ch = self.client.get_challenge_detail("health-monitoring-software")
        self.assertIsNotNone(health_ch)
        self.assertIn("Astronaut", health_ch["title"])
        self.assertTrue(len(health_ch["objectives"]) > 100)

    def test_search_challenges(self):
        fire_matches = search_challenges("fire")
        self.assertTrue(len(fire_matches) >= 2, "Should match at least MODIS/VIIRS and Flame in Freefall")

    def test_recommend_challenge(self):
        rec = recommend_challenge(["human", "biology", "software"], "astronaut health")
        self.assertEqual(rec["status"], "success")
        self.assertEqual(rec["recommended_challenges"][0]["challenge_slug"], "health-monitoring-software")

    def test_nasa_data_catalog(self):
        res = get_challenge_nasa_resources("modis-and-viirs-hot-spots")
        self.assertIn("FIRMS", str(res))

    def test_solution_blueprint(self):
        bp = generate_project_solution_architecture(
            "health-monitoring-software",
            "ASTRONOVA",
            "Autonomous edge decision engine for astronaut clinical care"
        )
        self.assertEqual(bp["project_name"], "ASTRONOVA")
        self.assertIn("rubric_checklist", bp)

    def test_astronaut_clinical_engine(self):
        # Test normal
        nominal = AstronautHealthEngine.full_astronaut_assessment({
            "optic_disc_elevation_um": 120,
            "intraocular_pressure_mmhg": 16,
            "spe_alert": False
        })
        self.assertGreater(nominal["mission_readiness_score"], 70)

        # Test SPE solar storm alert
        storm = AstronautHealthEngine.full_astronaut_assessment({
            "spe_alert": True,
            "daily_ambient_rate_ugy_hr": 400
        })
        self.assertTrue(storm["evaluations"]["radiation"]["spe_active"])
        self.assertIn("Storm Shelter", str(storm["priority_action_plan"]))

    def test_modis_viirs_harmonizer(self):
        prob = ModisViirsHarmonizer.calculate_modis_detection_probability(5.0)
        self.assertAlmostEqual(prob, 0.5, places=2)
        
        h_res = harmonize_modis_viirs(100, 300, 6.0)
        self.assertIn("harmonization_results", h_res)
        self.assertLess(h_res["harmonization_results"]["sensor_invariant_fire_index"], 400)

    def test_mcp_server_registration(self):
        async def _check():
            tools = await mcp_server.list_tools()
            self.assertGreaterEqual(len(tools), 15)
            resources = await mcp_server.list_resources()
            self.assertGreaterEqual(len(resources), 3)
            prompts = await mcp_server.list_prompts()
            self.assertGreaterEqual(len(prompts), 2)
        asyncio.run(_check())

if __name__ == "__main__":
    unittest.main()
