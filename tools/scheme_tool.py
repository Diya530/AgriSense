"""
Government Schemes Tool – AgriSense AI
────────────────────────────────────────
Placeholder for government agricultural schemes database.

Future integration:
  - MyScheme portal API (myscheme.gov.in)
  - State agriculture department portals
  - PM-KISAN beneficiary status API
  - Soil Health Card portal
"""


def get_government_schemes(category: str = None, state: str = None) -> dict:
    """
    Retrieve government agricultural schemes and subsidies.

    Args:
        category (str, optional): Filter by category
            ("insurance", "credit", "subsidy", "income_support", "market")
        state (str, optional): State-specific schemes

    Returns:
        dict: List of schemes with eligibility, benefits, and application links.

    TODO: Replace stub with real API or database query.
    """
    schemes = [
        {
            "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
            "category": "income_support",
            "ministry": "Ministry of Agriculture & Farmers Welfare",
            "benefit": "₹6,000/year in 3 equal installments of ₹2,000 directly to bank account",
            "eligibility": "All small and marginal farmers with cultivable land",
            "how_to_apply": "Visit pmkisan.gov.in or nearest Common Service Centre (CSC)",
            "documents": ["Aadhaar Card", "Land Records", "Bank Account Details"],
            "status": "Active",
            "icon": "💰",
            "color": "success",
        },
        {
            "name": "PM Fasal Bima Yojana (PMFBY)",
            "category": "insurance",
            "ministry": "Ministry of Agriculture & Farmers Welfare",
            "benefit": "Crop insurance coverage against natural calamities, pests & diseases",
            "eligibility": "All farmers growing notified crops in notified areas",
            "how_to_apply": "Through bank, insurance company agent, or pmfby.gov.in",
            "documents": ["Aadhaar", "Land Records", "Bank Passbook", "Sowing Certificate"],
            "status": "Active",
            "icon": "🛡️",
            "color": "primary",
        },
        {
            "name": "Kisan Credit Card (KCC)",
            "category": "credit",
            "ministry": "Ministry of Finance / NABARD",
            "benefit": "Short-term credit up to ₹3 lakh at 4% interest for crop loans",
            "eligibility": "All farmers, tenant farmers, sharecroppers and oral lessees",
            "how_to_apply": "Apply at any bank branch or via bank's mobile app",
            "documents": ["Aadhaar", "PAN Card", "Land Records", "Passport Photo"],
            "status": "Active",
            "icon": "💳",
            "color": "warning",
        },
        {
            "name": "Soil Health Card Scheme",
            "category": "subsidy",
            "ministry": "Ministry of Agriculture & Farmers Welfare",
            "benefit": "Free soil testing and nutrient recommendation card every 2 years",
            "eligibility": "All farmers in India",
            "how_to_apply": "Contact nearest KVK, agriculture dept., or soilhealth.dac.gov.in",
            "documents": ["Aadhaar Card", "Land Details"],
            "status": "Active",
            "icon": "🧪",
            "color": "info",
        },
        {
            "name": "e-NAM (National Agriculture Market)",
            "category": "market",
            "ministry": "Ministry of Agriculture & Farmers Welfare",
            "benefit": "Online trading platform for better price discovery across 1000+ mandis",
            "eligibility": "Farmers in states connected to e-NAM platform",
            "how_to_apply": "Register at enam.gov.in or through local mandi office",
            "documents": ["Aadhaar", "Bank Account", "Mandi License (for traders)"],
            "status": "Active",
            "icon": "📊",
            "color": "secondary",
        },
        {
            "name": "PM Krishi Sinchayee Yojana (PMKSY)",
            "category": "subsidy",
            "ministry": "Ministry of Jal Shakti / Agriculture",
            "benefit": "Subsidy on drip and sprinkler irrigation — up to 55% for small farmers",
            "eligibility": "All farmers; higher subsidy for SC/ST and small/marginal farmers",
            "how_to_apply": "Apply at District Agriculture Office or pmksy.gov.in",
            "documents": ["Aadhaar", "Land Records", "Bank Details", "Quotation from vendor"],
            "status": "Active",
            "icon": "💧",
            "color": "primary",
        },
        {
            "name": "National Food Security Mission (NFSM)",
            "category": "subsidy",
            "ministry": "Ministry of Agriculture & Farmers Welfare",
            "benefit": "Subsidized seeds, IPM inputs, farm machinery for rice, wheat, pulses, oilseeds",
            "eligibility": "Farmers in identified low-productivity districts",
            "how_to_apply": "Through State Agriculture Department / District office",
            "documents": ["Aadhaar", "Land Records"],
            "status": "Active",
            "icon": "🌾",
            "color": "success",
        },
        {
            "name": "NABARD Agriculture Infrastructure Fund",
            "category": "credit",
            "ministry": "NABARD / Ministry of Finance",
            "benefit": "Long-term debt financing for post-harvest infrastructure and logistics",
            "eligibility": "FPOs, PACS, Agri-entrepreneurs, SHGs, cooperative societies",
            "how_to_apply": "Apply through NABARD or scheduled commercial banks",
            "documents": ["Business Plan", "Land Documents", "Bank Statements"],
            "status": "Active",
            "icon": "🏗️",
            "color": "dark",
        },
    ]

    if category:
        filtered = [s for s in schemes if s["category"].lower() == category.lower()]
        result = filtered if filtered else schemes
    else:
        result = schemes

    return {
        "schemes": result,
        "total": len(result),
        "last_updated": "2024-01",
        "source": "stub",
        "disclaimer": "Verify scheme details on official government portals before applying.",
    }
