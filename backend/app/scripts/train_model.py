"""
Model Training Script for Precipitation Prediction

Collects historical NASA POWER data and trains RandomForest model.

Usage:
    python -m app.scripts.train_model --years 3 --samples-per-location 50

This will:
1. Sample global locations (varied climates)
2. Collect historical data from NASA POWER
3. Train RandomForest model
4. Evaluate with cross-validation
5. Save model with joblib
"""

from __future__ import annotations

import argparse
import asyncio
from datetime import date, datetime, timedelta
from pathlib import Path
import random
from typing import Any

import numpy as np
from loguru import logger
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from app.models.forecast import Location
from app.services.ml_predictor import MLPredictor
from app.services.nasa_power import NasaPowerClient


# Sample locations covering diverse climates
SAMPLE_LOCATIONS = [
    # Tropical
    {"name": "Singapore", "lat": 1.3521, "lon": 103.8198},
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"name": "Manaus, Brazil", "lat": -3.1190, "lon": -60.0217},
    {"name": "Nairobi, Kenya", "lat": -1.2921, "lon": 36.8219},
    
    # Temperate
    {"name": "London", "lat": 51.5074, "lon": -0.1278},
    {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503},
    {"name": "Sydney", "lat": -33.8688, "lon": 151.2093},
    
    # Arid/Desert
    {"name": "Phoenix", "lat": 33.4484, "lon": -112.0740},
    {"name": "Cairo", "lat": 30.0444, "lon": 31.2357},
    {"name": "Dubai", "lat": 25.2048, "lon": 55.2708},
    
    # Monsoon
    {"name": "Bangkok", "lat": 13.7563, "lon": 100.5018},
    {"name": "Jakarta", "lat": -6.2088, "lon": 106.8456},
    {"name": "Dhaka", "lat": 23.8103, "lon": 90.4125},
    
    # Polar/Cold
    {"name": "Reykjavik", "lat": 64.1466, "lon": -21.9426},
    {"name": "Moscow", "lat": 55.7558, "lon": 37.6173},
    
    # Mediterranean
    {"name": "Rome", "lat": 41.9028, "lon": 12.4964},
    {"name": "Athens", "lat": 37.9838, "lon": 23.7275},
    
    # Rainforest
    {"name": "Amazon (Peru)", "lat": -3.4653, "lon": -62.2159},
    {"name": "Congo Basin", "lat": -0.2280, "lon": 22.9068},
]


class ModelTrainer:
    """Trains precipitation prediction model using historical NASA data."""
    
    def __init__(self, years: int = 3, samples_per_location: int = 50):
        """
        Initialize trainer.
        
        Args:
            years: Number of years of historical data to collect
            samples_per_location: Number of random dates per location
        """
        self.years = years
        self.samples_per_location = samples_per_location
        self.nasa_client = NasaPowerClient()
        self.ml_predictor = MLPredictor()
        
        self.X_train: np.ndarray | None = None
        self.X_test: np.ndarray | None = None
        self.y_train: np.ndarray | None = None
        self.y_test: np.ndarray | None = None
        self.scaler = StandardScaler()
    
    async def collect_training_data(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Collect training data from NASA POWER API.
        
        Returns:
            Tuple of (features, targets)
        """
        logger.info(f"🔄 Collecting training data ({self.years} years, {len(SAMPLE_LOCATIONS)} locations)")
        
        features_list = []
        targets_list = []
        
        # Calculate date range
        end_date = date.today() - timedelta(days=7)  # NASA has ~1 week lag
        start_date = end_date - timedelta(days=365 * self.years)
        
        total_samples = len(SAMPLE_LOCATIONS) * self.samples_per_location
        collected = 0
        
        for loc_info in SAMPLE_LOCATIONS:
            location = Location(
                latitude=loc_info["lat"],
                longitude=loc_info["lon"],
                name=loc_info["name"]
            )
            
            logger.info(f"📍 Collecting data for {loc_info['name']}")
            
            # Sample random dates within range
            for _ in range(self.samples_per_location):
                try:
                    # Random date within range
                    days_diff = (end_date - start_date).days
                    random_days = random.randint(0, days_diff)
                    sample_date = start_date + timedelta(days=random_days)
                    
                    # Get NASA data
                    forecast = await self.nasa_client.precipitation_forecast(
                        location, sample_date
                    )
                    
                    # Extract features (without historical_avg to avoid look-ahead bias)
                    features = self.ml_predictor.extract_features(
                        location, sample_date, historical_avg=0.0
                    )
                    
                    # Target is actual precipitation
                    target = forecast.precipitation_intensity_mm
                    
                    features_list.append(features[0])
                    targets_list.append(target)
                    
                    collected += 1
                    if collected % 100 == 0:
                        logger.info(f"✅ Collected {collected}/{total_samples} samples")
                    
                    # Small delay to avoid rate limiting
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    logger.warning(f"⚠️  Failed to collect sample: {e}")
                    continue
        
        X = np.array(features_list)
        y = np.array(targets_list)
        
        logger.info(f"✅ Collected {len(X)} training samples")
        logger.info(f"📊 Feature shape: {X.shape}, Target shape: {y.shape}")
        logger.info(f"📊 Precipitation range: {y.min():.2f} - {y.max():.2f}mm")
        logger.info(f"📊 Mean precipitation: {y.mean():.2f}mm (std: {y.std():.2f}mm)")
        
        return X, y
    
    def train_model(
        self,
        X: np.ndarray,
        y: np.ndarray,
        n_estimators: int = 100,
        max_depth: int = 15,
        min_samples_split: int = 5,
        min_samples_leaf: int = 2
    ) -> dict[str, Any]:
        """
        Train Random Forest model with hyperparameter tuning.
        
        Args:
            X: Feature matrix
            y: Target vector
            n_estimators: Number of trees
            max_depth: Maximum tree depth
            min_samples_split: Minimum samples to split node
            min_samples_leaf: Minimum samples in leaf node
        
        Returns:
            Training metrics
        """
        logger.info("🤖 Training Random Forest model...")
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        logger.info(f"📊 Training samples: {len(self.X_train)}")
        logger.info(f"📊 Test samples: {len(self.X_test)}")
        
        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        # Train model
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=42,
            n_jobs=-1,  # Use all CPU cores
            verbose=1
        )
        
        model.fit(self.X_train_scaled, self.y_train)
        
        # Cross-validation
        logger.info("🔄 Running cross-validation...")
        cv_scores = cross_val_score(
            model, self.X_train_scaled, self.y_train,
            cv=5, scoring='r2', n_jobs=-1
        )
        
        # Evaluate on test set
        y_pred = model.predict(self.X_test_scaled)
        
        mae = mean_absolute_error(self.y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))
        r2 = r2_score(self.y_test, y_pred)
        
        # Calculate accuracy (within ±2mm threshold)
        within_threshold = np.abs(y_pred - self.y_test) <= 2.0
        accuracy = within_threshold.sum() / len(self.y_test)
        
        metrics = {
            "mae": round(mae, 3),
            "rmse": round(rmse, 3),
            "r2_score": round(r2, 3),
            "cv_r2_mean": round(cv_scores.mean(), 3),
            "cv_r2_std": round(cv_scores.std(), 3),
            "accuracy_2mm": round(accuracy, 3),
            "n_samples_train": len(self.X_train),
            "n_samples_test": len(self.X_test),
            "n_estimators": n_estimators,
            "max_depth": max_depth
        }
        
        logger.info("✅ Model training complete!")
        logger.info(f"📊 MAE: {mae:.3f}mm")
        logger.info(f"📊 RMSE: {rmse:.3f}mm")
        logger.info(f"📊 R² Score: {r2:.3f}")
        logger.info(f"📊 CV R² (mean±std): {cv_scores.mean():.3f}±{cv_scores.std():.3f}")
        logger.info(f"📊 Accuracy (±2mm): {accuracy:.1%}")
        
        # Store model
        self.ml_predictor.model = model
        self.ml_predictor.scaler = self.scaler
        self.ml_predictor.is_trained = True
        
        return metrics
    
    def analyze_feature_importance(self) -> dict[str, float]:
        """
        Analyze and display feature importance.
        
        Returns:
            Dictionary of feature importances
        """
        if self.ml_predictor.model is None:
            raise ValueError("Model not trained yet")
        
        feature_names = [
            'latitude', 'longitude', 'day_of_year', 'month', 'season',
            'historical_avg', 'distance_from_equator', 'is_tropical',
            'day_sin', 'day_cos'
        ]
        
        importances = self.ml_predictor.model.feature_importances_
        
        # Sort by importance
        indices = np.argsort(importances)[::-1]
        
        logger.info("\n📊 Feature Importance Rankings:")
        importance_dict = {}
        for i, idx in enumerate(indices):
            importance_dict[feature_names[idx]] = float(importances[idx])
            logger.info(f"  {i+1}. {feature_names[idx]}: {importances[idx]:.4f}")
        
        return importance_dict
    
    def save_model(self, output_dir: Path | None = None) -> None:
        """Save trained model and metadata."""
        if self.ml_predictor.model is None:
            raise ValueError("Model not trained yet")
        
        # Save model
        self.ml_predictor.save_model()
        
        logger.info("💾 Model and scaler saved successfully")
    
    async def run_full_training(self) -> dict[str, Any]:
        """
        Run complete training pipeline.
        
        Returns:
            Training results and metrics
        """
        # Collect data
        X, y = await self.collect_training_data()
        
        if len(X) < 100:
            raise ValueError(f"Insufficient training data: {len(X)} samples")
        
        # Train model
        metrics = self.train_model(X, y)
        
        # Analyze features
        feature_importance = self.analyze_feature_importance()
        
        # Save model
        self.save_model()
        
        results = {
            "status": "success",
            "metrics": metrics,
            "feature_importance": feature_importance,
            "training_date": datetime.now().isoformat(),
            "training_samples": len(X)
        }
        
        return results


async def main():
    """Main training script."""
    parser = argparse.ArgumentParser(
        description="Train precipitation prediction model"
    )
    parser.add_argument(
        "--years",
        type=int,
        default=3,
        help="Number of years of historical data to collect (default: 3)"
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=50,
        help="Number of samples per location (default: 50)"
    )
    parser.add_argument(
        "--estimators",
        type=int,
        default=100,
        help="Number of trees in Random Forest (default: 100)"
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=15,
        help="Maximum tree depth (default: 15)"
    )
    
    args = parser.parse_args()
    
    logger.info("🚀 Starting model training pipeline")
    logger.info(f"⚙️  Configuration:")
    logger.info(f"   - Years of data: {args.years}")
    logger.info(f"   - Samples per location: {args.samples}")
    logger.info(f"   - Locations: {len(SAMPLE_LOCATIONS)}")
    logger.info(f"   - Total expected samples: {len(SAMPLE_LOCATIONS) * args.samples}")
    logger.info(f"   - Random Forest trees: {args.estimators}")
    logger.info(f"   - Max tree depth: {args.max_depth}")
    
    trainer = ModelTrainer(years=args.years, samples_per_location=args.samples)
    
    try:
        results = await trainer.run_full_training()
        
        logger.info("\n" + "="*60)
        logger.info("🎉 TRAINING COMPLETE!")
        logger.info("="*60)
        logger.info(f"✅ Model saved to: {trainer.ml_predictor.model_path}")
        logger.info(f"✅ R² Score: {results['metrics']['r2_score']:.3f}")
        logger.info(f"✅ Accuracy (±2mm): {results['metrics']['accuracy_2mm']:.1%}")
        logger.info(f"✅ MAE: {results['metrics']['mae']:.3f}mm")
        logger.info("="*60)
        
        logger.info("\n🎯 Expected Performance:")
        if results['metrics']['r2_score'] >= 0.7:
            logger.info("   Excellent! Model should provide 70-80% accuracy")
        elif results['metrics']['r2_score'] >= 0.5:
            logger.info("   Good! Model should provide 60-70% accuracy")
        else:
            logger.info("   Fair. Consider collecting more data or tuning hyperparameters")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Training failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
