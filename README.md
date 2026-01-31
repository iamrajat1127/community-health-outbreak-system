# Community Health Outbreak System

A community-driven health management prototype:
- Detects regional disease spikes from conversational health chatter (verified + unverified)
- Visualizes outbreaks on an India map
- Shows explainability (symptoms, disease mentions, sample messages)
- Provides health literacy guidance for the dominant detected disease

## Repo structure
- `Health_Hackathon_AIModel/` -> Python pipeline (data cleaning, signal extraction, outbreak detection, JSON export)
- `health-hackathon-react-frontend/` -> React UI (Leaflet map + panels)

## How to run (Python pipeline)
1. Open terminal in `Health_Hackathon_AIModel`
2. Install dependencies:
   ```bash
   pip install pandas numpy matplotlib scikit-learn
