// Static country data
const countryData = {
    "countries": [
        {
            "id": 1,
            "name": "Nigeria",
            "code": "NGA",
            "region": "West Africa",
            "scores": {
                "2023": {
                    "policy_score": 0.75,
                    "sectoral_score": 0.65,
                    "finance_score": 0.60,
                    "human_capital_score": 0.55,
                    "overall_score": 0.64,
                    "tier": "Emerging"
                }
            }
        },
        {
            "id": 2,
            "name": "Kenya",
            "code": "KEN",
            "region": "East Africa",
            "scores": {
                "2023": {
                    "policy_score": 0.85,
                    "sectoral_score": 0.75,
                    "finance_score": 0.70,
                    "human_capital_score": 0.65,
                    "overall_score": 0.74,
                    "tier": "Frontrunner"
                }
            }
        },
        {
            "id": 3,
            "name": "South Africa",
            "code": "ZAF",
            "region": "Southern Africa",
            "scores": {
                "2023": {
                    "policy_score": 0.90,
                    "sectoral_score": 0.80,
                    "finance_score": 0.85,
                    "human_capital_score": 0.75,
                    "overall_score": 0.83,
                    "tier": "Frontrunner"
                }
            }
        },
        {
            "id": 4,
            "name": "Ethiopia",
            "code": "ETH",
            "region": "East Africa",
            "scores": {
                "2023": {
                    "policy_score": 0.60,
                    "sectoral_score": 0.70,
                    "finance_score": 0.50,
                    "human_capital_score": 0.45,
                    "overall_score": 0.56,
                    "tier": "High Potential"
                }
            }
        },
        {
            "id": 5,
            "name": "Ghana",
            "code": "GHA",
            "region": "West Africa",
            "scores": {
                "2023": {
                    "policy_score": 0.70,
                    "sectoral_score": 0.60,
                    "finance_score": 0.55,
                    "human_capital_score": 0.50,
                    "overall_score": 0.59,
                    "tier": "Emerging"
                }
            }
        }
    ]
};

// Calculate averages
function calculateAverages() {
    const scores2023 = countryData.countries.map(country => country.scores["2023"]);
    
    const policyAvg = scores2023.reduce((sum, score) => sum + score.policy_score, 0) / scores2023.length;
    const sectoralAvg = scores2023.reduce((sum, score) => sum + score.sectoral_score, 0) / scores2023.length;
    const financeAvg = scores2023.reduce((sum, score) => sum + score.finance_score, 0) / scores2023.length;
    const humanCapitalAvg = scores2023.reduce((sum, score) => sum + score.human_capital_score, 0) / scores2023.length;
    const overallAvg = (policyAvg + sectoralAvg + financeAvg + humanCapitalAvg) / 4;
    
    return {
        policy: policyAvg,
        sectoral: sectoralAvg,
        finance: financeAvg,
        human_capital: humanCapitalAvg,
        overall_score: overallAvg
    };
}

// Get country by code
function getCountryByCode(code) {
    return countryData.countries.find(country => country.code === code);
}

// Get all countries sorted by overall score
function getCountriesSorted() {
    return [...countryData.countries].sort((a, b) => 
        b.scores["2023"].overall_score - a.scores["2023"].overall_score
    );
}