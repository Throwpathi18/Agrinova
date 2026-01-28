class CropRecommender:
    def __init__(self):
        # Simple rule-based matrix
        # Soil: Sandy, Loamy, Clayey
        # Season: Summer, Winter, Monsoon
        self.recommendations = {
            ("Sandy", "Summer"): ["Watermelon", "Cucumber", "Peanuts"],
            ("Sandy", "Winter"): ["Potato", "Gram", "Mustard"],
            ("Loamy", "Summer"): ["Cotton", "Maize", "Pulses"],
            ("Loamy", "Winter"): ["Wheat", "Barley", "Peas"],
            ("Clayey", "Monsoon"): ["Rice", "Sugar Cane", "Jute"],
            ("Clayey", "Winter"): ["Linseed", "Gram"],
        }

    def suggest(self, soil_type, season):
        key = (soil_type, season)
        options = self.recommendations.get(key, ["Wheat", "Rice"]) # Defaults
        
        results = []
        for crop in options:
            results.append({
                "crop": crop,
                "reason": f"Matches {soil_type} soil for {season} season",
                "profit_potential": "High"
            })
        return results

crop_recommender = CropRecommender()
