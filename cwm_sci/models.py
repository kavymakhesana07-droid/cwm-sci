"""Data models for the Causal World Model.

Defines core data structures for causal laws, proof trees, and causal graphs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, Field


class CausalDirection(Enum):
    """Direction of causal relationship."""
    DIRECTED = "directed"
    BIDIRECTIONAL = "bidirectional"
    CONFOUNDED = "confounded"
    UNKNOWN = "unknown"


class CausalStrength(Enum):
    """Strength of causal relationship."""
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    DEFINITIVE = "definitive"


class CausalMechanism(Enum):
    """Type of causal mechanism."""
    DIRECT = "direct"
    MEDIATED = "mediated"
    CONFOUNDED = "confounded"
    COLLIDER = "collider"
    MEDIATED_CONFOUNDED = "mediated_confounded"


@dataclass(slots=True)
class CausalEdge:
    """Represents a causal edge in the causal graph."""
    source: str
    target: str
    direction: CausalDirection = CausalDirection.DIRECTED
    strength: CausalStrength = CausalStrength.MODERATE
    mechanism: CausalMechanism = CausalMechanism.DIRECT
    confidence: float = 0.5
    evidence: list[str] = field(default_factory=list)
    do_calculus_proof: str | None = None
    backdoor_adjustment: list[str] | None = None
    frontdoor_adjustment: list[str] | None = None
    instrumental_variables: list[str] | None = None

    def __post_init__(self):
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0 and 1")


class CausalGraph:
    """Directed acyclic graph representing causal relationships.

    Nodes represent variables, edges represent causal relationships
    with associated do-calculus proofs and confidence scores.
    """

    def __init__(self):
        self.nodes: set[str] = set()
        self.edges: dict[tuple[str, str], CausalEdge] = {}
        self.confounders: dict[str, set[str]] = {}
        self.mediators: dict[tuple[str, str], list[str]] = {}
        self.colliders: set[tuple[str, str]] = set()

    def add_node(self, node: str) -> None:
        """Add a node to the causal graph."""
        self.nodes.add(node)

    def add_edge(self, edge: CausalEdge) -> None:
        """Add a causal edge to the graph."""
        self.nodes.add(edge.source)
        self.nodes.add(edge.target)
        self.edges[(edge.source, edge.target)] = edge

    def get_parents(self, node: str) -> list[str]:
        """Get direct causes (parents) of a node."""
        return [src for (src, tgt) in self.edges.keys() if tgt == node]

    def get_children(self, node: str) -> list[str]:
        """Get direct effects (children) of a node."""
        return [tgt for (src, tgt) in self.edges.keys() if src == node]

    def get_ancestors(self, node: str) -> set[str]:
        """Get all ancestors of a node (transitive closure)."""
        ancestors = set()
        to_visit = self.get_parents(node)
        while to_visit:
            parent = to_visit.pop()
            if parent not in ancestors:
                ancestors.add(parent)
                to_visit.extend(self.get_parents(parent))
        return ancestors

    def get_descendants(self, node: str) -> set[str]:
        """Get all descendants of a node (transitive closure)."""
        descendants = set()
        to_visit = self.get_children(node)
        while to_visit:
            child = to_visit.pop()
            if child not in descendants:
                descendants.add(child)
                to_visit.extend(self.get_children(child))
        return descendants

    def get_children(self, node: str) -> list[str]:
        return [tgt for (src, tgt) in self.edges.keys() if src == node]

    def get_parents(self, node: str) -> list[str]:
        return [src for (src, tgt) in self.edges.keys() if tgt == node]

    def get_children(self, node: str) -> list[str]:
        return [tgt for (src, tgt) in self.edges.keys() if src == node]

    def get_parents(self, node: str) -> list[str]:
        return [src for (src, tgt) in self.edges.keys() if tgt == node]


class CausalLaw:
    """Represents a discovered causal law with formal proof."""

    def __init__(
        self,
        cause: str,
        effect: str,
        mechanism: str = "direct",
        strength: float = 0.5,
        confidence: float = 0.5,
        evidence: list[str] | None = None,
        proof_tree: dict | None = None,
        do_calculus_proof: str | None = None,
        backdoor_adjustment: list[str] | None = None,
        frontdoor_adjustment: list[str] | None = None,
        instrumental_variables: list[str] | None = None,
        metadata: dict | None = None,
    ):
        self.id = uuid4()
        self.cause = cause
        self.effect = effect
        self.mechanism = mechanism
        self.strength = strength
        self.confidence = confidence
        self.evidence = evidence or []
        self.proof_tree = proof_tree
        self.do_calculus_proof = do_calculus_proof
        self.backdoor_adjustment = backdoor_adjustment or []
        self.frontdoor_adjustment = frontdoor_adjustment or []
        self.instrumental_variables = instrumental_variables or []
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.version = "0.1.0"

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "cause": self.cause,
            "effect": self.effect,
            "mechanism": self.mechanism,
            "strength": self.strength,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "proof_tree": self.proof_tree,
            "do_calculus_proof": self.do_calculus_proof,
            "backdoor_adjustment": self.backdoor_adjustment,
            "frontdoor_adjustment": self.frontdoor_adjustment,
            "instrumental_variables": self.instrumental_variables,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CausalLaw":
        law = cls(
            cause=data["cause"],
            effect=data["effect"],
            mechanism=data.get("mechanism", "direct"),
            strength=data.get("strength", 0.5),
            confidence=data.get("confidence", 0.5),
            evidence=data.get("evidence", []),
            proof_tree=data.get("proof_tree"),
            do_calculus_proof=data.get("do_calculus_proof"),
            backdoor_adjustment=data.get("backdoor_adjustment", []),
            frontdoor_adjustment=data.get("frontdoor_adjustment", []),
            instrumental_variables=data.get("instrumental_variables", []),
            metadata=data.get("metadata", {}),
        )
        law.id = UUID(data["id"])
        law.created_at = datetime.fromisoformat(data["created_at"])
        law.updated_at = datetime.fromisoformat(data["updated_at"])
        law.version = data.get("version", "0.1.0")
        return law


class ProofTree:
    """Proof tree for causal claims using do-calculus."""

    def __init__(
        self,
        conclusion: str,
        premises: list[str] | None = None,
        rules_applied: list[str] | None = None,
        subproofs: list["ProofTree"] | None = None,
        confidence: float = 1.0,
    ):
        self.id = uuid4()
        self.conclusion = conclusion
        self.premises = premises or []
        self.rules_applied = rules_applied or []
        self.subproofs = subproofs or []
        self.confidence = confidence
        self.created_at = datetime.now()

    def add_premise(self, premise: str) -> None:
        self.premises.append(premise)

    def add_rule(self, rule: str) -> None:
        self.rules_applied.append(rule)

    def add_subproof(self, subproof: "ProofTree") -> None:
        self.subproofs.append(subproof)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "conclusion": self.conclusion,
            "premises": self.premises,
            "rules_applied": self.rules_applied,
            "subproofs": [sp.to_dict() for sp in self.subproofs],
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat(),
        }

    def __str__(self) -> str:
        return f"ProofTree(conclusion={self.conclusion}, confidence={self.confidence})"


class CausalLaw:
    """Represents a discovered causal law with formal proof."""

    def __init__(
        self,
        cause: str,
        effect: str,
        mechanism: str = "direct",
        strength: float = 0.5,
        confidence: float = 0.5,
        evidence: list[str] | None = None,
        proof_tree: dict | None = None,
        do_calculus_proof: str | None = None,
        backdoor_adjustment: list[str] | None = None,
        frontdoor_adjustment: list[str] | None = None,
        instrumental_variables: list[str] | None = None,
        metadata: dict | None = None,
    ):
        self.id = uuid4()
        self.cause = cause
        self.effect = effect
        self.mechanism = mechanism
        self.strength = strength
        self.confidence = confidence
        self.evidence = evidence or []
        self.proof_tree = proof_tree
        self.do_calculus_proof = do_calculus_proof
        self.backdoor_adjustment = backdoor_adjustment or []
        self.frontdoor_adjustment = frontdoor_adjustment or []
        self.instrumental_variables = instrumental_variables or []
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.version = "0.1.0"

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "cause": self.cause,
            "effect": self.effect,
            "mechanism": self.mechanism,
            "strength": self.strength,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "proof_tree": self.proof_tree,
            "do_calculus_proof": self.do_calculus_proof,
            "backdoor_adjustment": self.backdoor_adjustment,
            "frontdoor_adjustment": self.frontdoor_adjustment,
            "instrumental_variables": self.instrumental_variables,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CausalLaw":
        law = cls(
            cause=data["cause"],
            effect=data["effect"],
            mechanism=data.get("mechanism", "direct"),
            strength=data.get("strength", 0.5),
            confidence=data.get("confidence", 0.5),
            evidence=data.get("evidence", []),
            proof_tree=data.get("proof_tree"),
            do_calculus_proof=data.get("do_calculus_proof"),
            backdoor_adjustment=data.get("backdoor_adjustment", []),
            frontdoor_adjustment=data.get("frontdoor_adjustment", []),
            instrumental_variables=data.get("instrumental_variables", []),
            metadata=data.get("metadata", {}),
        )
        law.id = UUID(data["id"])
        law.created_at = datetime.fromisoformat(data["created_at"])
        law.updated_at = datetime.fromisoformat(data["updated_at"])
        law.version = data.get("version", "0.1.0")
        return law


class ProofTree:
    """Proof tree for causal claims using do-calculus."""

    def __init__(
        self,
        conclusion: str,
        premises: list[str] | None = None,
        rules_applied: list[str] | None = None,
        subproofs: list["ProofTree"] | None = None,
        confidence: float = 1.0,
    ):
        self.id = uuid4()
        self.conclusion = conclusion
        self.premises = premises or []
        self.rules_applied = rules_applied or []
        self.subproofs = subproofs or []
        self.confidence = confidence
        self.created_at = datetime.now()

    def add_premise(self, premise: str) -> None:
        self.premises.append(premise)

    def add_rule(self, rule: str) -> None:
        self.rules_applied.append(rule)

    def add_subproof(self, subproof: "ProofTree") -> None:
        self.subproofs.append(subproof)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "conclusion": self.conclusion,
            "premises": self.premises,
            "rules_applied": self.rules_applied,
            "subproofs": [sp.to_dict() for sp in self.subproofs],
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat(),
        }

    def __str__(self) -> str:
        return f"ProofTree(conclusion={self.conclusion}, confidence={self.confidence})"