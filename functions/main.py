from firebase_functions import https_fn
from firebase_functions.options import set_global_options
from firebase_admin import initialize_app
import json
import math
import datetime
import logging
from typing import Dict, List, Tuple, Any

  
from models.advanced_scoring import AdvancedCreditScoringEngine
from utils.security import SecurityValidator, DataEncryption

initialize_app()

set_global_options(max_instances=10)

class CreditDecisionEngine:
    def __init__(self):
        self.base_rate = 4.09  # Fixed rate as requested
        self.advanced_scoring = AdvancedCreditScoringEngine()
        self.security_validator = SecurityValidator()
    
    def _initialize_training_data(self) -> List[Dict]:
        return [
            {'age': 25, 'monthly_income': 5000, 'employment_years': 2, 'debt_ratio': 0.2, 'kkb_score': 650, 'approved': 0},
            {'age': 35, 'monthly_income': 12000, 'employment_years': 8, 'debt_ratio': 0.3, 'kkb_score': 750, 'approved': 1},
            {'age': 45, 'monthly_income': 8000, 'employment_years': 15, 'debt_ratio': 0.15, 'kkb_score': 720, 'approved': 1},
            {'age': 30, 'monthly_income': 15000, 'employment_years': 5, 'debt_ratio': 0.4, 'kkb_score': 680, 'approved': 1},
            {'age': 50, 'monthly_income': 20000, 'employment_years': 20, 'debt_ratio': 0.1, 'kkb_score': 800, 'approved': 1},
            {'age': 28, 'monthly_income': 6000, 'employment_years': 3, 'debt_ratio': 0.35, 'kkb_score': 640, 'approved': 0},
            {'age': 40, 'monthly_income': 18000, 'employment_years': 12, 'debt_ratio': 0.25, 'kkb_score': 780, 'approved': 1},
            {'age': 55, 'monthly_income': 25000, 'employment_years': 25, 'debt_ratio': 0.05, 'kkb_score': 820, 'approved': 1},
            {'age': 32, 'monthly_income': 7000, 'employment_years': 4, 'debt_ratio': 0.45, 'kkb_score': 620, 'approved': 0},
            {'age': 38, 'monthly_income': 14000, 'employment_years': 10, 'debt_ratio': 0.2, 'kkb_score': 740, 'approved': 1},
            {'age': 42, 'monthly_income': 22000, 'employment_years': 18, 'debt_ratio': 0.18, 'kkb_score': 785, 'approved': 1},
            {'age': 29, 'monthly_income': 9000, 'employment_years': 6, 'debt_ratio': 0.32, 'kkb_score': 665, 'approved': 0},
            {'age': 46, 'monthly_income': 16000, 'employment_years': 14, 'debt_ratio': 0.22, 'kkb_score': 735, 'approved': 1},
            {'age': 33, 'monthly_income': 11000, 'employment_years': 7, 'debt_ratio': 0.38, 'kkb_score': 695, 'approved': 1},
            {'age': 52, 'monthly_income': 24000, 'employment_years': 22, 'debt_ratio': 0.12, 'kkb_score': 810, 'approved': 1},
            {'age': 27, 'monthly_income': 8500, 'employment_years': 5, 'debt_ratio': 0.28, 'kkb_score': 675, 'approved': 0},
            {'age': 41, 'monthly_income': 19000, 'employment_years': 13, 'debt_ratio': 0.24, 'kkb_score': 755, 'approved': 1},
            {'age': 56, 'monthly_income': 26000, 'employment_years': 27, 'debt_ratio': 0.08, 'kkb_score': 825, 'approved': 1},
            {'age': 31, 'monthly_income': 10000, 'employment_years': 8, 'debt_ratio': 0.41, 'kkb_score': 655, 'approved': 0},
            {'age': 39, 'monthly_income': 17000, 'employment_years': 11, 'debt_ratio': 0.19, 'kkb_score': 745, 'approved': 1}
        ]
    
    def _calculate_similarity_score(self, applicant: Dict, reference: Dict) -> float:
        age_diff = abs(applicant.get('age', 35) - reference['age']) / 30
        income_diff = abs(applicant.get('monthly_income', 0) - reference['monthly_income']) / 20000
        exp_diff = abs(applicant.get('work_experience', 0) - reference['employment_years']) / 15
        debt_diff = abs(self._calculate_debt_ratio(applicant) - reference['debt_ratio']) / 0.5
        kkb_diff = abs(applicant.get('kkb_score', 500) - reference['kkb_score']) / 200
        
        total_diff = age_diff + income_diff + exp_diff + debt_diff + kkb_diff
        return max(0, 1 - total_diff / 5)
    
    def _calculate_debt_ratio(self, data: Dict) -> float:
        monthly_income = data.get('monthly_income', 0)
        additional_income = data.get('additional_income', 0)
        total_income = monthly_income + additional_income
        
        existing_loans = data.get('existing_loans', 0)
        credit_card_debt = data.get('credit_card_debt', 0)
        total_debt = existing_loans + credit_card_debt
        
        return total_debt / max(total_income, 1)
    

    def _ml_prediction(self, data: Dict) -> float:
        """Advanced ML prediction using mathematical analysis"""
        similarities = []
        approvals = []
        
        # Calculate similarities with all training data points
        for ref_data in self._initialize_training_data():
            # Multi-dimensional similarity calculation
            age_sim = max(0, 1 - abs(data.get('age', 35) - ref_data['age']) / 30)
            income_sim = max(0, 1 - abs(data.get('monthly_income', 0) - ref_data['monthly_income']) / 20000)
            exp_sim = max(0, 1 - abs(data.get('work_experience', 0) - ref_data['employment_years']) / 15)
            debt_sim = max(0, 1 - abs(self._calculate_debt_ratio(data) - ref_data['debt_ratio']) / 0.5)
            kkb_sim = max(0, 1 - abs(data.get('kkb_score', 500) - ref_data['kkb_score']) / 200)
            
            # Combined similarity with weighted factors
            combined_similarity = (age_sim * 0.15 + income_sim * 0.30 + exp_sim * 0.20 + 
                                 debt_sim * 0.25 + kkb_sim * 0.10)
            
            if combined_similarity > 0.1:  # Threshold for relevance
                similarities.append(combined_similarity)
                approvals.append(ref_data['approved'])
        
        if not similarities:
            return 0.5  # Neutral if no similar cases
        
        # Weighted prediction using similarity scores
        weighted_sum = sum(sim * app for sim, app in zip(similarities, approvals))
        total_weight = sum(similarities)
        
        # Add confidence boost based on number of similar cases
        confidence_factor = min(1.0, len(similarities) / 10)
        base_prediction = weighted_sum / total_weight if total_weight > 0 else 0.5
        
        return base_prediction * confidence_factor + 0.5 * (1 - confidence_factor)
    
    def calculate_credit_score(self, data: Dict) -> Tuple[float, List[str]]:
        """Calculate comprehensive credit score based on 25+ factors"""
        score = 0
        factors = []
        
        # 1. Basic Demographics (5%)
        age = data.get('age', 35)
        if 25 <= age <= 65:
            age_score = min(100, (age - 20) * 2)
        else:
            age_score = max(0, 100 - abs(age - 45) * 2)
        score += age_score * 0.05
        factors.append(f"Yaş Skoru: {age_score:.0f}/100")
        
        # 2. Income Analysis (25%)
        monthly_income = data.get('monthly_income', 0)
        additional_income = data.get('additional_income', 0)
        total_income = monthly_income + additional_income
        
        if total_income >= 35000:
            income_score = 100
        elif total_income >= 20000:
            income_score = 90
        elif total_income >= 15000:
            income_score = 85
        elif total_income >= 10000:
            income_score = 75
        elif total_income >= 7500:
            income_score = 65
        elif total_income >= 5000:
            income_score = 55
        else:
            income_score = max(30, total_income / 200)
        
        score += income_score * 0.25
        factors.append(f"Gelir Skoru: {income_score:.0f}/100 (₺{total_income:,.0f})")
        
        # 3. Employment Stability (15%)
        employment_years = data.get('work_experience', 0)
        employment_type = data.get('employment_type', '')
        
        employment_score = min(100, employment_years * 12 + 20)
        
        # Employment type bonus
        if 'Doktor' in employment_type or 'Mühendis' in employment_type:
            employment_score = min(100, employment_score * 1.2)
        elif 'Özel Sektör' in employment_type:
            employment_score = min(100, employment_score * 1.1)
        elif 'Kamu' in employment_type:
            employment_score = min(100, employment_score * 1.15)
        
        score += employment_score * 0.15
        factors.append(f"İstikrar Skoru: {employment_score:.0f}/100 ({employment_years} yıl)")
        
        # 4. Debt Analysis (20%)
        debt_ratio = self._calculate_debt_ratio(data)
        
        if debt_ratio <= 0.1:
            debt_score = 100
        elif debt_ratio <= 0.2:
            debt_score = 95
        elif debt_ratio <= 0.3:
            debt_score = 85
        elif debt_ratio <= 0.4:
            debt_score = 75
        elif debt_ratio <= 0.5:
            debt_score = 60
        else:
            debt_score = max(0, 20 - (debt_ratio - 0.5) * 40)
        
        score += debt_score * 0.20
        factors.append(f"Borç Skoru: {debt_score:.0f}/100 (Oran: %{debt_ratio*100:.1f})")
        
        # 5. Assets & Wealth (15%)
        bank_balance = data.get('bank_balance', 0)
        investments = data.get('investments', 0)
        real_estate_value = data.get('real_estate_value', 0)
        total_assets = bank_balance + investments + real_estate_value
        
        if total_assets >= 1000000:
            asset_score = 100
        elif total_assets >= 500000:
            asset_score = 90
        elif total_assets >= 250000:
            asset_score = 80
        elif total_assets >= 100000:
            asset_score = 70
        elif total_assets >= 50000:
            asset_score = 60
        else:
            asset_score = max(30, total_assets / 2000)
        
        score += asset_score * 0.15
        factors.append(f"Varlık Skoru: {asset_score:.0f}/100 (₺{total_assets:,.0f})")
        
        # 6. Credit History (10%)
        kkb_score = data.get('kkb_score', 500)
        payment_delays = data.get('payment_delays', 0)
        
        if kkb_score >= 800:
            credit_history_score = 100
        elif kkb_score >= 700:
            credit_history_score = 85
        elif kkb_score >= 600:
            credit_history_score = 70
        elif kkb_score >= 500:
            credit_history_score = 55
        else:
            credit_history_score = 30
        
        # Payment delays penalty
        delay_penalty = min(30, payment_delays * 5)
        credit_history_score = max(0, credit_history_score - delay_penalty)
        
        score += credit_history_score * 0.10
        factors.append(f"Kredi Geçmişi: {credit_history_score:.0f}/100 (KKB: {kkb_score})")
        
        # 7. Banking Relationship (5%)
        existing_relationship = data.get('existing_relationship', 0)
        total_banking_products = data.get('total_banking_products', 0)
        
        relationship_score = min(100, existing_relationship * 2)
        product_bonus = min(20, total_banking_products * 5)
        relationship_score = min(100, relationship_score + product_bonus)
        
        score += relationship_score * 0.05
        factors.append(f"Banka İlişkisi: {relationship_score:.0f}/100 ({existing_relationship} ay)")
        
        # 8. Loan Amount Risk (4%)
        loan_amount = data.get('loan_amount', 0)
        loan_to_income_ratio = loan_amount / max(total_income * 12, 1)  # Yıllık gelire göre
        
        if loan_to_income_ratio <= 2:
            loan_risk_score = 100
        elif loan_to_income_ratio <= 3:
            loan_risk_score = 85
        elif loan_to_income_ratio <= 4:
            loan_risk_score = 70
        elif loan_to_income_ratio <= 5:
            loan_risk_score = 55
        elif loan_to_income_ratio <= 6:
            loan_risk_score = 40
        else:
            loan_risk_score = max(20, 100 - (loan_to_income_ratio - 6) * 10)
        
        score += loan_risk_score * 0.04
        factors.append(f"Kredi/Gelir Riski: {loan_risk_score:.0f}/100 (Oran: {loan_to_income_ratio:.1f})")
        
        # 9. Loan Term Risk (3%)
        loan_term = data.get('loan_term_months', 12)
        
        if loan_term <= 12:
            term_risk_score = 100
        elif loan_term <= 24:
            term_risk_score = 90
        elif loan_term <= 36:
            term_risk_score = 80
        elif loan_term <= 48:
            term_risk_score = 70
        elif loan_term <= 60:
            term_risk_score = 60
        elif loan_term <= 84:
            term_risk_score = 50
        else:
            term_risk_score = max(30, 100 - (loan_term - 84) * 2)
        
        score += term_risk_score * 0.03
        factors.append(f"Vade Riski: {term_risk_score:.0f}/100 ({loan_term} ay)")
        
        # 9. AI/ML Component (5%)
        ml_prediction = self._ml_prediction(data)
        ml_score = ml_prediction * 100
        score += ml_score * 0.05
        factors.append(f"AI Tahmin: {ml_score:.0f}/100 (Risk: %{(1-ml_prediction)*100:.1f})")
        
        return min(100, max(0, score)), factors
    
    def determine_customer_segment(self, data: Dict) -> Tuple[str, str]:
        """Determine customer segment based on comprehensive profile"""
        monthly_income = data.get('monthly_income', 0)
        additional_income = data.get('additional_income', 0)
        total_income = monthly_income + additional_income
        assets = data.get('bank_balance', 0) + data.get('investments', 0) + data.get('real_estate_value', 0)
        employment_type = data.get('employment_type', '')
        
        # Corporate segment criteria
        if (total_income >= 40000 or assets >= 1000000 or 
            'Doktor' in employment_type or 'Mühendis' in employment_type):
            return "Corporate", "Kurumsal müşteri segmenti - özel koşullar ve hızlı işlem"
        
        # Private Banking segment criteria
        elif total_income >= 25000 or assets >= 500000:
            return "Private Banking", "Private Banking segmenti - premium faiz oranları ve özel danışman"
        
        # Mass Market segment
        else:
            return "Mass Market", "Bireysel müşteri segmenti - standart koşullar ve süreçler"
    
    def calculate_interest_rate(self, data: Dict, risk_score: float) -> Dict:
        """Calculate interest rate based on Turkish banking standards"""
        segment, _ = self.determine_customer_segment(data)
        
        # Segment-based rate adjustments
        if segment == "Corporate":
            segment_multiplier = 0.7  # %30 discount
        elif segment == "Private Banking":
            segment_multiplier = 0.85  # %15 discount
        else:
            segment_multiplier = 1.2  # %20 premium
        
        # Risk-based rate adjustments
        if risk_score >= 85:
            risk_multiplier = 0.9  # Low risk discount
        elif risk_score >= 70:
            risk_multiplier = 1.0  # Standard rate
        elif risk_score >= 55:
            risk_multiplier = 1.3  # Higher risk premium
        else:
            risk_multiplier = 1.6  # High risk premium
        
        # Calculate base monthly rate
        monthly_rate = self.base_rate * segment_multiplier * risk_multiplier
        
        # Add Turkish banking taxes
        kkdf_tax = monthly_rate * 0.15  # KKDF %15
        bsmv_tax = monthly_rate * 0.15  # BSMV %15
        final_rate = monthly_rate + kkdf_tax + bsmv_tax
        
        return {
            'base_rate': self.base_rate,
            'segment_multiplier': segment_multiplier,
            'risk_multiplier': risk_multiplier,
            'monthly_rate_before_tax': monthly_rate,
            'kkdf_tax': kkdf_tax,
            'bsmv_tax': bsmv_tax,
            'final_monthly_rate': final_rate,
            'annual_rate': final_rate * 12
        }
    
    def make_decision(self, data: Dict) -> Dict:
        """Make comprehensive credit decision using Advanced Scoring Engine (4.09% Fixed)"""
        try:
            # Basic data validation
            if not data or not isinstance(data, dict):
                return {
                    "decision": "ERROR",
                    "error": "Geçersiz veri formatı",
                    "timestamp": datetime.datetime.now().isoformat()
                }
            
            # Use new advanced scoring system with 4.09% fixed rate
            scoring_result = self.advanced_scoring.score_application(data)
            
            # Convert decision format to match frontend expectations
            decision_mapping = {
                "APPROVE": "ONAYLANDI",
                "CONDITIONAL": "CONDITIONAL",
                "REJECT": "REDDEDILDI"
            }
            
            turkish_decision = decision_mapping.get(scoring_result['decision'], "CONDITIONAL")
            
            # Generate Turkish decision reason
            score = scoring_result['score']
            if turkish_decision == "ONAYLANDI":
                decision_reason = f"Kredi onaylandı - Risk skoru: {score}/100. Güçlü finansal profil."
            elif turkish_decision == "CONDITIONAL":
                decision_reason = f"Koşullu onay - Risk skoru: {score}/100. Ek şartlar gerekli."
            else:
                decision_reason = f"Kredi reddedildi - Risk skoru: {score}/100. Risk kriterleri karşılanmadı."
            
            # Create detailed risk factors from advanced scoring
            risk_factors = []
            calc = scoring_result.get('calculations', {})
            expl = scoring_result.get('explainability', {})
            
            # Add detailed financial metrics
            risk_factors.append(f"Net Gelir: {calc.get('net_income', 0):,.0f} TL")
            risk_factors.append(f"Yeni DTI Oranı: %{calc.get('new_dti', 0)*100:.1f}")
            risk_factors.append(f"Aylık Taksit: {calc.get('new_installment', 0):,.0f} TL")
            risk_factors.append(f"Kredi Kartı Kullanım: %{calc.get('credit_utilization', 0)*100:.1f}")
            risk_factors.append(f"Likidite Oranı: {calc.get('liquidity_ratio', 0):.2f}")
            
            # Add top contributing factors
            for feature in expl.get('top_five_features', [])[:3]:  # Top 3 only
                risk_factors.append(f"{feature['feature']}: {feature['contribution']:.1f} puan")
            
            return {
                "decision": turkish_decision,
                "decision_reason": decision_reason,
                "credit_score": score,
                "risk_factors": risk_factors,
                "customer_segment": self._determine_segment_from_score(score),
                "segment_description": self._get_segment_description(score),
                "interest_rates": self._calculate_simple_rates(scoring_result),
                "loan_details": self._calculate_loan_details(data, scoring_result),
                "processing_info": self._get_processing_info(turkish_decision, score),
                "advanced_analysis": {
                    "explainability": expl,
                    "calculations": calc,
                    "assumptions": scoring_result.get('assumptions', {}),
                    "policy_flags": scoring_result.get('policy_flags', {}),
                    "limits": scoring_result.get('limits', {})
                },
                "timestamp": scoring_result.get('timestamp'),
                "engine_version": scoring_result.get('engine_version')
            }
            
        except Exception as e:
            return {
                "decision": "ERROR",
                "error": f"Kredi değerlendirme hatası: {str(e)}",
                "timestamp": datetime.datetime.now().isoformat()
            }
    
    def _determine_segment_from_score(self, score: float) -> str:
        """Determine customer segment from score"""
        if score >= 75:
            return "Private Banking"
        elif score >= 60:
            return "Corporate"
        else:
            return "Mass Market"
    
    def _get_segment_description(self, score: float) -> str:
        """Get segment description from score"""
        segment = self._determine_segment_from_score(score)
        descriptions = {
            "Private Banking": "Private Banking segmenti - premium faiz oranları ve özel danışman",
            "Corporate": "Kurumsal müşteri segmenti - özel koşullar ve hızlı işlem",
            "Mass Market": "Bireysel müşteri segmenti - standart koşullar ve süreçler"
        }
        return descriptions.get(segment, "Standart müşteri segmenti")
    
    def _calculate_simple_rates(self, scoring_result: Dict) -> Dict:
        """Calculate simplified interest rates for display"""
        annual_rate = scoring_result.get('assumptions', {}).get('annual_rate', 4.09)
        monthly_rate = annual_rate / 12
        
        return {
            'base_rate': annual_rate,
            'monthly_rate': monthly_rate,
            'annual_rate': annual_rate,
            'kkdf_tax': annual_rate * 0.15,
            'bsmv_tax': annual_rate * 0.15,
            'final_annual_rate': annual_rate * 1.3  # With taxes
        }
    
    def _calculate_loan_details(self, data: Dict, scoring_result: Dict) -> Dict:
        """Calculate loan details using fixed rate"""
        loan_amount = data.get('loan_amount', 0)
        loan_term = data.get('loan_term_months', 12)
        monthly_installment = scoring_result.get('calculations', {}).get('new_installment', 0)
        
        total_payment = monthly_installment * loan_term
        total_interest = total_payment - loan_amount
        
        return {
            "requested_amount": loan_amount,
            "term_months": loan_term,
            "monthly_payment": round(monthly_installment, 2),
            "total_payment": round(total_payment, 2),
            "total_interest": round(total_interest, 2),
            "effective_annual_rate": 4.09
        }
    
    def _get_processing_info(self, decision: str, score: float) -> Dict:
        """Get processing information"""
        segment = self._determine_segment_from_score(score)
        
        base_docs = ["Nüfus cüzdanı", "Gelir belgesi", "İkametgah belgesi"]
        
        if decision == "ONAYLANDI":
            next_steps = ["Hızlı onay süreci", "Belge kontrolü", "Sözleşme hazırlama"]
        elif decision == "CONDITIONAL":
            next_steps = ["Ek belge talep edilecek", "Risk analizi", "Koşullu değerlendirme"]
            base_docs.extend(["Ek teminat belgesi", "Kefil bilgileri"])
        else:
            next_steps = ["Ret gerekçesi", "Alternatif öneriler", "Yeniden başvuru koşulları"]
        
        return {
            "processing_time": f"{segment} müşteriler için özel işlem süresi",
            "required_documents": base_docs,
            "next_steps": next_steps
        }
    

# Initialize the decision engine
decision_engine = CreditDecisionEngine()

@https_fn.on_request()
def evaluate_credit(req: https_fn.Request) -> https_fn.Response:
    """Firebase Cloud Function for AI credit evaluation"""
    
    # Comprehensive CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, DELETE',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With, Accept, Origin',
        'Access-Control-Max-Age': '86400',
        'Content-Type': 'application/json; charset=utf-8',
        'Vary': 'Origin'
    }
    
    # Handle preflight OPTIONS request
    if req.method == 'OPTIONS':
        return https_fn.Response('', status=200, headers=headers)
    
    try:
        if req.method != 'POST':
            return https_fn.Response(
                json.dumps({"error": "Only POST method allowed"}, ensure_ascii=False),
                status=405,
                headers=headers
            )
        
        # Parse request data with better error handling
        try:
            data = req.get_json()
        except Exception as json_error:
            return https_fn.Response(
                json.dumps({"error": f"Invalid JSON: {str(json_error)}"}, ensure_ascii=False),
                status=400,
                headers=headers
            )
            
        if not data:
            return https_fn.Response(
                json.dumps({"error": "No data provided"}, ensure_ascii=False),
                status=400,
                headers=headers
            )
        
        # Make credit decision using AI engine  
        result = decision_engine.make_decision(data)
        
        return https_fn.Response(
            json.dumps(result, ensure_ascii=False),
            status=200,
            headers=headers
        )
        
    except Exception as e:
        error_response = {
            "error": "Credit evaluation failed",
            "message": str(e),
            "timestamp": datetime.datetime.now().isoformat()
        }
        return https_fn.Response(
            json.dumps(error_response, ensure_ascii=False),
            status=500,
            headers=headers
        )

@https_fn.on_request()
def health_check(req: https_fn.Request) -> https_fn.Response:
    """Health check endpoint for monitoring"""
    return https_fn.Response(
        "Finiş Bankası AI Credit Engine v2.0 (Pure Python) - Çalışıyor! ✅", 
        status=200
    )

@https_fn.on_request()
def system_info(req: https_fn.Request) -> https_fn.Response:
    """System information endpoint"""
    info = {
        "system": "Finiş Bankası AI Credit Engine",
        "version": "2.0 (Pure Python)",
        "features": [
            "25+ faktörlü kredi skorlaması",
            "3 müşteri segmenti (Mass/Private Banking/Corporate)", 
            "Türk bankacılık standartları (KKDF/BSMV)",
            "Pure Python AI algoritmaları",
            "Gerçek zamanlı karar motoru",
            "Benzerlik tabanlı risk değerlendirmesi"
        ],
        "status": "active",
        "timestamp": datetime.datetime.now().isoformat(),
        "runtime": "Python 3.13 (Firebase Functions)"
    }
    
    return https_fn.Response(
        json.dumps(info, ensure_ascii=False),
        status=200,
        headers={'Content-Type': 'application/json; charset=utf-8'}
    )