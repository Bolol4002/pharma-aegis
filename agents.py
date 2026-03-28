"""Pharma Aegis Analysis Agents - Real-time sensor analysis"""
from models import SensorReading, AnalysisResult, RiskResult, DecisionResult
from tools import get_latest_sensor_data


def data_analyzer(reading: SensorReading) -> AnalysisResult:
    """Analyze raw sensor data and determine status"""
    
    # Temperature analysis (Pharma storage: 15-25°C optimal)
    if reading.temperature < 15:
        temperature_status = "too_cold"
        temperature_score = 2
    elif reading.temperature < 18:
        temperature_status = "cool"
        temperature_score = 1
    elif reading.temperature <= 25:
        temperature_status = "optimal"
        temperature_score = 0
    elif reading.temperature <= 28:
        temperature_status = "warm"
        temperature_score = 1
    else:
        temperature_status = "too_hot"
        temperature_score = 2

    # Humidity analysis (Pharma storage: 30-60% optimal)
    if reading.humidity < 30:
        humidity_status = "too_dry"
        humidity_score = 1
    elif reading.humidity <= 60:
        humidity_status = "optimal"
        humidity_score = 0
    elif reading.humidity <= 75:
        humidity_status = "humid"
        humidity_score = 1
    else:
        humidity_status = "too_humid"
        humidity_score = 2

    # Vibration analysis
    if reading.vibration < 1.0:
        vibration_status = "normal"
        vibration_score = 0
    elif reading.vibration < 1.5:
        vibration_status = "elevated"
        vibration_score = 1
    else:
        vibration_status = "high"
        vibration_score = 2

    # Fire detection (highest priority)
    fire_status = "detected" if reading.fire == 1 else "safe"
    fire_score = 5 if reading.fire == 1 else 0

    return AnalysisResult(
        temperature_status=temperature_status,
        humidity_status=humidity_status,
        vibration_status=vibration_status,
        fire_status=fire_status,
        anomaly_score=temperature_score + humidity_score + vibration_score + fire_score,
    )


def risk_evaluator(analysis: AnalysisResult) -> RiskResult:
    """Evaluate risk based on analysis"""
    
    if analysis.fire_status == "detected":
        return RiskResult(
            risk_level="CRITICAL",
            reason="🚨 Fire signal detected! Immediate action required!"
        )

    if analysis.anomaly_score >= 5:
        return RiskResult(
            risk_level="CRITICAL",
            reason="Multiple critical sensor anomalies detected"
        )

    if analysis.anomaly_score >= 3:
        return RiskResult(
            risk_level="HIGH",
            reason="Multiple sensor anomalies indicate potential issues"
        )

    if analysis.anomaly_score >= 1:
        return RiskResult(
            risk_level="MEDIUM",
            reason="Minor anomalies detected - manual inspection recommended"
        )

    return RiskResult(
        risk_level="LOW",
        reason="All parameters within acceptable range"
    )


def decision_agent(risk: RiskResult) -> DecisionResult:
    """Make decision based on risk assessment"""
    
    if risk.risk_level == "CRITICAL":
        return DecisionResult(
            decision="TRIGGER_EMERGENCY",
            requires_human=True
        )

    if risk.risk_level == "HIGH":
        return DecisionResult(
            decision="ALERT_AND_STABILIZE",
            requires_human=True
        )

    if risk.risk_level == "MEDIUM":
        return DecisionResult(
            decision="CHECK_WAREHOUSE",
            requires_human=True
        )

    return DecisionResult(
        decision="MONITOR",
        requires_human=False
    )


def run_analysis_pipeline():
    """Execute full analysis pipeline"""
    print("\n" + "="*60)
    print("🏥 PHARMA AEGIS ANALYSIS PIPELINE")
    print("="*60)
    
    # Get latest sensor data
    sensor_data = get_latest_sensor_data()
    print(f"\n📊 Raw Sensor Data: {sensor_data}")
    
    # Create reading object
    reading = SensorReading(
        temperature=float(sensor_data.get("temperature", 20)),
        humidity=float(sensor_data.get("humidity", 50)),
        vibration=float(sensor_data.get("vibration", 1.0)),
        fire=int(sensor_data.get("fire", 0))
    )
    
    # Run analysis
    analysis = data_analyzer(reading)
    print(f"\n🔍 Analysis:")
    print(f"   Temperature: {analysis.temperature_status}")
    print(f"   Humidity: {analysis.humidity_status}")
    print(f"   Vibration: {analysis.vibration_status}")
    print(f"   Fire: {analysis.fire_status}")
    print(f"   Anomaly Score: {analysis.anomaly_score}")
    
    # Evaluate risk
    risk = risk_evaluator(analysis)
    print(f"\n⚠️  Risk Assessment:")
    print(f"   Level: {risk.risk_level}")
    print(f"   Reason: {risk.reason}")
    
    # Make decision
    decision = decision_agent(risk)
    print(f"\n✅ Decision:")
    print(f"   Action: {decision.decision}")
    print(f"   Human Review: {'Required' if decision.requires_human else 'Not required'}")
    print("="*60 + "\n")
    
    return analysis, risk, decision