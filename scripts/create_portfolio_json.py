"""Utility script for generating JSON payloads for Copperleaf's
PortfolioInvestment API within Matillion jobs.

This reads runtime variables injected by Matillion and builds the
portfolio investment JSON structure expected by the API.
"""

import json
from typing import Any, Dict, List


def _is_filled(value: Any) -> bool:
    """Return True if a variable has a meaningful value."""
    return value is not None


def make_json_from_table(table_data: List[Dict[str, Any]]) -> str:
    """Generate a JSON payload for PortfolioInvestment API."""
    portfolio_investments: List[Dict[str, Any]] = []

    for record in table_data:
        item: Dict[str, Any] = {}

        if _is_filled(record.get("INVESTMENTID")):
            item["InvestmentCode"] = record["INVESTMENTID"]

        # Default all requests to planning portfolio unless specified otherwise
        item["PortfolioIsPlanning"] = bool(record.get("PORTFOLIOISPLANNING", True))

        if _is_filled(record.get("PORTFOLIONAAM")):
            item["PortfolioName"] = record["PORTFOLIONAAM"]

        portfolio_investments.append(item)

    return json.dumps(portfolio_investments, indent=4)


# Dump all Matillion variables that start with ``jv_`` for debugging purposes
_globals = {name: globals()[name] for name in list(globals())}
for var_name in _globals:
    if var_name.startswith("jv_"):
        print(f"[{var_name} --> {_globals[var_name]}]")

# Example input using Matillion scalar variables
TABLE_DATA = [
    {
        "INVESTMENTID": jv_investmentid,
        "PORTFOLIONAAM": jv_json_portfolionaam,
        "PORTFOLIOISPLANNING": True,
    }
]

json_output = make_json_from_table(TABLE_DATA)
context.updateVariable("jv_json", json_output)

# Print variables again after update for visibility
_globals = {name: globals()[name] for name in list(globals())}
for var_name in _globals:
    if var_name.startswith("jv_"):
        print(f"[{var_name} --> {_globals[var_name]}]")

