"""FastAPI REST API for Causal World Model."""

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from cwm_sci.causal.discovery import CausalDiscoveryEngine, DiscoveryConfig
from cwm_sci.engine.calculus import DoCalculusEngine, CounterfactualQuery, CounterfactualResult
from cwm_sci.engine.graph import CausalGraphEngine
from cwm_sci.models import CausalLaw, ProofTree, CausalGraph

logger = logging.getLogger(__name__)

# Global state (in production, use proper dependency injection)
discovery_engine: Optional["CausalDiscoveryEngine"] = None
calculus_engine: Optional[DoCalculusEngine] = None
graph_engine: Optional[Any] = None


class DiscoverRequest(BaseModel):
    data_path: str
    algorithm: str = "pc"
    significance: float = 0.05
    max_parents: int = 5
    domain_knowledge: Optional[dict] = None


class DiscoverResponse(BaseModel):
    nodes: int
    edges: int
    graph_path: Optional[str] = None


class CounterfactualRequest(BaseModel):
    intervention: dict[str, Any]
    outcome: str
    evidence: dict[str, Any] = {}
    confidence_threshold: float = 0.95


class CounterfactualResponse(BaseModel):
    query_id: str
    intervention: dict[str, Any]
    outcome: str
    probability: float
    confidence: float
    proof_tree: Optional[dict] = None
    assumptions: list[str] = []


class CounterfactualRequest(BaseModel):
    intervention: dict[str, Any]
    outcome: str
    evidence: dict[str, Any] = {}
    confidence_threshold: float = 0.95


class CounterfactualResponse(BaseModel):
    query_id: str
    intervention: dict[str, Any]
    outcome: str
    probability: float
    confidence: float
    proof_tree: Optional[dict] = None
    assumptions: list[str] = []


class CounterfactualRequest(BaseModel):
    intervention: dict[str, Any]
    outcome: str
    evidence: dict[str, Any] = {}
    confidence_threshold: float = 0.95


class CounterfactualResponse(BaseModel):
    query_id: str
    intervention: dict[str, Any]
    outcome: str
    probability: float
    confidence: float
    proof_tree: Optional[dict] = None
    assumptions: list[str] = []


class CounterfactualRequest(BaseModel):
    intervention: dict[str, Any]
    outcome: str
    evidence: dict[str, Any] = {}
    confidence_threshold: float = 0.95


class CounterfactualResponse(BaseModel):
    query_id: str
    intervention: dict[str, Any]
    outcome: str
    probability: float
    confidence: float
    proof_tree: Optional[dict] = None
    assumptions: list[str] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global discovery_engine, calculus_engine, graph_engine

    logger.info("Initializing CWM-Sci services...")

    # Initialize engines
    discovery_engine = CausalDiscoveryEngine(DiscoveryConfig(
        algorithm="pc",
        significance_level=0.05,
        max_parents=5,
    ))

    calculus_engine = DoCalculusEngine(None)  # Graph loaded on demand

    logger.info("CWM-Sci services initialized")
    yield
    # Shutdown
    logger.info("Shutting down CWM-Sci services...")


app = FastAPI(
    title="Causal World Model for Scientific Discovery (CWM-Sci)",
    description="Foundation model for learning causal laws from scientific data with formal do-calculus proofs",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "service": "cwm-sci"
    }


@app.post("/api/v1/discover", response_model=DiscoverResponse)
async def discover_causal_structure(request: DiscoverRequest):
    """Discover causal structure from observational data."""
    engine = CausalDiscoveryEngine(DiscoveryConfig(
        algorithm=request.algorithm,
        significance_level=request.significance,
        max_parents=request.max_parents,
    ))

    # Load data
    import pandas as pd
    data = pd.read_csv(request.data_path)

    graph = await discovery_engine.discover(
        data=pd.read_csv(request.data_path),
        algorithm=request.algorithm,
    )

    # Save graph
    import networkx as nx
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(suffix=".graphml", delete=False) as tmp:
        graph_path = tmp.name
        nx.write_graphml(graph, graph_path)

    return DiscoverResponse(
        nodes=graph.number_of_nodes(),
        edges=graph.number_of_edges(),
        graph_path=graph_path,
    )


@app.post("/api/v1/counterfactual", response_model=CounterfactualResponse)
async def compute_counterfactual(request: CounterfactualRequest):
    """Compute counterfactual probability P(Y | do(X), evidence)."""
    engine = DoCalculusEngine(None)  # Graph loaded on demand

    query = CounterfactualQuery(
        intervention=request.intervention,
        outcome=request.outcome,
        evidence=request.evidence,
        confidence_threshold=request.confidence_threshold,
    )

    result = engine.compute_counterfactual(query)

    return CounterfactualResponse(
        query_id=result.query_id,
        intervention=request.intervention,
        outcome=request.outcome,
        probability=result.probability,
        confidence=result.confidence,
        proof_tree=result.proof_tree.to_dict() if result.proof_tree else None,
        assumptions=result.assumptions,
    )


@app.get("/api/v1/models")
async def list_models():
    """List registered models."""
    return {"models": []}


@app.get("/api/v1/models/{model_name}")
async def get_model(model_name: str):
    """Get model information."""
    return {"name": model_name, "status": "not_found"}


@app.post("/api/v1/models")
async def register_model(model: dict):
    """Register a new model."""
    return {"status": "registered", "model": model}


@app.get("/api/v1/graph")
async def get_graph():
    """Get current causal graph."""
    return {"nodes": [], "edges": []}


@app.post("/api/v1/graph")
async def update_graph(graph: dict):
    """Update causal graph."""
    return {"status": "updated"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("cwm_sci.api:app", host="0.0.0.0", port=8080, reload=True)