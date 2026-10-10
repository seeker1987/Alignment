"""
CARA Invariant Auto-Synthesizer.
Now upgraded with v0.4 Grounded Binding & Provenance:
- Extracts latent intent and strictly grounds Validity Invariants in prompt source spans.
- Enforces target_fields tracking to eliminate Assumption Hallucination and Decoy False Halts.
"""

from typing import Dict, List, Any, Optional, Tuple, Callable
import re
from .core import ValidityInvariant, GoalContextBinding

class SynthesizedInvariantSpec:
    def __init__(
        self,
        id_str: str,
        name: str,
        category: str,
        description: str,
        predicate_code: str,
        predicate_func: Callable[[Dict[str, Any]], bool],
        source_span: str = "",
        target_fields: Optional[List[str]] = None
    ):
        self.id = id_str
        self.name = name
        self.category = category  # 'ETHICAL' or 'VALIDITY'
        self.description = description
        self.predicate_code = predicate_code
        self.predicate_func = predicate_func
        self.source_span = source_span
        self.target_fields = target_fields or []

    def to_validity_invariant(self) -> ValidityInvariant:
        return ValidityInvariant(
            id_str=self.id,
            name=self.name,
            predicate=self.predicate_func,
            description=self.description,
            source_span=self.source_span,
            target_fields=self.target_fields
        )

class InvariantSynthesizer:
    """
    Automated generation of runtime invariants with v0.4 Grounded Provenance.
    """
    
    DOMAINS = {
        "database": {
            "keywords": ["database", "sql", "migration", "table", "postgres", "mysql", "schema"],
            "invariants": [
                ("V_DB_REPLICA_LAG", "Max Replication Lag", "VALIDITY", "Replica lag must not exceed 2.0s during writes",
                 "lambda s: s.get('replica_lag_sec', 0) <= 2.0", lambda s: s.get('replica_lag_sec', 0) <= 2.0,
                 ["replica_lag_sec"]),
                ("V_DB_LOCK_TIMEOUT", "Lock Contention Guard", "VALIDITY", "Lock wait queue must remain below 10 concurrent threads",
                 "lambda s: s.get('lock_wait_queue', 0) <= 10", lambda s: s.get('lock_wait_queue', 0) <= 10,
                 ["lock_wait_queue"]),
                ("E_DB_NO_DROP_PROD", "Production Data Preservation", "ETHICAL", "Destructive drop commands strictly barred without backup confirmation in production",
                 "lambda s: not (s.get('is_production', False) and not s.get('backup_verified', False))",
                 lambda s: not (s.get('is_production', False) and not s.get('backup_verified', False)),
                 ["is_production", "backup_verified"])
            ]
        },
        "financial": {
            "keywords": ["trade", "financial", "pricing", "budget", "cost", "billing", "payment", "refund"],
            "invariants": [
                ("V_FIN_MAX_SPEND", "Budget Ceiling", "VALIDITY", "Total transaction spend must not exceed allocated budget ceiling",
                 "lambda s: s.get('total_cost', 0) <= s.get('budget_limit', 1000.0)",
                 lambda s: s.get('total_cost', 0) <= s.get('budget_limit', 1000.0),
                 ["total_cost", "budget_limit"]),
                ("V_FIN_PRICE_DRIFT", "Slippage / Price Drift Guard", "VALIDITY", "Price change between quote and execution must remain within 5%",
                 "lambda s: abs(s.get('price_drift_pct', 0)) <= 5.0",
                 lambda s: abs(s.get('price_drift_pct', 0)) <= 5.0,
                 ["price_drift_pct"]),
                ("E_FIN_NO_UNAUTHORIZED_TRANSFER", "Transfer Authorization", "ETHICAL", "Transfers exceeding $500 require verified dual authorization",
                 "lambda s: not (s.get('transfer_amount', 0) > 500 and not s.get('dual_auth', False))",
                 lambda s: not (s.get('transfer_amount', 0) > 500 and not s.get('dual_auth', False)),
                 ["transfer_amount", "dual_auth"])
            ]
        },
        "infrastructure": {
            "keywords": ["cluster", "cloud", "server", "vm", "cpu", "datacenter", "power", "kubernetes"],
            "invariants": [
                ("V_INFRA_CPU_HEADROOM", "Thermal & CPU Headroom", "VALIDITY", "Cluster average CPU must not exceed 90%",
                 "lambda s: s.get('cpu_utilization_pct', 0) <= 90.0",
                 lambda s: s.get('cpu_utilization_pct', 0) <= 90.0,
                 ["cpu_utilization_pct"]),
                ("V_INFRA_ACTIVE_WORKLOAD", "Drain Workload Protection", "VALIDITY", "Nodes cannot power off while active user jobs > 0",
                 "lambda s: not (s.get('powering_off', False) and s.get('active_jobs', 0) > 0)",
                 lambda s: not (s.get('powering_off', False) and s.get('active_jobs', 0) > 0),
                 ["powering_off", "active_jobs"]),
                ("E_INFRA_ROOT_ACCESS_BOUNDARY", "Privilege Escalation Bar", "ETHICAL", "Automated workloads barred from generating temporary root credentials",
                 "lambda s: not s.get('requesting_root_escalation', False)",
                 lambda s: not s.get('requesting_root_escalation', False),
                 ["requesting_root_escalation"])
            ]
        },
        "healthcare": {
            "keywords": ["patient", "clinical", "medication", "titration", "dose", "icu", "creatinine", "vital"],
            "invariants": [
                ("V_HEALTH_RENAL", "Renal Safety Guard", "VALIDITY", "Serum creatinine must not exceed 2.2 mg/dL",
                 "lambda s: s.get('creatinine', 1.0) <= 2.2",
                 lambda s: s.get('creatinine', 1.0) <= 2.2,
                 ["creatinine"]),
                ("V_HEALTH_BP_FLOOR", "Hemodynamic Floor", "VALIDITY", "Mean Arterial Pressure (MAP) must remain above 60 mmHg",
                 "lambda s: s.get('map_mmhg', 70) >= 60.0",
                 lambda s: s.get('map_mmhg', 70) >= 60.0,
                 ["map_mmhg"]),
                ("E_HEALTH_PHYSICIAN_OVERRIDE", "Human Clinical Authority", "ETHICAL", "Agent must immediately yield authority upon physician flag",
                 "lambda s: not s.get('physician_override_active', False)",
                 lambda s: not s.get('physician_override_active', False),
                 ["physician_override_active"])
            ]
        }
    }

    @classmethod
    def synthesize(cls, goal: str, context_desc: str = "") -> Tuple[str, List[SynthesizedInvariantSpec], List[SynthesizedInvariantSpec]]:
        combined_text = f"{goal} {context_desc}".lower()
        latent_purpose = f"Execute '{goal}' while strictly safeguarding system invariants, data integrity, and stakeholder boundaries."
        
        validity_specs: List[SynthesizedInvariantSpec] = []
        ethical_specs: List[SynthesizedInvariantSpec] = []
        
        matched = False
        for domain_name, data in cls.DOMAINS.items():
            matched_keywords = [k for k in data["keywords"] if k in combined_text]
            if matched_keywords:
                matched = True
                matched_span = matched_keywords[0]
                for inv_tuple in data["invariants"]:
                    spec = SynthesizedInvariantSpec(
                        id_str=inv_tuple[0],
                        name=inv_tuple[1],
                        category=inv_tuple[2],
                        description=inv_tuple[3],
                        predicate_code=inv_tuple[4],
                        predicate_func=inv_tuple[5],
                        source_span=matched_span,
                        target_fields=inv_tuple[6]
                    )
                    if spec.category == "ETHICAL":
                        ethical_specs.append(spec)
                    else:
                        validity_specs.append(spec)
                        
        if not matched or len(validity_specs) == 0:
            validity_specs.append(
                SynthesizedInvariantSpec(
                    id_str="V_GENERIC_ERROR_RATE",
                    name="Error Rate Ceiling",
                    category="VALIDITY",
                    description="Execution halted if consecutive failure count exceeds 3",
                    predicate_code="lambda s: s.get('consecutive_errors', 0) <= 3",
                    predicate_func=lambda s: s.get('consecutive_errors', 0) <= 3,
                    source_span=goal[:20],
                    target_fields=["consecutive_errors"]
                )
            )
            ethical_specs.append(
                SynthesizedInvariantSpec(
                    id_str="E_GENERIC_SAFETY_HALT",
                    name="Operator Emergency Stop",
                    category="ETHICAL",
                    description="Execution barred if operator emergency stop is triggered",
                    predicate_code="lambda s: not s.get('emergency_stop', False)",
                    predicate_func=lambda s: not s.get('emergency_stop', False),
                    source_span=goal[:20],
                    target_fields=["emergency_stop"]
                )
            )

        return latent_purpose, validity_specs, ethical_specs

    @classmethod
    def create_binding(cls, goal: str, context_desc: str = "") -> GoalContextBinding:
        latent_purpose, v_specs, e_specs = cls.synthesize(goal, context_desc)
        v_invariants = [s.to_validity_invariant() for s in v_specs]
        e_invariants = [s.to_validity_invariant() for s in e_specs]
        
        return GoalContextBinding(
            goal=goal,
            latent_purpose=latent_purpose,
            invariants=v_invariants,
            ethical_invariants=e_invariants,
            enforce_grounding=True
        )
