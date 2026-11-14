from typing import Dict, Any, List
import math

class AstronautHealthEngine:
    """
    Autonomous Clinical Decision & Hazard Assessment Engine for Deep Space Missions.
    Implements NASA Human Research Program (HRP) 5 Spaceflight Hazards Framework.
    """

    @staticmethod
    def evaluate_sans_risk(
        visual_acuity_logmar: float,
        intraocular_pressure_mmhg: float,
        optic_disc_elevation_um: float,
        days_in_microgravity: int
    ) -> Dict[str, Any]:
        """
        Evaluate Spaceflight-Associated Neuro-ocular Syndrome (SANS).
        NASA astronauts on long missions experience cephalic fluid shift, increased ICP,
        choroidal folds, optic disc edema, and hyperopic refractive shift.
        """
        # Normal IOP: 10 - 21 mmHg
        # Optic disc elevation: >200 um indicates significant edema (Frisén Scale grade 1+)
        frisen_grade = 0
        if optic_disc_elevation_um > 500:
            frisen_grade = 4
        elif optic_disc_elevation_um > 350:
            frisen_grade = 3
        elif optic_disc_elevation_um > 220:
            frisen_grade = 2
        elif optic_disc_elevation_um > 120:
            frisen_grade = 1

        risk_score = min(100.0, (
            (intraocular_pressure_mmhg - 15) * 3.5 +
            (optic_disc_elevation_um / 6.0) +
            (visual_acuity_logmar * 40.0) +
            (days_in_microgravity * 0.15)
        ))
        risk_score = max(0.0, risk_score)

        severity = "Low"
        if risk_score > 70 or frisen_grade >= 3:
            severity = "Critical (Immediate Intervention Required)"
        elif risk_score > 40 or frisen_grade >= 1:
            severity = "Moderate (Heightened Monitoring)"

        countermeasures = [
            "Initiate daily Lower Body Negative Pressure (LBNP) at 25-30 mmHg for 2 hours to redistribute fluids caudal.",
            "Adjust cabin sleep posture with slight head-elevation harness.",
            "Verify cabin pCO2 is below 2.0 mmHg (elevated CO2 exacerbates cerebral venous congestion).",
            "Perform daily fundus photography and Optical Coherence Tomography (OCT) scan."
        ]

        return {
            "hazard": "Altered Gravity (Fluid Shift / SANS)",
            "risk_score_0_to_100": round(risk_score, 1),
            "severity": severity,
            "estimated_frisen_grade": frisen_grade,
            "clinical_interpretation": (
                f"Astronaut exhibits Frisén Grade {frisen_grade} optic disc elevation with IOP {intraocular_pressure_mmhg} mmHg. "
                "Cerebral venous congestion from microgravity fluid shift detected."
            ),
            "prescribed_countermeasures": countermeasures
        }

    @staticmethod
    def evaluate_radiation_exposure(
        cumulative_dose_mgy: float,
        daily_ambient_rate_ugy_hr: float,
        solar_particle_event_alert: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluate space radiation risk (Galactic Cosmic Rays + SPE).
        NASA career limits for astronauts: ~600 mSv (equivalent dose).
        Typical deep-space cruise: ~1.5 mGy/day.
        """
        daily_dose_mgy = (daily_ambient_rate_ugy_hr * 24.0) / 1000.0
        
        status = "Nominal GCR Baseline"
        spe_protocol = False
        
        if solar_particle_event_alert or daily_ambient_rate_ugy_hr > 200:
            status = "SOLAR PARTICLE EVENT (SPE) WARNING - High Flux"
            spe_protocol = True
            
        projected_30_day_dose = cumulative_dose_mgy + (daily_dose_mgy * 30)
        
        countermeasures = []
        if spe_protocol:
            countermeasures.append("IMMEDIATE: Move to Storm Shelter / Water-Wall shielded compartment.")
            countermeasures.append("Deploy polyethylene and water-jacket personal shields.")
            countermeasures.append("Administer prescribed oral antioxidant radioprotectant cocktail.")
        else:
            countermeasures.append("Maintain standard passive dosimetry logging.")
            countermeasures.append("Verify water tank shielding distribution around crew quarters.")

        return {
            "hazard": "Space Radiation",
            "cumulative_dose_mgy": round(cumulative_dose_mgy, 2),
            "daily_dose_mgy": round(daily_dose_mgy, 3),
            "projected_30_day_dose_mgy": round(projected_30_day_dose, 2),
            "spe_active": spe_protocol,
            "status": status,
            "prescribed_countermeasures": countermeasures
        }

    @staticmethod
    def evaluate_cardiovascular_deconditioning(
        resting_hr_bpm: float,
        orthostatic_systolic_drop_mmhg: float,
        hrv_rmssd_ms: float,
        daily_exercise_hours: float
    ) -> Dict[str, Any]:
        """
        Evaluate cardiovascular deconditioning & orthostatic intolerance risk.
        In microgravity, heart muscle mass decreases and baroreceptor sensitivity blunts.
        """
        deconditioning_index = 0.0
        if orthostatic_systolic_drop_mmhg > 20: # Orthostatic hypotension threshold
            deconditioning_index += 40
        if hrv_rmssd_ms < 25: # Low HRV indicates autonomic stress
            deconditioning_index += 30
        if daily_exercise_hours < 2.0:
            deconditioning_index += (2.0 - daily_exercise_hours) * 15

        deconditioning_index = min(100.0, max(0.0, deconditioning_index))

        countermeasures = [
            "Increase Advanced Resistive Exercise Device (ARED) squats and deadlifts to 45 mins/day.",
            "High-intensity interval cycle ergometer (CEVIS) protocol: 4x4 min at 85% VO2 max.",
            "Begin isotonic saline loading (1.0 L water with 8 g NaCl) 24 hours prior to G-transition/landing."
        ]

        return {
            "hazard": "Altered Gravity (Cardiovascular Deconditioning)",
            "deconditioning_index_0_to_100": round(deconditioning_index, 1),
            "orthostatic_risk": "High" if orthostatic_systolic_drop_mmhg > 20 else "Normal",
            "hrv_autonomic_status": "Fatigued" if hrv_rmssd_ms < 30 else "Recovered",
            "prescribed_countermeasures": countermeasures
        }

    @staticmethod
    def evaluate_behavioral_and_circadian_health(
        sleep_hours: float,
        sleep_efficiency_percent: float,
        cognitive_reaction_time_ms: float,
        cabin_pco2_mmhg: float
    ) -> Dict[str, Any]:
        """
        Evaluate behavioral health, sleep architecture, and environmental stressors.
        Confinement and elevated cabin CO2 lead to cognitive performance dips and headaches.
        """
        cognitive_baseline_ms = 240.0
        reaction_delay_percent = max(0.0, ((cognitive_reaction_time_ms - cognitive_baseline_ms) / cognitive_baseline_ms) * 100)
        
        fatigue_risk = "Low"
        if sleep_hours < 6.0 or sleep_efficiency_percent < 75 or reaction_delay_percent > 20:
            fatigue_risk = "Elevated Cognitive Fatigue"
        if sleep_hours < 5.0 or reaction_delay_percent > 35:
            fatigue_risk = "Critical Cognitive Impairment"

        co2_status = "Nominal"
        if cabin_pco2_mmhg > 3.0:
            co2_status = "Elevated pCO2 (NASA threshold: maintain <2.0 mmHg to prevent headache/edema)"

        countermeasures = [
            "Implement circadian blue-enriched 480nm LED lighting during shift start; dim red shift 2 hrs before sleep.",
            "Review Environmental Control and Life Support System (ECLSS) scrubber canisters to lower cabin pCO2.",
            "Schedule 30-minute restorative nap protocol before safety-critical extravehicular activity (EVA)."
        ]

        return {
            "hazard": "Isolation & Hostile Closed Environment",
            "fatigue_risk": fatigue_risk,
            "cognitive_reaction_delay_percent": round(reaction_delay_percent, 1),
            "cabin_pco2_status": co2_status,
            "prescribed_countermeasures": countermeasures
        }

    @classmethod
    def full_astronaut_assessment(cls, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive multi-hazard astronaut clinical telemetry assessment."""
        sans = cls.evaluate_sans_risk(
            telemetry.get("visual_acuity_logmar", 0.05),
            telemetry.get("intraocular_pressure_mmhg", 17.5),
            telemetry.get("optic_disc_elevation_um", 140.0),
            telemetry.get("days_in_microgravity", 120)
        )
        radiation = cls.evaluate_radiation_exposure(
            telemetry.get("cumulative_dose_mgy", 95.0),
            telemetry.get("daily_ambient_rate_ugy_hr", 65.0),
            telemetry.get("spe_alert", False)
        )
        cardio = cls.evaluate_cardiovascular_deconditioning(
            telemetry.get("resting_hr_bpm", 68.0),
            telemetry.get("orthostatic_drop_mmhg", 12.0),
            telemetry.get("hrv_rmssd_ms", 38.0),
            telemetry.get("daily_exercise_hours", 2.2)
        )
        behavioral = cls.evaluate_behavioral_and_circadian_health(
            telemetry.get("sleep_hours", 6.8),
            telemetry.get("sleep_efficiency_percent", 84.0),
            telemetry.get("cognitive_reaction_time_ms", 255.0),
            telemetry.get("cabin_pco2_mmhg", 1.8)
        )

        overall_readiness = 100.0 - (
            sans["risk_score_0_to_100"] * 0.3 +
            (30.0 if radiation["spe_active"] else 5.0) +
            cardio["deconditioning_index_0_to_100"] * 0.3 +
            (25.0 if "Critical" in behavioral["fatigue_risk"] else 8.0)
        )
        overall_readiness = max(10.0, min(100.0, overall_readiness))

        return {
            "mission_readiness_score": round(overall_readiness, 1),
            "status": "FLIGHT CERTIFIED - NOMINAL" if overall_readiness > 75 else "ATTENTION REQUIRED - ACTION PRESCRIBED",
            "evaluations": {
                "sans_vision": sans,
                "radiation": radiation,
                "cardiovascular": cardio,
                "behavioral_environmental": behavioral
            },
            "priority_action_plan": [
                *sans["prescribed_countermeasures"][:2],
                *radiation["prescribed_countermeasures"][:1],
                *cardio["prescribed_countermeasures"][:1]
            ]
        }
