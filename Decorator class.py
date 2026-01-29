# patterns/evaluation_decorator.py

from abc import ABC, abstractmethod
import time
from typing import Dict, Any, List
import hashlib
from datetime import datetime

# ==================== Base Evaluation Classes ====================

class Submission:
    """Represents a research submission"""
    def __init__(self, submission_id: str, title: str, content: str, author: str):
        self.submission_id = submission_id
        self.title = title
        self.content = content
        self.author = author
        self.word_count = len(content.split())
        self.created_at = datetime.now()
    
    def get_hash(self) -> str:
        """Generate a unique hash for caching"""
        data = f"{self.submission_id}:{self.title}:{self.content[:500]}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def __str__(self):
        return f"Submission('{self.title}', {self.word_count} words)"

class EvaluationResult:
    """Container for evaluation results"""
    def __init__(self, score: float, feedback: str, metadata: Dict[str, Any]):
        self.score = score
        self.feedback = feedback
        self.metadata = metadata
        self.timestamp = time.time()
        self.is_cached = False
    
    def __str__(self):
        cache_indicator = " [CACHED]" if self.is_cached else ""
        return f"Score: {self.score:.2f}/100{cache_indicator} | {self.feedback[:60]}..."

# Abstract base class for evaluation strategies
class EvaluationStrategy(ABC):
    """Abstract interface for evaluation strategies"""
    
    @abstractmethod
    def evaluate(self, submission: Submission) -> EvaluationResult:
        """Evaluate a submission and return result"""
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """Return name of the evaluation strategy"""
        pass

# Concrete Strategy 1: Rule-based Evaluation
class RuleBasedEvaluation(EvaluationStrategy):
    """Evaluates submissions based on predefined rules"""
    
    def __init__(self):
        self.rules = {
            "min_word_count": 1000,
            "max_word_count": 10000,
            "required_sections": ["abstract", "methodology", "results"],
            "min_references": 5
        }
    
    def evaluate(self, submission: Submission) -> EvaluationResult:
        print(f"  [Rule-Based] Evaluating '{submission.title}'...")
        time.sleep(1.5)  # Simulate expensive operation
        
        # Rule checking logic
        score = 0.0
        feedback_parts = []
        
        # Word count check (30 points)
        if self.rules["min_word_count"] <= submission.word_count <= self.rules["max_word_count"]:
            score += 30
            feedback_parts.append(f"Word count OK ({submission.word_count})")
        elif submission.word_count < self.rules["min_word_count"]:
            feedback_parts.append(f"Too short ({submission.word_count}/{self.rules['min_word_count']})")
        else:
            feedback_parts.append(f"Too long ({submission.word_count}/{self.rules['max_word_count']})")
        
        # Section checks (40 points)
        content_lower = submission.content.lower()
        sections_found = []
        
        for section in self.rules["required_sections"]:
            if section in content_lower:
                sections_found.append(section)
                score += 13.33  # 40/3 points per section
        
        if sections_found:
            feedback_parts.append(f"Sections: {', '.join(sections_found)}")
        
        # Reference count simulation (20 points)
        ref_count = content_lower.count("reference") + content_lower.count("cite")
        if ref_count >= self.rules["min_references"]:
            score += 20
            feedback_parts.append(f"References sufficient ({ref_count})")
        else:
            feedback_parts.append(f"References insufficient ({ref_count}/{self.rules['min_references']})")
        
        # Formatting (10 points)
        if "." in submission.content and len(submission.content.split()) > 50:
            score += 10
            feedback_parts.append("Proper formatting")
        
        # Cap score at 100
        score = min(100, max(0, score))
        
        metadata = {
            "strategy": "rule_based",
            "word_count": submission.word_count,
            "sections_found": sections_found,
            "reference_count": ref_count,
            "processing_time_ms": 1500
        }
        
        return EvaluationResult(score, "; ".join(feedback_parts), metadata)
    
    def get_strategy_name(self) -> str:
        return "Rule-Based Evaluation"

# Concrete Strategy 2: Peer Review Evaluation
class PeerReviewEvaluation(EvaluationStrategy):
    """Simulates peer review evaluation process"""
    
    def __init__(self, num_reviewers: int = 3):
        self.num_reviewers = num_reviewers
    
    def evaluate(self, submission: Submission) -> EvaluationResult:
        print(f"  [Peer Review] Evaluating '{submission.title}' with {self.num_reviewers} reviewers...")
        time.sleep(3.0)  # Simulate expensive operation
        
        # Simulate multiple reviewers with different perspectives
        scores = []
        feedbacks = []
        
        for i in range(self.num_reviewers):
            # Each reviewer focuses on different aspects
            if i == 0:  # Methodology reviewer
                method_score = min(100, len(submission.content) / 30)
                scores.append(method_score)
                feedbacks.append("Methodology: Strong approach")
            elif i == 1:  # Results reviewer
                results_score = min(100, len(submission.content.split()) / 20)
                scores.append(results_score)
                feedbacks.append("Results: Well-presented")
            else:  # Writing quality reviewer
                # Count sentences for writing quality
                sentence_count = submission.content.count('.') + submission.content.count('!') + submission.content.count('?')
                writing_score = min(100, sentence_count * 5)
                scores.append(writing_score)
                feedbacks.append("Writing: Clear and concise")
        
        # Calculate final score (weighted average)
        avg_score = sum(scores) / len(scores)
        
        # Add some randomness to simulate reviewer variance
        import random
        avg_score += random.uniform(-5, 5)
        avg_score = max(0, min(100, avg_score))
        
        metadata = {
            "strategy": "peer_review",
            "reviewers_count": self.num_reviewers,
            "individual_scores": [round(s, 1) for s in scores],
            "score_variance": round(max(scores) - min(scores), 1),
            "processing_time_ms": 3000
        }
        
        return EvaluationResult(avg_score, " | ".join(feedbacks), metadata)
    
    def get_strategy_name(self) -> str:
        return "Peer Review Evaluation"

# Concrete Strategy 3: ML-based Evaluation
class MLEvaluation(EvaluationStrategy):
    """Mock ML-based evaluation (most expensive)"""
    
    def __init__(self, model_name: str = "scibert-research-2024"):
        self.model_name = model_name
    
    def evaluate(self, submission: Submission) -> EvaluationResult:
        print(f"  [ML Model] Evaluating '{submission.title}' using {self.model_name}...")
        time.sleep(5.0)  # Simulate very expensive ML operation
        
        # Mock ML evaluation metrics
        content = submission.content.lower()
        
        # Complexity score based on vocabulary diversity
        unique_words = len(set(content.split()))
        total_words = len(content.split())
        lexical_diversity = unique_words / max(1, total_words)
        complexity_score = lexical_diversity * 70
        
        # Novelty score based on rare words
        common_words = {'the', 'and', 'of', 'to', 'in', 'a', 'is', 'that', 'for', 'it'}
        rare_word_count = sum(1 for word in content.split() if word not in common_words)
        novelty_score = min(100, rare_word_count / 10)
        
        # Technical term density
        tech_terms = {'algorithm', 'methodology', 'analysis', 'experiment', 'results', 
                     'conclusion', 'data', 'model', 'parameter', 'validation'}
        tech_count = sum(1 for term in tech_terms if term in content)
        technical_score = min(100, tech_count * 15)
        
        # Combine scores with weights
        ml_score = (
            complexity_score * 0.4 +
            novelty_score * 0.3 +
            technical_score * 0.3
        )
        
        ml_score = max(0, min(100, ml_score))
        
        feedback = (f"{self.model_name}: Complexity={complexity_score:.1f}, "
                   f"Novelty={novelty_score:.1f}, Technical={technical_score:.1f}")
        
        metadata = {
            "strategy": "ml_based",
            "model_used": self.model_name,
            "complexity_score": round(complexity_score, 1),
            "novelty_score": round(novelty_score, 1),
            "technical_score": round(technical_score, 1),
            "inference_time_ms": 5000
        }
        
        return EvaluationResult(ml_score, feedback, metadata)
    
    def get_strategy_name(self) -> str:
        return "ML-Based Evaluation"

# ==================== Decorator Pattern Implementation ====================

class EvaluationDecorator(EvaluationStrategy):
    """Base decorator class following the Decorator pattern"""
    
    def __init__(self, wrapped_evaluator: EvaluationStrategy):
        self._wrapped_evaluator = wrapped_evaluator
    
    def evaluate(self, submission: Submission) -> EvaluationResult:
        return self._wrapped_evaluator.evaluate(submission)
    
    def get_strategy_name(self) -> str:
        return self._wrapped_evaluator.get_strategy_name()

class CachingDecorator(EvaluationDecorator):
    """
    Decorator that adds caching functionality to expensive evaluations.
    This is the main implementation of the Decorator pattern for caching.
    """
    
    def __init__(self, wrapped_evaluator: EvaluationStrategy, cache_ttl: int = 3600):
        super().__init__(wrapped_evaluator)
        self.cache_ttl = cache_ttl  # Time-to-live in seconds (1 hour default)
        self._cache: Dict[str, tuple[EvaluationResult, float]] = {}
        self.cache_hits = 0
        self.cache_misses = 0
        print(f"  [Cache] Initialized with TTL: {cache_ttl}s")
    
    def _get_cache_key(self, submission: Submission) -> str:
        """Generate unique cache key from submission and strategy"""
        strategy_name = self.get_strategy_name().replace(" ", "_").lower()
        submission_hash = submission.get_hash()
        return f"{strategy_name}_{submission_hash}"
    
    def _is_cache_valid(self, timestamp: float) -> bool:
        """Check if cached result is still valid based on TTL"""
        current_time = time.time()
        age = current_time - timestamp
        return age < self.cache_ttl
    
    def evaluate(self, submission: Submission) -> EvaluationResult:
        cache_key = self._get_cache_key(submission)
        
        # Check cache first
        if cache_key in self._cache:
            cached_result, cache_timestamp = self._cache[cache_key]
            
            if self._is_cache_valid(cache_timestamp):
                # Cache hit with valid TTL
                self.cache_hits += 1
                print(f"  [Cache] ✓ HIT for '{submission.title}' (saved {time.time() - cache_timestamp:.1f}s)")
                
                # Return cached result with cache indicator
                result = EvaluationResult(
                    cached_result.score,
                    cached_result.feedback + " [CACHED]",
                    {**cached_result.metadata, "cached": True, "cache_hit": True}
                )
                result.is_cached = True
                result.timestamp = time.time()
                return result
        
        # Cache miss or expired
        self.cache_misses += 1
        print(f"  [Cache] ✗ MISS for '{submission.title}'")
        
        # Perform actual evaluation (expensive operation)
        start_time = time.time()
        result = self._wrapped_evaluator.evaluate(submission)
        evaluation_time = time.time() - start_time
        
        # Store in cache
        self._cache[cache_key] = (result, time.time())
        
        # Add performance metadata
        result.metadata["evaluation_time_ms"] = round(evaluation_time * 1000, 1)
        result.metadata["cache_miss"] = True
        
        print(f"  [Cache] Stored result for '{submission.title}' (took {evaluation_time:.2f}s)")
        return result
    
    def clear_cache(self):
        """Clear all cached results"""
        self._cache.clear()
        self.cache_hits = 0
        self.cache_misses = 0
        print("  [Cache] Cleared all cached results")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "total_requests": total_requests,
            "hit_rate_percent": round(hit_rate, 1),
            "cache_size": len(self._cache),
            "cache_ttl": self.cache_ttl
        }
    
    def get_cached_keys(self) -> List[str]:
        """Get list of all cache keys"""
        return list(self._cache.keys())

class LoggingDecorator(EvaluationDecorator):
    """Additional decorator for logging (shows decorator chaining)"""
    
    def __init__(self, wrapped_evaluator: EvaluationStrategy):
        super().__init__(wrapped_evaluator)
        self.evaluation_log = []
    
    def evaluate(self, submission: Submission) -> EvaluationResult:
        start_time = time.time()
        
        print(f"  [Logging] Starting evaluation of '{submission.title}'")
        result = self._wrapped_evaluator.evaluate(submission)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Log the evaluation
        log_entry = {
            "submission_id": submission.submission_id,
            "title": submission.title,
            "strategy": self.get_strategy_name(),
            "score": result.score,
            "duration_seconds": round(duration, 2),
            "timestamp": datetime.now().isoformat(),
            "cached": result.is_cached
        }
        self.evaluation_log.append(log_entry)
        
        print(f"  [Logging] Completed in {duration:.2f}s, Score: {result.score:.1f}")
        return result
    
    def get_logs(self) -> List[Dict]:
        """Get all evaluation logs"""
        return self.evaluation_log

# ==================== Demo and Example Usage ====================

def demonstrate_decorator_pattern():
    """Demonstrate the Decorator pattern with caching functionality"""
    
    print("\n" + "="*60)
    print("SURMS - DECORATOR PATTERN DEMONSTRATION")
    print("Caching Expensive Evaluation Operations")
    print("="*60 + "\n")
    
    # Create sample submissions
    submissions = [
        Submission("S001", "Deep Learning in Medical Imaging", 
                  "Abstract: This paper explores... Methodology: We used... Results: Our approach achieved...", 
                  "Dr. Alice Chen"),
        Submission("S002", "Quantum Computing Algorithms", 
                  "Abstract: Quantum computing offers... We present a new algorithm... Results show improvement... Conclusion: Future work...", 
                  "Prof. Bob Smith"),
        Submission("S003", "Sustainable Energy Systems", 
                  "Methodology: Our study analyzed... Data was collected from... Results indicate that... References: [1]... [2]...", 
                  "Dr. Carol Johnson"),
    ]
    
    # Create base evaluator (expensive ML evaluation)
    print("1. Creating base ML evaluator (expensive operation ~5 seconds):")
    ml_evaluator = MLEvaluation("scibert-research-v2")
    
    # Wrap with Caching Decorator
    print("\n2. Wrapping with CachingDecorator:")
    cached_ml_evaluator = CachingDecorator(ml_evaluator, cache_ttl=30)  # 30s TTL for demo
    
    # Wrap with Logging Decorator (decorator chaining)
    print("3. Adding LoggingDecorator (decorator chaining):")
    logged_cached_evaluator = LoggingDecorator(cached_ml_evaluator)
    
    print("\n" + "-"*60)
    print("FIRST ROUND: All evaluations (should be cache misses)")
    print("-"*60)
    
    # First evaluation round (cache misses)
    for i, submission in enumerate(submissions, 1):
        print(f"\n--- Evaluation {i}: {submission.title} ---")
        result = logged_cached_evaluator.evaluate(submission)
        print(f"Result: {result}")
    
    print("\n" + "-"*60)
    print("SECOND ROUND: Same submissions (should be cache hits)")
    print("-"*60)
    
    # Second evaluation round (cache hits - much faster!)
    for i, submission in enumerate(submissions, 1):
        print(f"\n--- Re-evaluation {i}: {submission.title} ---")
        result = logged_cached_evaluator.evaluate(submission)
        print(f"Result: {result}")
    
    print("\n" + "-"*60)
    print("THIRD ROUND: New submission (cache miss)")
    print("-"*60)
    
    # New submission (cache miss)
    new_submission = Submission("S004", "Blockchain for Supply Chain", 
                               "Abstract: Blockchain technology... Methodology: Smart contracts... Results: Efficiency improved by 40%...", 
                               "Dr. David Wilson")
    print(f"\n--- New submission: {new_submission.title} ---")
    result = logged_cached_evaluator.evaluate(new_submission)
    print(f"Result: {result}")
    
    # Demonstrate different evaluators with caching
    print("\n" + "-"*60)
    print("DEMONSTRATING DIFFERENT EVALUATORS WITH CACHING")
    print("-"*60)
    
    evaluators = [
        ("Rule-Based", CachingDecorator(RuleBasedEvaluation(), cache_ttl=1800)),
        ("Peer Review", CachingDecorator(PeerReviewEvaluation(num_reviewers=2), cache_ttl=1800)),
        ("ML-Based", CachingDecorator(MLEvaluation(), cache_ttl=1800)),
    ]
    
    test_submission = submissions[0]
    
    for evaluator_name, evaluator in evaluators:
        print(f"\n--- Testing {evaluator_name} Evaluator ---")
        
        # First call
        print(f"First evaluation:")
        start = time.time()
        result1 = evaluator.evaluate(test_submission)
        time1 = time.time() - start
        
        # Second call (should be cached)
        print(f"\nSecond evaluation (should be cached):")
        start = time.time()
        result2 = evaluator.evaluate(test_submission)
        time2 = time.time() - start
        
        speedup = (time1 - time2) / time1 * 100
        print(f"Performance: {time1:.2f}s → {time2:.2f}s ({speedup:.0f}% faster)")
        print(f"Cache stats: {evaluator.get_cache_stats()}")
    
    # Show final statistics
    print("\n" + "="*60)
    print("FINAL CACHE STATISTICS")
    print("="*60)
    
    stats = cached_ml_evaluator.get_cache_stats()
    for key, value in stats.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    # Show logs from logging decorator
    print(f"\nTotal evaluations logged: {len(logged_cached_evaluator.get_logs())}")
    
    print("\n" + "="*60)
    print("DECORATOR PATTERN EXPLANATION")
    print("="*60)
    
    print("""
    HOW THE DECORATOR PATTERN WORKS:
    
    1. Base Component: EvaluationStrategy (interface)
    2. Concrete Components: RuleBasedEvaluation, PeerReviewEvaluation, MLEvaluation
    3. Base Decorator: EvaluationDecorator (implements same interface)
    4. Concrete Decorators: 
       - CachingDecorator: Adds caching functionality
       - LoggingDecorator: Adds logging functionality
    
    Class Hierarchy:
        EvaluationStrategy (interface)
        ├── RuleBasedEvaluation (concrete)
        ├── PeerReviewEvaluation (concrete)
        ├── MLEvaluation (concrete)
        └── EvaluationDecorator (base decorator)
            ├── CachingDecorator (adds caching)
            └── LoggingDecorator (adds logging)
    
    Decorators can be chained:
        LoggingDecorator → CachingDecorator → MLEvaluation
    
    This follows the Open/Closed Principle - we can add new functionality
    without modifying existing classes.
    """)
    
    print("\n" + "="*60)
    print("PERFORMANCE IMPROVEMENT SUMMARY")
    print("="*60)
    
    print("""
    Without Caching:
    - ML Evaluation: ~5 seconds per submission
    - Peer Review: ~3 seconds per submission  
    - Rule-Based: ~1.5 seconds per submission
    
    With Caching:
    - First evaluation: Same as above (cache miss)
    - Subsequent evaluations: ~0.001 seconds (cache hit)
    - 99.9%+ performance improvement for repeated evaluations
    
    Real-world benefits in SURMS:
    1. Faster dashboard loading (cached evaluations)
    2. Reduced server load during peak times
    3. Cost savings on expensive ML API calls
    4. Better user experience (instant results)
    5. Scalability for high-traffic periods
    """)

if __name__ == "__main__":
    demonstrate_decorator_pattern()