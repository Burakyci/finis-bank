from typing import Dict, Any, List, Literal
import datetime

Decision = Literal["APPROVE", "CONDITIONAL", "REJECT"]

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))

def annuity_payment(P: float, r: float, n: int) -> float:
    if r <= 0 or n <= 0:
        return P / max(n, 1)
    a = (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return P * a

class AdvancedCreditScoringEngine:
    
    def __init__(self):
        self.annual_rate = 4.09
        self.monthly_rate = 4.09 / 100 / 12  # 0.003408
        
        self.weights = {
            'kkb_credit_history': 25,
            'dti_ratio': 20,
            'income_adequacy': 15,
            'credit_utilization': 8,
            'liquidity': 10,
            'collateral_assets': 8,
            'stability': 7,
            'banking_relationship': 5,
            'max_penalty': 20
        }
        
        self.approve_threshold = 75
        self.conditional_threshold = 60
    
    def score_application(self, data: Dict[str, Any]) -> Dict[str, Any]:
        
        # Extract and organize input data
        loan_amount = float(data.get('loan_amount', 0))
        loan_term_months = int(data.get('loan_term_months', 12))
        
        # Financial data
        monthly_income = float(data.get('monthly_income', 0))
        additional_income = float(data.get('additional_income', 0))
        expenses = float(data.get('expenses', 0))
        rent_payment = float(data.get('rent_payment', 0))
        existing_loans = float(data.get('existing_loans', 0))
        credit_card_debt = float(data.get('credit_card_debt', 0))
        credit_card_limit = float(data.get('credit_card_limit', 0))
        bank_balance = float(data.get('bank_balance', 0))
        investments = float(data.get('investments', 0))
        real_estate_value = float(data.get('real_estate_value', 0))
        
        # Personal data
        age = int(data.get('age', 30))
        employment_type = str(data.get('employment_type', '')).lower()
        work_experience = float(data.get('work_experience', 0))
        kkb_score = float(data.get('kkb_score', 500))
        payment_delays = int(data.get('payment_delays', 0))
        home_ownership = str(data.get('home_ownership', '')).lower()
        residence_duration = float(data.get('residence_duration', 0))
        
        # Banking relationship
        existing_relationship = float(data.get('existing_relationship', 0))
        total_products = int(data.get('total_banking_products', 0))
        customer_segment = str(data.get('customer_segment', 'mass')).lower()
        
        # Risk factors
        defaulted_loans = bool(data.get('defaulted_loans', False))
        legal_issues = bool(data.get('legal_issues', False))
        has_insurance = bool(data.get('has_insurance', False))
        job_stability = str(data.get('job_stability', 'stable')).lower()
        
        # Calculate derived variables
        net_income = max(0, monthly_income + additional_income - expenses - rent_payment)
        
        # Calculate current debt payments
        dti = data.get('debt_to_income_ratio')
        if dti is not None:
            current_monthly_debt = float(dti) * net_income if net_income > 0 else 0.0
            dti_note = "DTI girdiden alındı"
        else:
            # Heuristic calculation
            cc_min = 0.04 * credit_card_debt  # 4% minimum payment
            loan_payment = annuity_payment(existing_loans, self.monthly_rate, 24) if existing_loans > 0 else 0.0
            current_monthly_debt = cc_min + loan_payment
            dti_note = "DTI hesaplandı (CC=%4, krediler=24ay)"
        
        # New loan installment
        new_installment = annuity_payment(loan_amount, self.monthly_rate, loan_term_months)
        
        # New DTI ratio
        new_dti = (current_monthly_debt + new_installment) / net_income if net_income > 0 else 1.0
        
        # Other ratios
        credit_util = credit_card_debt / credit_card_limit if credit_card_limit > 0 else 0.0
        liquidity_ratio = (bank_balance + 0.8 * investments) / loan_amount if loan_amount > 0 else 0.0
        collateral_factor = (real_estate_value / loan_amount) if (loan_amount > 0 and home_ownership == "owner") else 0.0
        
        # Calculate individual scores (0-1 scale)
        scores = self._calculate_component_scores(
            kkb_score, new_dti, new_installment, net_income, credit_util,
            liquidity_ratio, collateral_factor, work_experience, residence_duration,
            employment_type, job_stability, existing_relationship, total_products,
            customer_segment, payment_delays, defaulted_loans, legal_issues
        )
        
        # Apply weights and calculate total score
        total_score = 0.0
        contributions = {}
        
        for component, weight in self.weights.items():
            if component == 'max_penalty':
                continue
            component_score = scores.get(component, 0.0)
            contribution = clamp(component_score, 0.0, 1.0) * weight
            total_score += contribution
            contributions[component] = contribution
        
        # Apply penalties
        penalty_score = self._calculate_penalties(payment_delays, defaulted_loans, legal_issues)
        penalty_points = penalty_score * self.weights['max_penalty']
        total_score = clamp(total_score - penalty_points, 0.0, 100.0)
        
        # Policy caps for high-risk cases
        hard_block = False
        policy_reasons = []
        if defaulted_loans or legal_issues:
            total_score = min(total_score, 60.0)
            hard_block = True
            if defaulted_loans:
                policy_reasons.append("Geçmiş temerrüt")
            if legal_issues:
                policy_reasons.append("Hukuki ihtilaf")
        
        # Make decision
        if total_score >= self.approve_threshold:
            decision: Decision = "APPROVE"
        elif total_score >= self.conditional_threshold:
            decision = "CONDITIONAL" 
        else:
            decision = "REJECT"
        
        # Calculate limits and recommendations
        limits = self._calculate_limits(net_income, loan_amount, loan_term_months, new_dti, decision)
        
        # Generate explanations
        explanations = self._generate_explanations(scores, contributions, penalty_points)
        
        return {
            "score": round(total_score, 2),
            "decision": decision,
            "limits": limits,
            "assumptions": {
                "monthly_interest_rate_used": self.monthly_rate,
                "annual_rate": self.annual_rate,
                "notes": [
                    dti_note,
                    "Annüite formülü kullanıldı",
                    f"Sabit faiz oranı: %{self.annual_rate}",
                    "Yatırımlar %80 ağırlıkla likidite hesabında"
                ]
            },
            "explainability": explanations,
            "calculations": {
                "net_income": round(net_income, 2),
                "current_monthly_debt_payment": round(current_monthly_debt, 2),
                "new_installment": round(new_installment, 2),
                "new_dti": round(new_dti, 4),
                "credit_utilization": round(credit_util, 4),
                "liquidity_ratio": round(liquidity_ratio, 4),
                "collateral_factor": round(collateral_factor, 4)
            },
            "policy_flags": {
                "hard_block": hard_block,
                "reasons": policy_reasons
            },
            "timestamp": datetime.datetime.now().isoformat(),
            "engine_version": "Finiş Bankası Advanced Scoring v3.0 (Fixed 4.09%)"
        }
    
    def _calculate_component_scores(self, kkb_score: float, new_dti: float, new_installment: float,
                                  net_income: float, credit_util: float, liquidity_ratio: float,
                                  collateral_factor: float, work_experience: float, residence_duration: float,
                                  employment_type: str, job_stability: str, existing_relationship: float,
                                  total_products: int, customer_segment: str, payment_delays: int,
                                  defaulted_loans: bool, legal_issues: bool) -> Dict[str, float]:
        """Calculate individual component scores"""
        
        # KKB Score (300-900 -> 0-1)
        kkb_norm = clamp((kkb_score - 300.0) / 600.0, 0.0, 1.0)
        
        # DTI Score (0.2 excellent, 0.6 poor)
        if new_dti <= 0.2:
            dti_score = 1.0
        elif new_dti >= 0.6:
            dti_score = 0.0
        else:
            dti_score = 1.0 - (new_dti - 0.2) / (0.6 - 0.2)
        
        # Income adequacy (installment/income ratio)
        payment_ratio = new_installment / net_income if net_income > 0 else 1.0
        if payment_ratio <= 0.3:
            income_score = 1.0
        elif payment_ratio >= 0.7:
            income_score = 0.0
        else:
            income_score = 1.0 - (payment_ratio - 0.3) / (0.7 - 0.3)
        
        # Credit utilization (0 excellent, 1 poor)
        credit_util_score = 1.0 - clamp(credit_util, 0.0, 1.0)
        
        # Liquidity score (0-2.0 range, saturated)
        liquidity_score = clamp(liquidity_ratio / 2.0, 0.0, 1.0)
        
        # Collateral score (0-3.0 range, saturated)
        collateral_score = clamp(collateral_factor / 3.0, 0.0, 1.0)
        
        # Stability score
        stability_base = 0.0
        if job_stability == "stable":
            stability_base += 0.6
        stability_base += clamp(work_experience / 10.0, 0.0, 0.3)
        stability_base += clamp(residence_duration / 120.0, 0.0, 0.1)
        if employment_type in ("kamu", "public"):
            stability_base += 0.2
        stability_score = clamp(stability_base, 0.0, 1.0)
        
        # Banking relationship score
        rel_score = clamp(existing_relationship / 60.0, 0.0, 0.6)
        rel_score += clamp(total_products / 6.0, 0.0, 0.3)
        if customer_segment == "private":
            rel_score += 0.1
        relationship_score = clamp(rel_score, 0.0, 1.0)
        
        return {
            'kkb_credit_history': kkb_norm,
            'dti_ratio': dti_score,
            'income_adequacy': income_score,
            'credit_utilization': credit_util_score,
            'liquidity': liquidity_score,
            'collateral_assets': collateral_score,
            'stability': stability_score,
            'banking_relationship': relationship_score
        }
    
    def _calculate_penalties(self, payment_delays: int, defaulted_loans: bool, legal_issues: bool) -> float:
        """Calculate penalty score (0-1 scale)"""
        penalty = 0.0
        if defaulted_loans:
            penalty += 0.35
        if legal_issues:
            penalty += 0.35
        penalty += clamp(payment_delays / 6.0, 0.0, 0.2)  # Max 6 delays = 0.2 penalty
        
        return clamp(penalty, 0.0, 1.0)
    
    def _calculate_limits(self, net_income: float, loan_amount: float, loan_term_months: int,
                         new_dti: float, decision: Decision) -> Dict[str, Any]:
        """Calculate recommended limits and terms"""
        
        # Target 35% payment ratio for safe lending
        target_payment_ratio = 0.35
        
        if net_income > 0 and self.monthly_rate > 0:
            target_installment = net_income * target_payment_ratio
            
            # Find maximum amount for target installment
            max_amount = 0.0
            step = max(loan_amount / 50.0, 1000.0)
            test_amount = step
            
            while test_amount <= loan_amount * 1.5:
                payment = annuity_payment(test_amount, self.monthly_rate, loan_term_months)
                if payment <= target_installment:
                    max_amount = test_amount
                    test_amount += step
                else:
                    break
            
            max_approved_amount = round(max_amount, -3)  # Round to nearest 1000
        else:
            max_approved_amount = 0.0
        
        # Recommend term adjustment for conditional approvals
        recommended_term = loan_term_months
        if decision == "CONDITIONAL" and new_dti > 0.45:
            # Extend term to reduce DTI
            recommended_term = min(loan_term_months + 12, 84)
        
        return {
            "max_approved_amount": max_approved_amount,
            "recommended_term_months": recommended_term
        }
    
    def _generate_explanations(self, scores: Dict[str, float], contributions: Dict[str, float],
                              penalty_points: float) -> Dict[str, Any]:
        """Generate human-readable explanations"""
        
        positives = []
        negatives = []
        
        # Positive factors
        if scores.get('kkb_credit_history', 0) >= 0.7:
            positives.append("Yüksek KKB skoru - güvenilir kredi geçmişi")
        if scores.get('dti_ratio', 0) >= 0.7:
            positives.append("Sürdürülebilir borç/gelir oranı")
        if scores.get('credit_utilization', 0) >= 0.7:
            positives.append("Düşük kredi kartı kullanım oranı - disiplinli harcama")
        if scores.get('liquidity', 0) >= 0.6:
            positives.append("Güçlü nakit rezervi ve yatırım portföyü")
        if scores.get('collateral_assets', 0) >= 0.4:
            positives.append("Değerli varlık ve teminat desteği")
        if scores.get('stability', 0) >= 0.6:
            positives.append("İstikrarlı iş ve ikamet durumu")
        if scores.get('banking_relationship', 0) >= 0.5:
            positives.append("Uzun vadeli banka müşteri ilişkisi")
        
        # Negative factors
        if scores.get('kkb_credit_history', 0) < 0.4:
            negatives.append("Düşük KKB skoru - kredi geçmişi risk taşıyor")
        if scores.get('dti_ratio', 0) < 0.4:
            negatives.append("Yüksek toplam borç yükü - sürdürülebilirlik riski")
        if scores.get('credit_utilization', 0) < 0.4:
            negatives.append("Yüksek kredi kartı kullanım oranı")
        if scores.get('liquidity', 0) < 0.4:
            negatives.append("Yetersiz nakit rezervi")
        if scores.get('stability', 0) < 0.4:
            negatives.append("İş veya ikamet istikrarsızlığı")
        
        if penalty_points > 0:
            negatives.append(f"Risk cezası: {penalty_points:.1f} puan")
        
        # Top 5 features by contribution
        top_features = sorted(contributions.items(), key=lambda x: x[1], reverse=True)[:5]
        
        feature_names = {
            'kkb_credit_history': 'KKB Kredi Geçmişi',
            'dti_ratio': 'Borç/Gelir Oranı',
            'income_adequacy': 'Gelir Yeterliliği',
            'credit_utilization': 'Kredi Kartı Kullanımı',
            'liquidity': 'Likidite Durumu',
            'collateral_assets': 'Teminat Varlıkları',
            'stability': 'İstikrar Faktörü',
            'banking_relationship': 'Banka İlişkisi'
        }
        
        top_five = []
        for feature, contribution in top_features:
            impact = "HIGH" if contribution >= 12 else "MEDIUM" if contribution >= 6 else "LOW"
            direction = "+" if contribution > 0 else "-"
            
            top_five.append({
                "feature": feature_names.get(feature, feature),
                "impact": impact,
                "direction": direction,
                "contribution": round(contribution, 1),
                "reason": f"{contribution:.1f} puan katkı"
            })
        
        return {
            "positives": positives,
            "negatives": negatives,
            "top_five_features": top_five
        }