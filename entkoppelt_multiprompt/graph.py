from typing import Any, Dict, Callable

from entkoppelt_multiprompt.nodes.input_ingest import IngestSpec
from entkoppelt_multiprompt.nodes.parser_spec import ParseSpec
from entkoppelt_multiprompt.nodes.prompt_builder import PromptBuilder
from entkoppelt_multiprompt.nodes.semantic_from_prompt import SemanticFromPrompt
from entkoppelt_multiprompt.nodes.active_text_filter import ActiveTextFilter
from entkoppelt_multiprompt.nodes.semantic_heuristic_lite import SemanticHeuristicLite
from entkoppelt_multiprompt.nodes.semantic_merge import SemanticMerger
from entkoppelt_multiprompt.nodes.prompt_policy_validator import PromptPolicyValidator
from entkoppelt_multiprompt.nodes.output_assembler import OutputAssembler


def build_app() -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """Baut eine einfache, sequentielle Ausfuehrung des Graphen.

    Rueckgabe ist eine Callable, die einen State (dict) entgegennimmt und
    das finale Ergebnis (dict) zurueckgibt.
    """

    def app(state: Dict[str, Any]) -> Dict[str, Any]:
        if state is None:
            state = {}
        # Nodes sequentiell ausfuehren
        state = IngestSpec(state)
        state = ParseSpec(state)
        state = ActiveTextFilter(state)
        state = PromptBuilder(state)
        state = SemanticFromPrompt(state)
        state = SemanticHeuristicLite(state)
        state = SemanticMerger(state)
        state = PromptPolicyValidator(state)
        out = OutputAssembler(state)
        return out

    return app


