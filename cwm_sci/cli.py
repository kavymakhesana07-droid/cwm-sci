"""CLI interface for Causal World Model."""

from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn

from cwm_sci.causal.discovery import CausalDiscoveryEngine, DiscoveryConfig
from cwm_sci.engine.calculus import DoCalculusEngine, CounterfactualQuery
from cwm_sci.engine.graph import CausalGraphEngine
from cwm_sci.models import CausalGraph, CausalLaw

app = typer.Typer(help="Causal World Model for Scientific Discovery (CWM-Sci)")
console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger(__name__)


@app.command()
def discover(
    data_path: str = typer.Argument(..., help="Path to CSV data file"),
    algorithm: str = typer.Option("pc", help="Discovery algorithm: pc, ges, notears"),
    output: Optional[str] = typer.Option(None, help="Output graph file (GraphML)"),
    significance: float = 0.05,
    max_parents: int = 5,
):
    """Discover causal structure from observational data."""
    console = Console()

    async def _discover():
        config = DiscoveryConfig(
            algorithm=algorithm,
            significance_level=significance,
            max_parents=5,
        )

        engine = CausalDiscoveryEngine(DiscoveryConfig(algorithm=algorithm))
        # Load data
        import pandas as pd
        data = pd.read_csv(data_path)

        graph = await engine.discover(data, algorithm=algorithm)

        console.print(f"[green]Discovered graph with {len(graph.nodes())} nodes, {graph.number_of_edges()} edges[/green]")

        if output:
            import networkx as nx
            nx.write_graphml(graph, output)
            console.print(f"[green]Graph saved to {output}[/green]")

    asyncio.run(_discover())


@app.command()
def reason(
    query: str = typer.Argument(..., help="Counterfactual query (e.g., 'What if we block IP X?')"),
    data: Optional[str] = None,
    model: str = "deep",
):
    """Answer counterfactual queries using do-calculus."""
    console = Console()

    async def _reason():
        # Load causal graph
        graph = None  # Would load from file/model registry

        engine = DoCalculusEngine(None)
        query_obj = CounterfactualQuery(
            intervention={"action": query},
            outcome="outcome",
        )

        result = engine.compute_counterfactual(query)

        console.print(f"[green]Counterfactual result: {result.probability:.3f}[/green]")

    asyncio.run(_reason())


@app.command()
def train(
    data_path: str = typer.Argument(..., help="Path to training data"),
    model_type: str = typer.Option("deep", help="Model type: deep, xgboost, fast"),
    output: str = typer.Option(..., help="Output model path"),
    epochs: int = 50,
    batch_size: int = 256,
):
    """Train a causal model."""
    console = Console()
    console.print(f"[yellow]Training {model_type} model on {data}...[/yellow]")
    # Implementation would go here


@app.command()
def serve(
    host: str = "0.0.0.0",
    port: int = 8080,
    model_path: Optional[str] = None,
):
    """Start the CWM-Sci API server."""
    import uvicorn
    from cwm_sci.api import app

    uvicorn.run("cwm_sci.api:app", host=host, port=port, reload=True)


@app.command()
def validate(
    graph_path: str = typer.Argument(..., help="Path to graph file (GraphML)"),
):
    """Validate a causal graph structure."""
    import networkx as nx
    from cwm_sci.engine.graph import compute_graph_metrics

    graph = nx.read_graphml(graph_path)
    metrics = compute_graph_metrics(nx.read_graphml(graph_path))

    console.print(f"[green]Graph validation results:[/green]")
    for key, value in metrics.__dict__.items():
        console.print(f"  {key}: {value}")


@app.command()
def discover(
    data_path: str = typer.Argument(..., help="Path to CSV data file"),
    algorithm: str = typer.Option("pc", help="Discovery algorithm: pc, ges, notears"),
    output: str = typer.Option(None, help="Output graph file (GraphML)"),
    significance: float = 0.05,
    max_parents: int = 5,
):
    """Discover causal structure from observational data."""
    import asyncio
    import pandas as pd
    import networkx as nx

    from cwm_sci.causal.discovery import CausalDiscoveryEngine, DiscoveryConfig

    async def _discover():
        config = DiscoveryConfig(
            algorithm=algorithm,
            significance_level=significance,
            max_parents=max_parents,
        )

        engine = CausalDiscoveryEngine(config)
        data = pd.read_csv(data_path)

        console.print(f"[cyan]Discovering causal structure with {algorithm}...[/cyan]")
        graph = await engine.discover(data, algorithm=algorithm)

        console.print(f"[green]Discovered graph with {len(graph.nodes())} nodes, {graph.number_of_edges()} edges[/green]")

        if output:
            import networkx as nx
            nx.write_graphml(graph, output)
            console.print(f"[green]Graph saved to {output}[/green]")

    asyncio.run(_discover())


if __name__ == "__main__":
    app()