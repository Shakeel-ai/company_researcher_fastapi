from dataclasses import dataclass, field
from typing import Any, Optional, Annotated
import operator


DEFAULT_EXTRACTION_SCHEMA = {
    "title": "CompanyInfo",
    "description": "Basic information about a company including current job openings",
    "type": "object",
    "properties": {
        "company_name": {
            "type": "string",
            "description": "Official name of the company"
        },
        "founding_year": {
            "type": ["integer", "null"],  # Allow null if data is missing
            "description": "Year the company was founded"
        },
        "founder_names": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Names of the founding team members"
        },
        "product_description": {
            "type": "string",
            "description": "Brief description of the company's main product or service"
        },
        "funding_summary": {
            "type": ["string", "null"],  # Allow empty data
            "description": "Summary of the company's funding history"
        },
        "open_jobs": {
            "type": "array",
            "description": "List of current open job positions at the company",
            "items": {
                "type": "object",
                "properties": {
                    "job_title": {
                        "type": "string",
                        "description": "Title of the job position"
                    },
                    "apply_link": {
                        "type": "string",
                        "description": "Link to apply for the job",
                        "format": "uri"
                    },
                    "last_date": {
                        "type": "string",
                        "description": "Application deadline date",
                        "format": "date"  # Ensure it's a valid date format
                    },
                    "job_location": {
                        "type": ["string", "null"],  # Location can be missing
                        "description": "Location of the job"
                    },
                    "job_description": {
                        "type": ["string", "null"],  # Allow missing descriptions
                        "description": "Brief description of the job"
                    },
                    "job_type": {
                        "type": ["string", "null"],
                        "description": "Type of job (full-time, part-time, contract)"
                    }
                },
                
            }
        }
    },
    "required": ["company_name", "product_description"]  # Added required fields
}





@dataclass(kw_only=True)
class InputState:
    """Input state defines the interface between the graph and the user (external API)."""

    company: str
    "Company to research provided by the user."

    extraction_schema: dict[str, Any] = field(
        default_factory=lambda: DEFAULT_EXTRACTION_SCHEMA
    )
    "The json schema defines the information the agent is tasked with filling out."

    user_notes: Optional[dict[str, Any]] = field(default=None)
    "Any notes from the user to start the research process."


@dataclass(kw_only=True)
class OverallState:
    """Input state defines the interface between the graph and the user (external API)."""

    company: str
    "Company to research provided by the user."

    extraction_schema: dict[str, Any] = field(
        default_factory=lambda: DEFAULT_EXTRACTION_SCHEMA
    )
    "The json schema defines the information the agent is tasked with filling out."

    user_notes: str = field(default=None)
    "Any notes from the user to start the research process."

    search_queries: list[str] = field(default=None)
    "List of generated search queries to find relevant information"

    completed_notes: Annotated[list, operator.add] = field(default_factory=list)
    "Notes from completed research related to the schema"

    info: dict[str, Any] = field(default=None)
    """
    A dictionary containing the extracted and processed information
    based on the user's query and the graph's execution.
    This is the primary output of the enrichment process.
    """

    is_satisfactory: bool = field(default=None)
    "True if all required fields are well populated, False otherwise"

    reflection_steps_taken: int = field(default=0)
    "Number of times the reflection node has been executed"


@dataclass(kw_only=True)
class OutputState:
    """The response object for the end user.

    This class defines the structure of the output that will be provided
    to the user after the graph's execution is complete.
    """

    info: dict[str, Any]
    """
    A dictionary containing the extracted and processed information
    based on the user's query and the graph's execution.
    This is the primary output of the enrichment process.
    """
