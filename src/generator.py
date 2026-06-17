# src/generator.py
"""Assemble the final Markdown case study from insights and summaries."""
from typing import Dict, List
from datetime import datetime

TEMPLATE = """
# Case Study: {company_name}

**Generated:** {date}

---

## 1. Executive Summary
{executive_summary}

## 2. Problem Statement
{problem}

## 3. Solution & Approach
{solution}

## 4. Technology Stack
{technology}

## 5. Results & Impact
{result}

## 6. Industry Context
{industry}

## 7. References
{references}
"""

def build_section(items: List[str]) -> str:
    if not items:
        return "_No specific information extracted._"
    return "\n".join(f"- {item}" for item in items)

def generate_case_study(
    company_name: str,
    summary: str,
    insights: Dict[str, List[str]],
    references: List[str]
) -> str:
    """Render the case study markdown string."""
    ref_block = "\n".join(f"- {r}" for r in references) if references else "_None found._"
    return TEMPLATE.format(
        company_name=company_name,
        date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        executive_summary=summary[:800] + "..." if len(summary) > 800 else summary,
        problem=build_section(insights.get("problem", [])),
        solution=build_section(insights.get("solution", [])),
        technology=build_section(insights.get("technology", [])),
        result=build_section(insights.get("result", [])),
        industry=build_section(insights.get("industry", [])),
        references=ref_block,
    )

def generate_all(
    companies: Dict[str, str],
    all_insights: Dict[str, Dict],
    all_refs: Dict[str, List]
) -> Dict[str, str]:
    """Generate case studies for all companies."""
    return {
        name: generate_case_study(
            company_name=name,
            summary=companies.get(name, ""),
            insights=all_insights.get(name, {}),
            references=all_refs.get(name, [])
        )
        for name in companies
    }
