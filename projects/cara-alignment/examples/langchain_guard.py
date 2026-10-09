#!/usr/bin/env python3
"""
Example: Protecting LangChain Agents with CARACallbackHandler.
Demonstrates intercepting an agent before a dangerous tool call when an invariant fails.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from cara import ValidityInvariant, GoalContextBinding
from cara.integrations import CARACallbackHandler

def main():
    print("=" * 70)
    print("CARA LangChain Integration Example")
    print("=" * 70)

    # 1. Shared environmental state
    environment = {
        "active_users": 1500,
        "database_replica_lag_sec": 4.5,
        "maintenance_window": False
    }

    # 2. Safety Invariant: Database write tools cannot run outside maintenance window if replica lag > 2s
    invariants = [
        ValidityInvariant(
            "V_REPLICA_LAG",
            "Database Replication Lag Safety",
            lambda s: s.get("maintenance_window", False) or s.get("database_replica_lag_sec", 0) <= 2.0
        )
    ]

    binding = GoalContextBinding(
        goal="Run schema migration",
        latent_purpose="Migrate customer table without causing replication lag spikes during peak hours",
        invariants=invariants
    )

    # 3. Initialize CARACallbackHandler with state getter
    cara_callback = CARACallbackHandler(binding, ambient_state_getter=lambda: environment)

    # 4. Simulate LangChain dispatching tool 'execute_ddl_migration'
    print("Agent attempts tool call: 'execute_ddl_migration'")
    print(f"Current Environment: {environment}")
    
    try:
        cara_callback.on_tool_start(
            serialized={"name": "execute_ddl_migration"},
            input_str="ALTER TABLE customers ADD COLUMN metadata JSON;"
        )
        print("Tool executed successfully.")
    except PermissionError as e:
        print("\n[SUCCESS] CARA Callback intercepted tool dispatch:")
        print(f"--> {e}")
        print("\nDatabase integrity protected from replica lag desynchronization.")

if __name__ == "__main__":
    main()
