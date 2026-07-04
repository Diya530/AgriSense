"""
Pest & Disease Management Tool – AgriSense AI
───────────────────────────────────────────────
Placeholder for pest identification and IPM recommendation engine.

Future integration:
  - Image-based pest/disease detection (CNN model)
  - NCIPM (National Centre for Integrated Pest Management) database
  - Plantix / CropIn API integration
"""


def get_pest_management(crop: str, symptoms: str = None, pest_name: str = None) -> dict:
    """
    Provide Integrated Pest Management (IPM) recommendations.

    Args:
        crop (str): Crop affected (e.g., "Wheat", "Cotton")
        symptoms (str, optional): Description of symptoms observed
        pest_name (str, optional): Known pest or disease name

    Returns:
        dict: IPM recommendations with biological, chemical, and cultural controls.

    TODO: Replace stub with real pest identification model or API.
    """
    pest_database = {
        "wheat": {
            "common_pests": [
                {
                    "name": "Wheat Stem Rust",
                    "type": "Fungal Disease",
                    "symptoms": "Orange-brown pustules on stems and leaves",
                    "biological_control": "Use resistant varieties (HD-2967, GW-496)",
                    "chemical_control": "Propiconazole 25EC @ 0.1% spray",
                    "cultural_control": "Early sowing, avoid excess nitrogen",
                    "severity": "High",
                },
                {
                    "name": "Aphids",
                    "type": "Insect Pest",
                    "symptoms": "Yellow leaves, sticky honeydew, sooty mold",
                    "biological_control": "Conserve ladybird beetles; neem oil spray",
                    "chemical_control": "Imidacloprid 17.8 SL @ 0.05% spray",
                    "cultural_control": "Avoid late sowing; remove alternate hosts",
                    "severity": "Medium",
                },
            ]
        },
        "cotton": {
            "common_pests": [
                {
                    "name": "Pink Bollworm",
                    "type": "Insect Pest",
                    "symptoms": "Roseate flowers, damaged bolls with pink larvae inside",
                    "biological_control": "Pheromone traps @ 5/acre; Trichogramma releases",
                    "chemical_control": "Profenofos 50EC @ 2ml/liter or Spinosad 45SC",
                    "cultural_control": "Use Bt cotton; early harvest; destroy crop residue",
                    "severity": "High",
                },
            ]
        },
        "rice": {
            "common_pests": [
                {
                    "name": "Brown Plant Hopper (BPH)",
                    "type": "Insect Pest",
                    "symptoms": "Hopper burn — circular drying patches in field",
                    "biological_control": "Conserve spiders and natural enemies; light traps",
                    "chemical_control": "Buprofezin 25SC @ 1ml/liter; avoid pyrethroids",
                    "cultural_control": "Avoid excess nitrogen; use resistant varieties",
                    "severity": "High",
                },
                {
                    "name": "Blast Disease",
                    "type": "Fungal Disease",
                    "symptoms": "Spindle-shaped lesions with gray center on leaves",
                    "biological_control": "Trichoderma seed treatment",
                    "chemical_control": "Tricyclazole 75WP @ 0.6g/liter spray",
                    "cultural_control": "Avoid excess nitrogen; maintain proper spacing",
                    "severity": "Very High",
                },
            ]
        },
    }

    crop_data = pest_database.get(crop.lower(), {})
    pests = crop_data.get("common_pests", [
        {
            "name": "General Pest Advisory",
            "type": "General",
            "symptoms": f"Observed symptoms: {symptoms or 'Not specified'}",
            "biological_control": "Use neem-based products (Azadirachtin 0.03%)",
            "chemical_control": "Consult local KVK for specific pesticide recommendation",
            "cultural_control": "Crop rotation, field sanitation, resistant varieties",
            "severity": "Unknown",
        }
    ])

    return {
        "crop": crop,
        "pests_detected": len(pests),
        "pest_list": pests,
        "general_ipm_tips": [
            "Scout fields regularly (twice a week during crop period).",
            "Maintain Economic Threshold Level (ETL) before spraying.",
            "Always wear PPE (gloves, mask, goggles) while spraying.",
            "Do not spray during flowering to protect pollinators.",
            "Observe pre-harvest interval (PHI) of pesticides.",
        ],
        "emergency_contact": "Kisan Call Centre: 1800-180-1551 (Toll Free)",
        "source": "stub",
    }
