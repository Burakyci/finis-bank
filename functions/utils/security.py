# Security utilities for AI backend
import hashlib
import hmac
import time
from typing import Dict, Any, Optional
import logging

class SecurityValidator:
    """Security validation for API requests"""
    
    def __init__(self):
        self.rate_limits = {}
        self.max_requests_per_minute = 30
        self.max_requests_per_hour = 200
        
    def validate_request_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize incoming request data"""
        
        validation_result = {
            'valid': True,
            'errors': [],
            'sanitized_data': {}
        }
        
        try:
            # Required fields validation
            required_fields = [
                'loan_amount', 'loan_term_months', 'monthly_income',
                'debt_to_income_ratio', 'kkb_score'
            ]
            
            for field in required_fields:
                if field not in data:
                    validation_result['errors'].append(f'Missing required field: {field}')
                    validation_result['valid'] = False
            
            if not validation_result['valid']:
                return validation_result
            
            # Sanitize and validate numerical fields
            numerical_fields = {
                'loan_amount': {'min': 1000, 'max': 2000000},
                'loan_term_months': {'min': 3, 'max': 240},
                'monthly_income': {'min': 0, 'max': 1000000},
                'debt_to_income_ratio': {'min': 0, 'max': 5},
                'kkb_score': {'min': 300, 'max': 900},
                'age': {'min': 18, 'max': 80},
                'work_experience': {'min': 0, 'max': 50}
            }
            
            for field, constraints in numerical_fields.items():
                if field in data:
                    try:
                        value = float(data[field])
                        if value < constraints['min'] or value > constraints['max']:
                            validation_result['errors'].append(
                                f'{field} must be between {constraints["min"]} and {constraints["max"]}'
                            )
                            validation_result['valid'] = False
                        else:
                            validation_result['sanitized_data'][field] = value
                    except (ValueError, TypeError):
                        validation_result['errors'].append(f'{field} must be a valid number')
                        validation_result['valid'] = False
            
            # String field validation
            string_fields = ['employment_type', 'customer_segment', 'home_ownership']
            for field in string_fields:
                if field in data:
                    value = str(data[field]).strip()
                    if len(value) > 100:  # Prevent overly long strings
                        value = value[:100]
                    validation_result['sanitized_data'][field] = value
            
            # Boolean field validation
            boolean_fields = ['defaulted_loans', 'legal_issues', 'has_insurance']
            for field in boolean_fields:
                if field in data:
                    validation_result['sanitized_data'][field] = bool(data[field])
            
            return validation_result
            
        except Exception as e:
            validation_result['valid'] = False
            validation_result['errors'].append(f'Validation error: {str(e)}')
            return validation_result
    
    def check_rate_limit(self, client_ip: str) -> Dict[str, Any]:
        """Check if client has exceeded rate limits"""
        
        current_time = time.time()
        
        if client_ip not in self.rate_limits:
            self.rate_limits[client_ip] = {
                'requests': [],
                'blocked_until': 0
            }
        
        client_data = self.rate_limits[client_ip]
        
        # Check if client is currently blocked
        if current_time < client_data['blocked_until']:
            return {
                'allowed': False,
                'reason': 'Rate limit exceeded. Please try again later.',
                'retry_after': int(client_data['blocked_until'] - current_time)
            }
        
        # Clean old requests (older than 1 hour)
        client_data['requests'] = [
            req_time for req_time in client_data['requests']
            if current_time - req_time < 3600
        ]
        
        # Check hourly limit
        if len(client_data['requests']) >= self.max_requests_per_hour:
            client_data['blocked_until'] = current_time + 1800  # Block for 30 minutes
            return {
                'allowed': False,
                'reason': 'Hourly rate limit exceeded',
                'retry_after': 1800
            }
        
        # Check per-minute limit
        recent_requests = [
            req_time for req_time in client_data['requests']
            if current_time - req_time < 60
        ]
        
        if len(recent_requests) >= self.max_requests_per_minute:
            return {
                'allowed': False,
                'reason': 'Per-minute rate limit exceeded',
                'retry_after': 60
            }
        
        # Add current request
        client_data['requests'].append(current_time)
        
        return {'allowed': True}
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security-related events"""
        
        logging.warning(f"Security Event: {event_type} - {details}")

class DataEncryption:
    """Data encryption utilities"""
    
    @staticmethod
    def hash_sensitive_data(data: str) -> str:
        """Hash sensitive data using SHA-256"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def generate_request_signature(data: Dict[str, Any], secret_key: str) -> str:
        """Generate HMAC signature for request validation"""
        data_string = str(sorted(data.items()))
        return hmac.new(
            secret_key.encode(),
            data_string.encode(),
            hashlib.sha256
        ).hexdigest()