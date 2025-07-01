"""
Clean scoring script for Azure ML endpoint
Returns only prediction (-1, 0, 1) and confidence
"""

import json
import pandas as pd
import numpy as np

def init():
    """Initialize the model"""
    global model_info
    model_info = {
        "model_type": "Clean Football Prediction Model",
        "version": "1.0"
    }
    print(f"✅ {model_info['model_type']} v{model_info['version']} initialized")

def predict_match_outcomes(matches_data):
    """Clean football match prediction function"""
    results = []
    
    for match in matches_data:
        try:
            # Extract features with flexible column name handling
            home_fpi = float(match.get('hometeam_FPI', match.get('HomeFPI', 70)))
            away_fpi = float(match.get('awayteam_FPI', match.get('AwayFPI', 70)))
            fpi_diff = home_fpi - away_fpi
            
            home_odds = float(match.get('home_win_odds', match.get('HomeOdds', 2.5)))
            away_odds = float(match.get('away_win_odds', match.get('AwayOdds', 2.5)))
            draw_odds = float(match.get('draw_odds', 3.0))
            
            spectators = float(match.get('spectators', match.get('NumberSpectators', 35000)))
            if pd.isna(spectators) or spectators <= 0:
                spectators = 35000
            
            weather = str(match.get('weather', match.get('Weather', 'Clear')))
            
            # Calculate base probabilities from odds
            home_prob_odds = 1 / home_odds if home_odds > 0 else 0.4
            away_prob_odds = 1 / away_odds if away_odds > 0 else 0.4
            draw_prob_odds = 1 / draw_odds if draw_odds > 0 else 0.2
            
            # Normalize odds probabilities
            total_odds_prob = home_prob_odds + away_prob_odds + draw_prob_odds
            if total_odds_prob > 0:
                home_prob = home_prob_odds / total_odds_prob
                away_prob = away_prob_odds / total_odds_prob
                draw_prob = draw_prob_odds / total_odds_prob
            else:
                home_prob, away_prob, draw_prob = 0.4, 0.4, 0.2
            
            # FPI adjustments
            if abs(fpi_diff) > 15:
                fpi_adjustment = 0.2
            elif abs(fpi_diff) > 8:
                fpi_adjustment = 0.15
            elif abs(fpi_diff) > 3:
                fpi_adjustment = 0.1
            else:
                fpi_adjustment = 0.05
            
            if fpi_diff > 0:  # Home team stronger
                home_prob = min(0.85, home_prob + fpi_adjustment)
                away_prob = max(0.05, away_prob - fpi_adjustment * 0.7)
            else:  # Away team stronger
                away_prob = min(0.85, away_prob + fpi_adjustment)
                home_prob = max(0.05, home_prob - fpi_adjustment * 0.7)
            
            # Home advantage
            crowd_factor = min(1.3, 1 + (spectators - 30000) / 100000)
            home_advantage = 0.05 * crowd_factor
            home_prob = min(0.9, home_prob + home_advantage)
            
            # Weather effects
            weather_effects = {'Rain': 0.08, 'Snow': 0.12, 'Mist': 0.03, 'Cloudy': 0.01}
            if weather in weather_effects:
                draw_boost = weather_effects[weather]
                draw_prob = min(0.6, draw_prob + draw_boost)
            
            # Final normalization
            total_prob = home_prob + draw_prob + away_prob
            home_prob /= total_prob
            draw_prob /= total_prob
            away_prob /= total_prob
            
            # Determine prediction and confidence
            probs = {'home_win': home_prob, 'draw': draw_prob, 'away_win': away_prob}
            prediction_label = max(probs.items(), key=lambda x: x[1])[0]
            confidence = max(probs.values())
            
            # Convert to numeric format: home_win=1, draw=0, away_win=-1
            if prediction_label == 'home_win':
                prediction = 1
            elif prediction_label == 'draw':
                prediction = 0
            else:  # away_win
                prediction = -1
            
            results.append({
                'prediction': prediction,
                'confidence': round(confidence, 3)
            })
            
        except Exception as e:
            # Return neutral prediction on error
            results.append({
                'prediction': 0,
                'confidence': 0.333
            })
    
    return results

def run(raw_data: str) -> str:
    """Main scoring function - returns clean format"""
    try:
        # Parse input data
        input_data = json.loads(raw_data)
        
        if 'data' not in input_data:
            raise ValueError("Input must contain 'data' field")
        
        matches = input_data['data']
        if not isinstance(matches, list):
            raise ValueError("'data' field must be a list")
        
        print(f"🏈 Processing {len(matches)} match(es)...")
        
        # Generate predictions
        predictions = predict_match_outcomes(matches)
        
        # Return simple array format
        return json.dumps(predictions)
        
    except Exception as e:
        # Return default prediction on any error
        return json.dumps([{"prediction": 0, "confidence": 0.333}])

# Test function
if __name__ == "__main__":
    print("🧪 Testing clean scoring script...")
    
    init()
    
    test_data = {
        "data": [
            {
                "HomeFPI": 85.5,
                "AwayFPI": 78.2,
                "HomeOdds": 2.1,
                "AwayOdds": 3.2,
                "NumberSpectators": 50000,
                "Weather": "Clear"
            }
        ]
    }
    
    result = run(json.dumps(test_data))
    print("Clean result:")
    print(result)
