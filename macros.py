"""
ASSIP 2026 Wiki — mkdocs-macros plugin hooks.

This module is referenced by `mkdocs.yml` (plugins → macros → module_name).
It exposes the canonical program facts to every page via Jinja2 so content
authors can write e.g. `{{ program.symposium }}` instead of hard-coding
"August 12, 2026" in twenty places.

Sibling content agents may extend this with custom filters and macros as
they author the dashboard pages; keep additions backwards-compatible.
"""

from __future__ import annotations


def define_env(env) -> None:
    """Register macros, filters, and variables used across docs/."""

    # ------------------------------------------------------------------ #
    # Program facts — single source of truth for dates / contacts.      #
    # Mirrors `extra.program` in mkdocs.yml; the dict here is what       #
    # `{{ program.* }}` resolves to inside markdown.                     #
    # ------------------------------------------------------------------ #
    env.variables["program"] = {
        "name": "Aspiring Scientists Summer Internship Program (ASSIP)",
        "short": "ASSIP",
        "host": "George Mason University, College of Science",
        "director": "Dr. Amanda Haymond Still",
        "director_email": "cosassip@gmu.edu",
        "mentor": "Prof. Lei Gao",
        "mentor_email": "lgao9@gmu.edu",
        "cohort": "Empirical Finance Research Group",
        "modality": "Remote (online only)",
        "orientation": "Thursday, June 18, 2026",
        "first_day": "Monday, June 22, 2026",
        "symposium": "Wednesday, August 12, 2026",
        "schedule": "Monday–Friday, 9:00 am – 5:00 pm",
        "holidays": ["June 19 (Juneteenth)", "July 3 (Independence Day observance)"],
        "tuition": "$1,299",
        "application_fee": "$25",
        "credits": "3 GMU College of Science credits",
        "deliverables": [
            "Research poster (required) at the August 12 symposium",
            "Abstract published in JSSR (Journal of Student-Scientists' Research)",
            "Optional full paper",
            "Scientific-writing and career-forum participation",
        ],
    }

    # ------------------------------------------------------------------ #
    # Convenience filter: render a week-status pill (matches the         #
    # .week-badge CSS classes in stylesheets/extra.css).                 #
    # Usage in markdown:  `{{ "active" | week_badge("Week 3") }}`        #
    # ------------------------------------------------------------------ #
    @env.filter
    def week_badge(status: str, label: str) -> str:
        status = (status or "upcoming").lower()
        if status not in {"upcoming", "active", "complete"}:
            status = "upcoming"
        return f'<span class="week-badge {status}">{label}</span>'
