#!/usr/bin/env python3
import json
from typing import Any, Dict, List


def is_filled(value: Any) -> bool:
    """Return True if value is not None."""
    return value is not None


def make_portfolio_json(table_data: List[Dict[str, Any]]) -> str:
    """Convert table data to PortfolioInvestment API JSON string."""
    investments: List[Dict[str, Any]] = []
    for record in table_data:
        item: Dict[str, Any] = {}
        if is_filled(record.get("INVESTMENTCODE")):
            item["InvestmentCode"] = record["INVESTMENTCODE"]
        if is_filled(record.get("PORTFOLIONAAM")):
            item["PortfolioName"] = record["PORTFOLIONAAM"]
        # Default to true when not provided
        item["PortfolioIsPlanning"] = bool(record.get("PORTFOLIOISPLANNING", True))
        investments.append(item)
    return json.dumps(investments, indent=4)


if __name__ == "__main__":
    # Example for Matillion variables prefixed with 'jv_' available in globals
    glob = {g: globals()[g] for g in list(globals())}
    var_prefix = "jv_"
    for name in glob:
        if name.startswith(var_prefix):
            print(f"[{name} -> {glob[name]}]")

    table_data = [
        {
            "INVESTMENTCODE": glob.get("jv_investmentid"),
            "PORTFOLIOISPLANNING": True,
            "PORTFOLIONAAM": glob.get("jv_json_portfolionaam"),
        }
    ]

    json_output = make_portfolio_json(table_data)
    context.updateVariable("jv_json", json_output)
