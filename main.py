from orchestrator import OrchestratorCore
from orchestrator.cli.main import app as core_cli
from orchestrator.settings import AppSettings

import products  # noqa: F401  Side-effects
import workflows  # noqa: F401  Side-effects
import schedules

app = OrchestratorCore(base_settings=AppSettings())

if __name__ == "__main__":
    core_cli()
