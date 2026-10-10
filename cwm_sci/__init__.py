"""Causal World Model for Scientific Discovery (CWM-Sci).

A foundation model that learns causal laws from scientific literature and 
observational data with formal do-calculus proofs.

This module provides the core causal discovery and reasoning engine for 
scientific discovery, enabling the extraction of causal laws with formal
do-calculus proofs from observational data and scientific literature.
"""

from __future__ import annotations

__version__ = "0.1.0"
__author__ = "Kavy Makhesana"
__email__ = "kavymakhesana07@gmail.com"

__all__ = [
    "CausalWorldModel",
    "CausalDiscoveryEngine",
    "DoCalculusEngine",
    "CausalGraph",
    "CausalLaw",
    "ProofTree",
]

from cwm_sci.causal.discovery import CausalDiscoveryEngine
from cwm_sci.causal.graph import CausalGraph
from cwm_sci.causal.laws import CausalLaw
from cwm_sci.engine.calculus import DoCalculusEngine
from cwm_sci.engine.graph import CausalGraph as EngineCausalGraph
from cwm_sci.engine.discovery import CausalDiscoveryEngine
from cwm_sci.engine.calculus import DoCalculusEngine
from cwm_sci.models import CausalLaw, ProofTree, CausalGraph as ModelCausalGraph

__all__ = [
    "CausalDiscoveryEngine",
    "DoCalculusEngine",
    "CausalGraph",
    "CausalLaw",
    "ProofTree",
    "CausalWorldModel",
]

class CausalWorldModel:
    """Main entry point for the Causal World Model for Scientific Discovery.
    
    This class provides a unified interface for causal discovery, 
    do-calculus reasoning, and causal law extraction from scientific data.
    """
    
    def __init__(self, config: dict | None = None):
        self.config = config or {}
        self.discovery_engine = CausalDiscoveryEngine()
        self.calculus_engine = DoCalculusEngine()
        self.causal_graph = EngineCausalGraph()
    
    def discover_causal_laws(
        self, 
        data: "pd.DataFrame",
        domain_knowledge: dict | None = None
    ) -> list:
        """Discover causal laws from observational data.
        
        Args:
            data: Observational data as pandas DataFrame
            domain_knowledge: Optional domain knowledge constraints
            
        Returns:
            List of discovered causal laws with proof trees
        """
        # Implementation would go here
        pass
    
    def answer_counterfactual(
        self, 
        query: str,
        evidence: dict
    ) -> dict:
        """Answer counterfactual queries using do-calculus."""
        pass
    
    def validate_causal_claim(
        self, 
        claim: str,
        evidence: dict
    ) -> dict:
        """Validate a causal claim using do-calculus."""
        pass


# Re-export key classes for convenience
from cwm_sci.models import (
    CausalLaw,
    ProofTree,
    CausalGraph as ModelCausalGraph,
)

# For backward compatibility
CausalGraph = EngineCausalGraph
DoCalculusEngine = DoCalculusEngine
CausalDiscoveryEngine = CausalDiscoveryEngine
CausalLaw = CausalLaw
ProofTree = ProofTree