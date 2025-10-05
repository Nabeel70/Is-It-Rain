"""
Machine Learning Predictor for Precipitation Forecasting

Uses sklearn RandomForestRegressor trained on historical NASA POWER data
to predict precipitation probability and intensity.

Target Accuracy: 70-75% for historical patterns
Model: Random Forest with 100 estimators
Features: latitude, longitude, day_of_year, month, season, historical_avg
"""

from __future__ import annotations

import os
from datetime import date, datetime
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from loguru import logger
from sklearn.ensemble import RandomForestRegressor

from app.models.forecast import Location


class MLPredictor:
    """Machine Learning predictor for precipitation forecasting."""
    
    MODEL_PATH = Path("data/ml_models/precipitation_model.joblib")
    SCALER_PATH = Path("data/ml_models/feature_scaler.joblib")
    
    def __init__(self, model_path: Path | None = None):
        """
        Initialize ML predictor.
        
        Args:
            model_path: Optional custom path to model file
        """
        self.model_path = model_path or self.MODEL_PATH
        self.scaler_path = self.SCALER_PATH
        self.model: RandomForestRegressor | None = None
        self.scaler: Any | None = None
        self.is_trained = False
        
        # Try to load existing model
        if self.model_path.exists():
            self.load_model()
    
    def load_model(self) -> bool:
        """
        Load trained model from disk.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            self.model = joblib.load(self.model_path)
            if self.scaler_path.exists():
                self.scaler = joblib.load(self.scaler_path)
            self.is_trained = True
            logger.info(f"✅ ML model loaded from {self.model_path}")
            return True
        except Exception as e:
            logger.warning(f"⚠️  Could not load ML model: {e}")
            self.is_trained = False
            return False
    
    def save_model(self) -> None:
        """Save trained model to disk."""
        if self.model is None:
            raise ValueError("No model to save. Train model first.")
        
        # Create directory if it doesn't exist
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save model and scaler
        joblib.dump(self.model, self.model_path)
        if self.scaler:
            joblib.dump(self.scaler, self.scaler_path)
        
        logger.info(f"💾 ML model saved to {self.model_path}")
    
    def extract_features(
        self, 
        location: Location, 
        target_date: date,
        historical_avg: float = 0.0
    ) -> np.ndarray:
        """
        Extract features for ML prediction.
        
        Features:
        - latitude: -90 to 90
        - longitude: -180 to 180
        - day_of_year: 1 to 366
        - month: 1 to 12
        - season: 0 (winter), 1 (spring), 2 (summer), 3 (fall)
        - historical_avg: average precipitation for this location/date
        - distance_from_equator: abs(latitude)
        - is_tropical: 1 if -23.5 < lat < 23.5, else 0
        
        Args:
            location: Location with lat/lon
            target_date: Date to predict for
            historical_avg: Historical average precipitation (mm)
        
        Returns:
            Feature array of shape (1, n_features)
        """
        # Basic features
        latitude = location.latitude
        longitude = location.longitude
        day_of_year = target_date.timetuple().tm_yday
        month = target_date.month
        
        # Derived features
        # Season: 0=winter, 1=spring, 2=summer, 3=fall (Northern Hemisphere)
        season = (month % 12) // 3
        
        # Distance from equator (proxy for temperature)
        distance_from_equator = abs(latitude)
        
        # Is tropical region? (±23.5° latitude)
        is_tropical = 1.0 if abs(latitude) < 23.5 else 0.0
        
        # Seasonal sine/cosine (captures cyclical nature)
        day_sin = np.sin(2 * np.pi * day_of_year / 365.25)
        day_cos = np.cos(2 * np.pi * day_of_year / 365.25)
        
        features = np.array([
            latitude,
            longitude,
            day_of_year,
            month,
            season,
            historical_avg,
            distance_from_equator,
            is_tropical,
            day_sin,
            day_cos
        ]).reshape(1, -1)
        
        return features
    
    def predict(
        self,
        location: Location,
        target_date: date,
        historical_avg: float = 0.0
    ) -> dict[str, Any]:
        """
        Predict precipitation using trained ML model.
        
        Args:
            location: Location to predict for
            target_date: Date to predict for
            historical_avg: Historical average for this location/date
        
        Returns:
            Dictionary with:
            - predicted_mm: Predicted precipitation (mm)
            - confidence: Model confidence (0-1)
            - feature_importance: Dictionary of feature contributions
        """
        if not self.is_trained or self.model is None:
            logger.warning("⚠️  ML model not trained. Using fallback.")
            return {
                "predicted_mm": historical_avg,
                "confidence": 0.3,
                "feature_importance": {},
                "model_available": False
            }
        
        try:
            # Extract features
            features = self.extract_features(location, target_date, historical_avg)
            
            # Scale features if scaler available
            if self.scaler:
                features = self.scaler.transform(features)
            
            # Predict
            prediction = self.model.predict(features)[0]
            prediction = max(0.0, prediction)  # No negative precipitation
            
            # Estimate confidence based on feature values and model uncertainty
            # Use standard deviation from ensemble trees
            if hasattr(self.model, 'estimators_'):
                tree_predictions = np.array([
                    tree.predict(features)[0] 
                    for tree in self.model.estimators_
                ])
                std_dev = np.std(tree_predictions)
                # Lower std dev = higher confidence
                confidence = max(0.3, min(0.95, 1.0 - (std_dev / (prediction + 1))))
            else:
                confidence = 0.7  # Default confidence
            
            # Feature importance (if available)
            feature_names = [
                'latitude', 'longitude', 'day_of_year', 'month', 'season',
                'historical_avg', 'distance_from_equator', 'is_tropical',
                'day_sin', 'day_cos'
            ]
            
            feature_importance = {}
            if hasattr(self.model, 'feature_importances_'):
                for name, importance in zip(feature_names, self.model.feature_importances_):
                    feature_importance[name] = float(importance)
            
            logger.debug(
                f"🤖 ML prediction: {prediction:.2f}mm "
                f"(confidence: {confidence:.2f}) for {location.name}"
            )
            
            return {
                "predicted_mm": float(prediction),
                "confidence": float(confidence),
                "feature_importance": feature_importance,
                "model_available": True
            }
            
        except Exception as e:
            logger.error(f"❌ ML prediction failed: {e}", exc_info=True)
            return {
                "predicted_mm": historical_avg,
                "confidence": 0.3,
                "feature_importance": {},
                "model_available": False
            }
    
    def get_model_info(self) -> dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Model metadata including version, features, performance metrics
        """
        if not self.is_trained or self.model is None:
            return {
                "model_available": False,
                "message": "No model loaded. Train a model first."
            }
        
        info = {
            "model_available": True,
            "model_type": "RandomForestRegressor",
            "model_path": str(self.model_path),
            "n_estimators": getattr(self.model, 'n_estimators', None),
            "max_depth": getattr(self.model, 'max_depth', None),
            "n_features": getattr(self.model, 'n_features_in_', None),
        }
        
        # Add file metadata
        if self.model_path.exists():
            stat = os.stat(self.model_path)
            info["model_size_mb"] = round(stat.st_size / (1024 * 1024), 2)
            info["last_modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
        
        return info


# Singleton instance
_ml_predictor: MLPredictor | None = None


def get_ml_predictor() -> MLPredictor:
    """Get or create ML predictor singleton."""
    global _ml_predictor
    if _ml_predictor is None:
        _ml_predictor = MLPredictor()
    return _ml_predictor
