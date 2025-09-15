# Advanced credit scoring model
from datetime import datetime
from typing import Dict, Any, Tuple

class CreditScoringEngine:
    """Advanced credit scoring engine with Turkish banking standards"""
    
    def __init__(self):
        self.risk_factors = {
            'income_stability': 0.25,
            'debt_to_income': 0.20,
            'kkb_score': 0.15,
            'employment_history': 0.12,
            'banking_relationship': 0.10,
            'collateral_assets': 0.08,
            'payment_history': 0.10
        }
        
        self.segment_thresholds = {
            'mass': {'min_income': 8000, 'max_loan': 300000},
            'private': {'min_income': 40000, 'max_loan': 1000000},
            'corporate': {'min_income': 25000, 'max_loan': 750000}
        }

    def calculate_risk_score(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive risk score"""
        
        try:
            # Extract key metrics
            monthly_income = float(application_data.get('monthly_income', 0))
            debt_to_income = float(application_data.get('debt_to_income_ratio', 0))
            kkb_score = int(application_data.get('kkb_score', 500))
            loan_amount = float(application_data.get('loan_amount', 0))
            employment_years = float(application_data.get('work_experience', 0))
            
            # Income stability score (0-100)
            income_score = min(100, (monthly_income / 10000) * 50 + 
                             (employment_years / 10) * 30 + 20)
            
            # Debt ratio score (0-100) - lower debt ratio = higher score
            debt_score = max(0, 100 - (debt_to_income * 200))
            
            # KKB score normalization (300-900 -> 0-100)
            kkb_normalized = max(0, min(100, ((kkb_score - 300) / 600) * 100))
            
            # Employment stability
            employment_score = min(100, (employment_years / 15) * 100)
            
            # Banking relationship score
            relationship_months = float(application_data.get('existing_relationship', 0))
            banking_score = min(100, (relationship_months / 60) * 100)
            
            # Asset collateral score
            real_estate = float(application_data.get('real_estate_value', 0))
            investments = float(application_data.get('investments', 0))
            total_assets = real_estate + investments
            asset_score = min(100, (total_assets / 500000) * 100)
            
            # Payment history score
            payment_delays = int(application_data.get('payment_delays', 0))
            payment_score = max(0, 100 - (payment_delays * 25))
            
            # Calculate weighted risk score
            risk_score = (
                income_score * self.risk_factors['income_stability'] +
                debt_score * self.risk_factors['debt_to_income'] +
                kkb_normalized * self.risk_factors['kkb_score'] +
                employment_score * self.risk_factors['employment_history'] +
                banking_score * self.risk_factors['banking_relationship'] +
                asset_score * self.risk_factors['collateral_assets'] +
                payment_score * self.risk_factors['payment_history']
            )
            
            # Customer segmentation
            segment = self._determine_segment(monthly_income, total_assets)
            
            # Risk category
            risk_category = self._categorize_risk(risk_score)
            
            # Loan to income ratio check
            loan_to_income_ratio = loan_amount / (monthly_income * 12) if monthly_income > 0 else float('inf')
            
            return {
                'risk_score': round(risk_score, 2),
                'risk_category': risk_category,
                'customer_segment': segment,
                'loan_to_income_ratio': round(loan_to_income_ratio, 2),
                'component_scores': {
                    'income': round(income_score, 1),
                    'debt': round(debt_score, 1),
                    'kkb': round(kkb_normalized, 1),
                    'employment': round(employment_score, 1),
                    'banking': round(banking_score, 1),
                    'assets': round(asset_score, 1),
                    'payment_history': round(payment_score, 1)
                }
            }
            
        except Exception as e:
            return {
                'error': f'Risk calculation failed: {str(e)}',
                'risk_score': 0,
                'risk_category': 'HIGH_RISK'
            }

    def _determine_segment(self, income: float, assets: float) -> str:
        """Determine customer segment based on income and assets"""
        if income >= 40000 and assets >= 300000:
            return 'private'
        elif income >= 25000 and assets >= 100000:
            return 'corporate'
        else:
            return 'mass'

    def _categorize_risk(self, score: float) -> str:
        """Categorize risk based on score"""
        if score >= 80:
            return 'LOW_RISK'
        elif score >= 60:
            return 'MEDIUM_RISK'
        elif score >= 40:
            return 'HIGH_RISK'
        else:
            return 'VERY_HIGH_RISK'

    def make_decision(self, risk_data: Dict[str, Any], application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make final credit decision"""
        
        risk_score = risk_data.get('risk_score', 0)
        loan_amount = float(application_data.get('loan_amount', 0))
        segment = risk_data.get('customer_segment', 'mass')
        
        # Decision matrix based on risk score and segment
        if risk_score >= 75:
            approved = True
            recommended_amount = loan_amount
            conditions = ['Standart kredi koşulları geçerlidir']
        elif risk_score >= 60:
            approved = True
            recommended_amount = min(loan_amount, loan_amount * 0.8)
            conditions = ['Ek teminat gerekebilir', 'Daha yüksek faiz oranı uygulanabilir']
        elif risk_score >= 45:
            approved = False
            recommended_amount = min(loan_amount, loan_amount * 0.5)
            conditions = ['Ek gelir belgesi gerekli', 'Kefil veya teminat zorunlu']
        else:
            approved = False
            recommended_amount = 0
            conditions = ['Mevcut şartlarda kredi verilemez', 'Gelir artışı sonrası tekrar değerlendirilebilir']
        
        # Risk factors affecting decision
        factors = []
        scores = risk_data.get('component_scores', {})
        
        if scores.get('income', 0) < 50:
            factors.append('Düşük gelir seviyesi')
        if scores.get('debt', 0) < 60:
            factors.append('Yüksek borç/gelir oranı')
        if scores.get('kkb', 0) < 50:
            factors.append('Düşük KKB skoru')
        if scores.get('employment', 0) < 40:
            factors.append('Kısa iş deneyimi')
        
        decision_reason = self._generate_decision_reason(approved, risk_score, factors)
        
        return {
            'approved': approved,
            'risk_score': risk_score,
            'recommended_amount': recommended_amount,
            'decision_reason': decision_reason,
            'conditions': conditions,
            'factors': factors,
            'segment': segment,
            'timestamp': datetime.now().isoformat()
        }

    def _generate_decision_reason(self, approved: bool, score: float, factors: list) -> str:
        """Generate human-readable decision reason"""
        if approved:
            return f"Kredi başvurunuz onaylanmıştır. Risk skoru: {score}/100. Güçlü finansal profil tespit edilmiştir."
        else:
            main_issues = ', '.join(factors[:2]) if factors else 'Genel risk değerlendirmesi'
            return f"Kredi başvurunuz reddedilmiştir. Risk skoru: {score}/100. Ana sorunlar: {main_issues}."