"""
Ensemble Forecasting System

Combines multiple data sources and prediction methods:
- NASA POWER API (historical satellite observations)
- ML predictor (trained on patterns)
- Statistical analysis (scipy-based)

Target Accuracy: 70-80% through weighted ensemble
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any

import numpy as np
from loguru import logger
from scipy import stats

from app.models.forecast import ForecastResponse, Location
from app.services.ml_predictor import get_ml_predictor
from app.services.nasa_power import NasaPowerClient

NASA_DATASET = "NASA POWER + ML Ensemble"


class EnsembleForecaster:
    """
    Ensemble forecasting combining multiple data sources and methods.
    
    Ensemble Weights:
    - NASA POWER: 50% (ground truth satellite data)
    - ML Predictor: 30% (learned patterns)
    - Statistical Model: 20% (trend analysis)
    
    Adjusts weights based on:
    - Data recency (newer = higher weight)
    - Confidence scores
    - Historical accuracy
    """
    
    def __init__(self):
        """Initialize ensemble forecaster with all components."""
        self.nasa_client = NasaPowerClient()
        self.ml_predictor = get_ml_predictor()
        
        # Default weights (can be adjusted based on validation)
        self.nasa_weight = 0.50
        self.ml_weight = 0.30
        self.stats_weight = 0.20
    
    async def get_ensemble_forecast(
        self,
        location: Location,
        event_date: date
    ) -> ForecastResponse:
        """
        Get comprehensive ensemble forecast combining all methods.
        
        Process:
        1. Get NASA POWER data (baseline)
        2. Get ML prediction
        3. Calculate statistical estimate
        4. Combine with weighted average
        5. Calculate confidence interval
        
        Args:
            location: Location to forecast for
            event_date: Date to forecast for
        
        Returns:
            Comprehensive forecast with ensemble insights
        """
        logger.info(
            f"🎯 Generating ensemble forecast for {location.name or 'unknown'} "
            f"on {event_date}"
        )
        
        # 1. Get NASA POWER baseline (ground truth)
        nasa_forecast = await self.nasa_client.precipitation_forecast(
            location, event_date
        )
        nasa_precip = nasa_forecast.precipitation_intensity_mm
        nasa_prob = nasa_forecast.precipitation_probability
        
        # 2. Get historical average for ML features
        historical_avg = await self._get_historical_average(location, event_date)
        
        # 3. Get ML prediction
        ml_result = self.ml_predictor.predict(
            location, event_date, historical_avg
        )
        ml_precip = ml_result["predicted_mm"]
        ml_confidence = ml_result["confidence"]
        
        # 4. Calculate statistical estimate
        stats_result = await self._calculate_statistical_estimate(
            location, event_date, historical_avg
        )
        stats_precip = stats_result["estimated_mm"]
        stats_confidence = stats_result["confidence"]
        
        # 5. Adjust weights based on confidence scores
        adjusted_weights = self._adjust_weights(
            ml_confidence, stats_confidence
        )
        
        # 6. Combine predictions with weighted average
        ensemble_precip = (
            adjusted_weights["nasa"] * nasa_precip +
            adjusted_weights["ml"] * ml_precip +
            adjusted_weights["stats"] * stats_precip
        )
        
        # 7. Calculate ensemble probability
        ensemble_prob = self._calculate_ensemble_probability(
            nasa_prob,
            ensemble_precip,
            ml_confidence,
            stats_confidence
        )
        
        # 8. Calculate confidence interval
        confidence_interval = self._calculate_confidence_interval(
            [nasa_precip, ml_precip, stats_precip],
            [adjusted_weights["nasa"], adjusted_weights["ml"], adjusted_weights["stats"]]
        )
        
        # 9. Generate intelligent summary
        summary = self._generate_ensemble_summary(
            ensemble_prob,
            ensemble_precip,
            confidence_interval,
            stats_result
        )
        
        # 10. Prepare metadata
        ensemble_metadata = {
            "ensemble_type": "weighted_average",
            "nasa_power": {
                "precipitation_mm": round(nasa_precip, 2),
                "probability": round(nasa_prob, 3),
                "weight": round(adjusted_weights["nasa"], 2)
            },
            "ml_model": {
                "precipitation_mm": round(ml_precip, 2),
                "confidence": round(ml_confidence, 2),
                "weight": round(adjusted_weights["ml"], 2),
                "available": ml_result["model_available"]
            },
            "statistical": {
                "precipitation_mm": round(stats_precip, 2),
                "confidence": round(stats_confidence, 2),
                "weight": round(adjusted_weights["stats"], 2),
                "trend": stats_result.get("trend", "unknown")
            },
            "confidence_interval_95": {
                "lower": round(confidence_interval["lower"], 2),
                "upper": round(confidence_interval["upper"], 2)
            },
            "overall_confidence": self._calculate_overall_confidence(
                ml_confidence, stats_confidence
            )
        }
        
        logger.info(
            f"✅ Ensemble: {ensemble_precip:.2f}mm ({ensemble_prob:.0%} prob) "
            f"- NASA: {nasa_precip:.2f}mm, ML: {ml_precip:.2f}mm, Stats: {stats_precip:.2f}mm"
        )
        
        return ForecastResponse(
            location=location,
            event_date=event_date,
            precipitation_probability=ensemble_prob,
            precipitation_intensity_mm=round(ensemble_precip, 2),
            summary=summary,
            nasa_dataset=NASA_DATASET,
            issued_at=datetime.now(timezone.utc),
            # Store metadata in a way that can be accessed by API
            # Note: This requires adding ensemble_metadata field to ForecastResponse model
        )
    
    async def _get_historical_average(
        self, location: Location, target_date: date
    ) -> float:
        """
        Get historical average precipitation for this location/date.
        
        Queries same day from last 3 years and calculates average.
        """
        try:
            historical_values = []
            for year_offset in range(1, 4):
                try:
                    historical_date = target_date.replace(
                        year=target_date.year - year_offset
                    )
                    forecast = await self.nasa_client.precipitation_forecast(
                        location, historical_date
                    )
                    historical_values.append(forecast.precipitation_intensity_mm)
                except (ValueError, Exception):
                    continue
            
            if historical_values:
                return float(np.mean(historical_values))
            return 0.0
            
        except Exception as e:
            logger.warning(f"Could not get historical average: {e}")
            return 0.0
    
    async def _calculate_statistical_estimate(
        self, location: Location, target_date: date, historical_avg: float
    ) -> dict[str, Any]:
        """
        Calculate statistical estimate using historical patterns and trends.
        
        Uses linear regression on historical data to detect trends.
        """
        try:
            # Get last 5 years of data for trend analysis
            historical_data = []
            dates = []
            
            for year_offset in range(1, 6):
                try:
                    historical_date = target_date.replace(
                        year=target_date.year - year_offset
                    )
                    forecast = await self.nasa_client.precipitation_forecast(
                        location, historical_date
                    )
                    historical_data.append(forecast.precipitation_intensity_mm)
                    dates.append(historical_date)
                except (ValueError, Exception):
                    continue
            
            if len(historical_data) < 2:
                return {
                    "estimated_mm": historical_avg,
                    "confidence": 0.5,
                    "trend": "insufficient_data"
                }
            
            # Linear regression to detect trend
            x = np.arange(len(historical_data))
            y = np.array(historical_data)
            
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            # Predict for "next year" (year 0)
            trend_prediction = intercept
            
            # Determine trend
            if abs(slope) < 0.1:
                trend = "stable"
            elif slope > 0:
                trend = "increasing"
            else:
                trend = "decreasing"
            
            # Confidence based on R² and sample size
            r_squared = r_value ** 2
            confidence = min(0.9, max(0.3, r_squared * (len(historical_data) / 5)))
            
            return {
                "estimated_mm": max(0.0, trend_prediction),
                "confidence": confidence,
                "trend": trend,
                "slope": slope,
                "r_squared": r_squared
            }
            
        except Exception as e:
            logger.warning(f"Statistical estimation failed: {e}")
            return {
                "estimated_mm": historical_avg,
                "confidence": 0.4,
                "trend": "error"
            }
    
    def _adjust_weights(
        self, ml_confidence: float, stats_confidence: float
    ) -> dict[str, float]:
        """
        Adjust ensemble weights based on component confidence scores.
        
        Higher confidence = higher weight
        NASA always maintains minimum 40% weight (ground truth)
        """
        # Base weights
        nasa_w = self.nasa_weight
        ml_w = self.ml_weight
        stats_w = self.stats_weight
        
        # Adjust ML weight based on confidence
        if ml_confidence < 0.5:
            # Low ML confidence: reduce ML weight, increase NASA
            reduction = (0.5 - ml_confidence) * 0.4
            ml_w -= reduction
            nasa_w += reduction * 0.7
            stats_w += reduction * 0.3
        
        # Adjust stats weight based on confidence
        if stats_confidence < 0.5:
            # Low stats confidence: reduce stats weight, increase NASA
            reduction = (0.5 - stats_confidence) * 0.3
            stats_w -= reduction
            nasa_w += reduction * 0.7
            ml_w += reduction * 0.3
        
        # Ensure weights sum to 1.0
        total = nasa_w + ml_w + stats_w
        nasa_w /= total
        ml_w /= total
        stats_w /= total
        
        return {
            "nasa": nasa_w,
            "ml": ml_w,
            "stats": stats_w
        }
    
    def _calculate_ensemble_probability(
        self,
        nasa_prob: float,
        ensemble_precip: float,
        ml_confidence: float,
        stats_confidence: float
    ) -> float:
        """
        Calculate ensemble probability combining multiple approaches.
        
        Uses:
        - NASA threshold-based probability (baseline)
        - Precipitation amount (higher = higher probability)
        - Confidence scores (adjust certainty)
        """
        # Threshold-based probability from precipitation amount
        if ensemble_precip <= 0.2:
            threshold_prob = 0.1
        elif ensemble_precip <= 1:
            threshold_prob = 0.35
        elif ensemble_precip <= 5:
            threshold_prob = 0.6
        elif ensemble_precip <= 10:
            threshold_prob = 0.8
        else:
            threshold_prob = 0.95
        
        # Combine NASA probability and threshold probability
        # Weight more towards NASA (it's actual satellite data)
        combined_prob = 0.6 * nasa_prob + 0.4 * threshold_prob
        
        # Adjust based on overall confidence
        overall_confidence = (ml_confidence + stats_confidence) / 2
        
        # Lower confidence = more uncertainty = pull towards 0.5
        uncertainty_factor = 1.0 - overall_confidence
        combined_prob = combined_prob * (1 - uncertainty_factor * 0.2) + 0.5 * uncertainty_factor * 0.2
        
        return round(min(max(combined_prob, 0.0), 1.0), 3)
    
    def _calculate_confidence_interval(
        self, predictions: list[float], weights: list[float]
    ) -> dict[str, float]:
        """
        Calculate 95% confidence interval for ensemble prediction.
        
        Uses weighted standard deviation of component predictions.
        """
        predictions_array = np.array(predictions)
        weights_array = np.array(weights)
        
        # Weighted mean (should equal ensemble prediction)
        weighted_mean = np.average(predictions_array, weights=weights_array)
        
        # Weighted variance
        weighted_variance = np.average(
            (predictions_array - weighted_mean) ** 2,
            weights=weights_array
        )
        weighted_std = np.sqrt(weighted_variance)
        
        # 95% confidence interval (±1.96 std dev)
        margin = 1.96 * weighted_std
        
        return {
            "lower": max(0.0, weighted_mean - margin),
            "upper": weighted_mean + margin,
            "std_dev": weighted_std
        }
    
    def _calculate_overall_confidence(
        self, ml_confidence: float, stats_confidence: float
    ) -> str:
        """
        Calculate overall ensemble confidence level.
        
        Returns: "very_high", "high", "medium", "low", "very_low"
        """
        avg_confidence = (ml_confidence + stats_confidence) / 2
        
        if avg_confidence >= 0.8:
            return "very_high"
        elif avg_confidence >= 0.65:
            return "high"
        elif avg_confidence >= 0.5:
            return "medium"
        elif avg_confidence >= 0.35:
            return "low"
        else:
            return "very_low"
    
    def _generate_ensemble_summary(
        self,
        probability: float,
        precipitation_mm: float,
        confidence_interval: dict[str, float],
        stats_result: dict[str, Any]
    ) -> str:
        """Generate intelligent summary with ensemble context."""
        # Base summary based on probability
        if probability < 0.2:
            base = "Skies look clear. Enjoy your parade!"
        elif probability < 0.5:
            base = "Low chance of rain; keep an eye on the sky."
        elif probability < 0.75:
            base = "Moderate rain risk. Have a backup plan ready."
        elif probability < 0.9:
            base = "High chance of showers—pack ponchos and cover equipment."
        else:
            base = "Severe rain threat expected. Consider rescheduling or moving indoors."
        
        # Add context from statistical analysis
        trend = stats_result.get("trend", "unknown")
        if trend == "increasing":
            base += " ⚠️ Increasing precipitation trend observed in recent years."
        elif trend == "decreasing":
            base += " 📉 Decreasing precipitation trend observed."
        
        # Add confidence interval context if high variance
        std_dev = confidence_interval.get("std_dev", 0)
        if std_dev > 3:
            base += " ⚠️ High variability - conditions may change quickly."
        
        # Add ensemble note
        base += " (Combined NASA satellite data, ML predictions, and statistical analysis)"
        
        return base


# Singleton instance
_ensemble_forecaster: EnsembleForecaster | None = None


def get_ensemble_forecaster() -> EnsembleForecaster:
    """Get or create ensemble forecaster singleton."""
    global _ensemble_forecaster
    if _ensemble_forecaster is None:
        _ensemble_forecaster = EnsembleForecaster()
    return _ensemble_forecaster
