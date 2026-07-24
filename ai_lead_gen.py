import json
import random
import time
from typing import List, Dict

# --- AI LEAD GENERATION TOOL ---
# Inspired by Jason Wardrop's 1-Person AI Business Strategy
# Optimized for Website + Hostinger Hosting Pitch

class AILeadGenTool:
    def __init__(self, location: str, niche: str):
        self.location = location
        self.niche = niche
        self.leads = []

    def scrape_leads(self, mock: bool = True):
        """
        Simulates scraping Google Maps for local businesses.
        In a real scenario, you would use Google Maps API or SerpApi.
        """
        print(f"[*] Searching for {self.niche} in {self.location}...")
        
        if mock:
            # Mock data for demonstration
            self.leads = [
                {
                    "name": "Quick Fix Plumbers",
                    "address": "123 Main St",
                    "rating": 4.2,
                    "reviews": 15,
                    "website": None,  # KEY LEAD: No website
                    "phone": "555-0101"
                },
                {
                    "name": "Green Lawn Experts",
                    "address": "456 Oak Ave",
                    "rating": 3.8,
                    "reviews": 8,
                    "website": "http://slow-unoptimized-site.com", # LEAD: Poor website
                    "phone": "555-0102"
                },
                {
                    "name": "Sunny Day Cafe",
                    "address": "789 Pine Rd",
                    "rating": 4.8,
                    "reviews": 120,
                    "website": "http://established-cafe.com",
                    "phone": "555-0103"
                }
            ]
        else:
            # Real implementation would go here
            # Example: response = requests.get(f"https://serpapi.com/search?engine=google_maps&q={self.niche}+{self.location}&api_key=YOUR_KEY")
            pass

    def analyze_leads(self) -> List[Dict]:
        """Categorizes leads and identifies high-value opportunities."""
        optimized_leads = []
        for lead in self.leads:
            # Case 1: No website at all (Highest conversion)
            if not lead["website"]:
                lead["category"] = "MISSING_WEBSITE"
                lead["pain_point"] = "Missing out on local search traffic and 24/7 online presence."
                optimized_leads.append(lead)
            
            # Case 2: Slow/Poor website (High conversion for migration)
            elif "slow" in lead["website"] or lead["rating"] < 4.0:
                lead["category"] = "POOR_WEBSITE"
                lead["pain_point"] = "Low performance/conversion rates are hurting your Google ranking."
                optimized_leads.append(lead)
                
        return optimized_leads

    def generate_pitch(self, lead: Dict) -> str:
        """Generates an AI-optimized personalized pitch."""
        name = lead["name"]
        rating = lead["rating"]
        reviews = lead["reviews"]
        
        # Personalized Opening based on Rating
        if rating > 4.0:
            hook = f"I noticed your impressive {rating}-star rating with {reviews} reviews on Google. Your customers clearly love what you do!"
        else:
            hook = f"I've been looking at your business on Google Maps and see you've already started building a reputation in {self.location}."

        # The Pitch logic for Website + Hostinger
        if lead["category"] == "MISSING_WEBSITE":
            offer = (
                f"However, I noticed you don't have a website link active. In 2026, 85% of customers check a site before calling. "
                "I can build you a high-converting, mobile-ready site in 48 hours."
            )
        else:
            offer = (
                f"I took a look at your current website, and I think we can significantly boost its speed and ranking. "
                "A slow site can lose up to 40% of visitors before they even see your offer."
            )

        # Optimization: Integrating Hostinger (Speed & Affordability)
        hosting_pitch = (
            "\n\nI specifically recommend moving to Hostinger's AI-optimized infrastructure. "
            "It's lightning-fast (essential for Google ranking), include a free domain, and costs significantly less than traditional hosting "
            "while providing 24/7 security. I can set this all up for you."
        )

        cta = "\n\nCan I send over a quick 2-minute video showing you exactly what we can build for you? No strings attached."

        return f"Hi {name} Team,\n\n{hook}\n\n{offer}{hosting_pitch}{cta}\n\nBest regards,\n[Your Name]"

    def run(self):
        self.scrape_leads()
        high_value_leads = self.analyze_leads()
        
        print(f"\n[+] Found {len(high_value_leads)} high-value leads for optimization.\n")
        
        for lead in high_value_leads:
            print("-" * 50)
            print(f"LEAD: {lead['name']} ({lead['category']})")
            print("PITCH:")
            print(self.generate_pitch(lead))
            print("-" * 50)

if __name__ == "__main__":
    # Example Usage
    tool = AILeadGenTool(location="Austin, TX", niche="Plumbers")
    tool.run()
