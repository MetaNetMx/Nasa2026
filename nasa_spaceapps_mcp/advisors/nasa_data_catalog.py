from typing import Dict, Any, List

CHALLENGE_DATA_CATALOG: Dict[str, Dict[str, Any]] = {
    "health-monitoring-software": {
        "title": "Create Health Monitoring Software for Astronauts on Space Missions",
        "nasa_mission_directorate": "Space Operations & Human Exploration (HRP)",
        "datasets": [
            {
                "name": "NASA Open Science Data Repository (OSDR / LSDA)",
                "url": "https://osdr.nasa.gov/bio/repo/",
                "api_endpoint": "https://osdr.nasa.gov/osdr/data/osd/meta/",
                "description": "Comprehensive biological, physiological, and omics datasets from astronauts and model organisms flown on ISS, Space Shuttle, and simulated microgravity analogs."
            },
            {
                "name": "NASA Human Research Program (HRP) 5 Hazards Framework",
                "url": "https://www.nasa.gov/hrp/hazards/",
                "description": "Standardized NASA risk matrix covering Space Radiation, Isolation/Confinement, Distance from Earth, Gravity Fields (0G/1.6G/3.8G), and Hostile Closed Environments."
            },
            {
                "name": "NASA Life Sciences Portal & Spaceflight-Associated Neuro-ocular Syndrome (SANS) Data",
                "url": "https://lsda.jsc.nasa.gov/",
                "description": "Clinical guidelines, visual acuity shifts, optic disc edema measurements, and lumbar puncture intracranial pressure records from long-duration ISS crew."
            },
            {
                "name": "NASA Standard Measures Core Telemetry Reference",
                "url": "https://www.nasa.gov/hrp/elements/hhrp/",
                "description": "Standardized battery of in-flight measurements: heart rate variability, arterial stiffness, immune cytokine panels, bone resorption markers (NTX), and sleep actigraphy."
            }
        ],
        "winning_project_angle": "Autonomous Spacecraft Edge Medical System: An offline-first clinical decision support system combining biometric telemetry anomaly detection, SANS eye-scan diagnostic analysis, and automated daily exercise/fluid-loading countermeasures tailored for Mars transit communications blackouts."
    },
    "modis-and-viirs-hot-spots": {
        "title": "Harmonization of MODIS and VIIRS Hot Spots",
        "nasa_mission_directorate": "Earth Science (FIRMS / ESDIS)",
        "datasets": [
            {
                "name": "NASA FIRMS (Fire Information for Resource Management System)",
                "url": "https://firms.modaps.eosdis.nasa.gov/",
                "api_endpoint": "https://firms.modaps.eosdis.nasa.gov/api/area/",
                "description": "Near real-time and historical active fire detections from MODIS (Terra/Aqua, 1km) and VIIRS (Suomi NPP & NOAA-20/21, 375m)."
            },
            {
                "name": "NASA Earthdata CMR (Common Metadata Repository)",
                "url": "https://cmr.earthdata.nasa.gov/search/",
                "api_endpoint": "https://cmr.earthdata.nasa.gov/search/granules.json",
                "description": "Open search for MOD14/MYD14 (MODIS Thermal Anomalies) and VNP14IMG/VJ114IMG (VIIRS 375m Active Fire) granules."
            },
            {
                "name": "NASA GIBS (Global Imagery Browse Services)",
                "url": "https://wiki.earthdata.nasa.gov/display/GIBS",
                "api_endpoint": "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/",
                "description": "Standard WMS/WMTS tile services for visual validation of smoke plumes, burn scars, and corrected reflectance imagery."
            }
        ],
        "winning_project_angle": "Dual-Sensor Point Spread Function (PSF) Harmonizer & Interactive Fire Calendar: A mathematical normalization pipeline that scales VIIRS 375m detections into equivalent MODIS 1km probability distributions while retaining sub-kilometer detection sensitivity, presented on an interactive 25-year fire regime calendar."
    },
    "lunar-landing-site-navigator": {
        "title": "Lunar Landing Site Navigator",
        "nasa_mission_directorate": "Exploration Systems Development / Artemis",
        "datasets": [
            {
                "name": "LRO LOLA (Lunar Orbiter Laser Altimeter) Science Node",
                "url": "https://pds-geosciences.wustl.edu/missions/lro/lola.htm",
                "description": "High-resolution digital elevation models (DEM), slope maps, and surface roughness datasets for the Lunar South Pole (Shackleton, Malapert, de Gerlache)."
            },
            {
                "name": "ASU Quickmap LROC Interface",
                "url": "https://quickmap.lroc.asu.edu/",
                "description": "Interactive tile server with LROC Narrow Angle Camera (NAC) 0.5m/pixel imagery, permanent shadow overlays, and slope analysis."
            },
            {
                "name": "JPL Horizons Ephemeris API",
                "url": "https://ssd.jpl.nasa.gov/horizons/",
                "api_endpoint": "https://ssd.jpl.nasa.gov/api/horizons.api",
                "description": "High-precision solar illumination angles, Earth visibility lines-of-sight, and celestial ephemerides for any lunar surface coordinate."
            }
        ],
        "winning_project_angle": "Artemis Landing Corridor Multi-Criteria Optimization Engine: Real-time candidate site evaluator combining 3D LOLA terrain slope hazard avoidance (<12 deg), cumulative solar illumination percentage, and uninterrupted direct-to-Earth communication windows."
    },
    "dancing-with-the-sars": {
        "title": "Dancing with the SARs",
        "nasa_mission_directorate": "Earth Science (NISAR / ASF DAAC)",
        "datasets": [
            {
                "name": "Alaska Satellite Facility (ASF) DAAC / Vertex",
                "url": "https://asf.alaska.edu/",
                "api_endpoint": "https://api.daac.asf.alaska.edu/services/search/param",
                "description": "Synthetic Aperture Radar (SAR) imagery archive including Sentinel-1, ALOS PALSAR, UAVSAR, and upcoming NISAR dual-frequency L/S-band datasets."
            },
            {
                "name": "NASA-ISRO SAR (NISAR) Mission Portal",
                "url": "https://nisar.jpl.nasa.gov/",
                "description": "Radar interferometry for ecosystem structure, ice sheet dynamics, and surface deformation monitoring."
            }
        ],
        "winning_project_angle": "Interferometric Coherence Change Detector (InSAR): Cloud-penetrating radar workflow for automated flood extent mapping and post-earthquake ground deformation monitoring."
    },
    "adapting-farms-with-nasa-data": {
        "title": "Field Shift: Adapting Farms with NASA Data",
        "nasa_mission_directorate": "Earth Science Applied Sciences (NASA Harvest & Acres)",
        "datasets": [
            {
                "name": "NASA SMAP (Soil Moisture Active Passive)",
                "url": "https://smap.jpl.nasa.gov/",
                "description": "Global L3/L4 surface and root-zone soil moisture estimates for irrigation timing and drought forecasting."
            },
            {
                "name": "ECOSTRESS (ECOsystem Spaceborne Thermal Radiometer Experiment on Space Station)",
                "url": "https://ecostress.jpl.nasa.gov/",
                "description": "Plant water stress and Evaporative Stress Index (ESI) measured from the International Space Station at diurnal intervals."
            },
            {
                "name": "LP DAAC Landsat/MODIS NDVI/EVI Vegetation Indices",
                "url": "https://lpdaac.usgs.gov/",
                "description": "Calibrated historical and near-real-time crop vigor time series."
            }
        ],
        "winning_project_angle": "Micro-Climate Crop Resilience Advisor: Precision agriculture engine combining SMAP root-zone moisture and ECOSTRESS evapotranspiration to recommend optimal planting windows, crop rotation shifts, and water conservation strategies under changing climate patterns."
    },
    "flame-in-freefall": {
        "title": "Flame in Freefall: SI-Powered Fire Safety Insights from Microgravity Combustion Data",
        "nasa_mission_directorate": "Biological and Physical Sciences (PSI)",
        "datasets": [
            {
                "name": "NASA Physical Sciences Informatics (PSI) Database",
                "url": "https://psi.nasa.gov/",
                "description": "Open repository of microgravity flight experiment data including ACME, FLEX, BASS, and Soot on ISS."
            },
            {
                "name": "NASA Glenn Research Center Combustion Science",
                "url": "https://www.nasa.gov/centers/glenn/home/index.html",
                "description": "Experimental video footage, pyrometry measurements, flame extinction diameters, and burning rate curves in 0-G environments."
            }
        ],
        "winning_project_angle": "Microgravity Flammability & Extinction Boundary Predictor: AI-driven dashboard that ingests PSI flame video and thermocouple metrics to calculate limiting oxygen index (LOI) and spacecraft material fire propagation hazards."
    },
    "planet-x-and-spherex": {
        "title": "Planet X and SPHEREx",
        "nasa_mission_directorate": "Astrophysics (SPHEREx / JPL)",
        "datasets": [
            {
                "name": "NASA/IPAC Infrared Science Archive (IRSA)",
                "url": "https://irsa.ipac.caltech.edu/",
                "description": "Archive for WISE, NEOWISE, Spitzer, and future SPHEREx all-sky spectroscopic infrared surveys."
            },
            {
                "name": "NASA SPHEREx Mission Science Center",
                "url": "https://spherex.caltech.edu/",
                "description": "96-channel all-sky near-infrared spectral survey for cosmic origins, water ice distribution, and outer solar system body detection."
            }
        ],
        "winning_project_angle": "Trans-Neptunian Candidate Hunter: High-throughput spectral difference engine that searches multi-epoch infrared surveys for parallax shifts of distant solar system bodies."
    }
}

def get_resources_for_challenge(slug_or_id: str) -> Dict[str, Any]:
    """Retrieve curated NASA datasets and mission info for a specific challenge."""
    for key, data in CHALLENGE_DATA_CATALOG.items():
        if key in slug_or_id.lower() or slug_or_id.lower() in key:
            return data
    # Generic NASA Open Data portal fallback
    return {
        "title": slug_or_id,
        "nasa_mission_directorate": "NASA Science Mission Directorate (SMD)",
        "datasets": [
            {
                "name": "NASA Open Data Portal",
                "url": "https://data.nasa.gov/",
                "description": "Central catalog of thousands of NASA open datasets, APIs, and geospatial resources."
            },
            {
                "name": "NASA Earthdata",
                "url": "https://www.earthdata.nasa.gov/",
                "description": "Full access to Earth observation satellite products, DAACs, and open GIS tools."
            },
            {
                "name": "NASA Open APIs",
                "url": "https://api.nasa.gov/",
                "description": "APIs for astronomy pictures, rover imagery, space weather, planetary orbital data, and satellite tracking."
            }
        ],
        "winning_project_angle": "Leverage official NASA open data repositories with clear scientific validation and high-impact visual presentation."
    }
