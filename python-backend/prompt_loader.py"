"""
Prompt Template Loader for ERNI Gruppe Building Agents.

This module provides utilities for loading and rendering Jinja2 templates
for agent instructions, improving maintainability and separation of concerns.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound

logger = logging.getLogger(__name__)

# Template directory
PROMPTS_DIR = Path(__file__).parent / "prompts"


class PromptLoader:
    """
    Loader for agent instruction templates.

    Uses Jinja2 to load and render templates from the prompts/ directory.
    Provides caching and error handling for template operations.
    """

    def __init__(self, templates_dir: Path = PROMPTS_DIR):
        """
        Initialize the prompt loader.

        Args:
            templates_dir: Directory containing Jinja2 templates
        """
        self.templates_dir = templates_dir

        if not self.templates_dir.exists():
            logger.warning(
                f"Templates directory not found: {self.templates_dir}. "
                "Creating directory..."
            )
            self.templates_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=False,  # We're generating prompts, not HTML
            trim_blocks=True,
            lstrip_blocks=True,
        )

        logger.info(f"PromptLoader initialized with templates from: {self.templates_dir}")

    def load_template(self, template_name: str) -> Template:
        """
        Load a Jinja2 template by name.

        Args:
            template_name: Name of the template file (e.g., "triage_agent.j2")

        Returns:
            Loaded Jinja2 template

        Raises:
            TemplateNotFound: If template file doesn't exist
        """
        try:
            template = self.env.get_template(template_name)
            logger.debug(f"Loaded template: {template_name}")
            return template
        except TemplateNotFound:
            logger.error(f"Template not found: {template_name}")
            raise

    def render_template(self, template_name: str, **context: Any) -> str:
        """
        Load and render a template with the given context.

        Args:
            template_name: Name of the template file
            **context: Variables to pass to the template

        Returns:
            Rendered template string

        Raises:
            TemplateNotFound: If template file doesn't exist
        """
        template = self.load_template(template_name)
        rendered = template.render(**context)
        logger.debug(f"Rendered template: {template_name} with context keys: {list(context.keys())}")
        return rendered

    def render_agent_instructions(
        self,
        agent_name: str,
        recommended_prompt_prefix: str = "",
        **context: Any,
    ) -> str:
        """
        Render agent instructions template.

        Convenience method that automatically adds the recommended prompt prefix
        and uses standard naming convention for agent templates.

        Args:
            agent_name: Name of the agent (e.g., "triage", "cost_estimation")
            recommended_prompt_prefix: OpenAI Agents SDK recommended prefix
            **context: Additional context variables for the template

        Returns:
            Rendered instructions string

        Example:
            >>> loader = PromptLoader()
            >>> instructions = loader.render_agent_instructions(
            ...     "cost_estimation",
            ...     recommended_prompt_prefix=RECOMMENDED_PROMPT_PREFIX,
            ...     inquiry_id="INQ-12345"
            ... )
        """
        template_name = f"{agent_name}_agent.j2"

        # Add recommended prefix to context
        context["recommended_prompt_prefix"] = recommended_prompt_prefix

        return self.render_template(template_name, **context)

    def list_templates(self) -> list[str]:
        """
        List all available template files.

        Returns:
            List of template filenames
        """
        if not self.templates_dir.exists():
            return []

        templates = [
            f.name
            for f in self.templates_dir.iterdir()
            if f.is_file() and f.suffix in [".j2", ".jinja2"]
        ]

        logger.debug(f"Found {len(templates)} templates: {templates}")
        return sorted(templates)

    def validate_templates(self, required_templates: list[str]) -> Dict[str, bool]:
        """
        Validate that required templates exist.

        Args:
            required_templates: List of required template names

        Returns:
            Dictionary mapping template names to existence status

        Example:
            >>> loader = PromptLoader()
            >>> status = loader.validate_templates([
            ...     "triage_agent.j2",
            ...     "cost_estimation_agent.j2"
            ... ])
            >>> print(status)
            {'triage_agent.j2': True, 'cost_estimation_agent.j2': True}
        """
        available = set(self.list_templates())
        status = {template: template in available for template in required_templates}

        missing = [t for t, exists in status.items() if not exists]
        if missing:
            logger.warning(f"Missing templates: {missing}")
        else:
            logger.info(f"All {len(required_templates)} required templates found")

        return status


# Global prompt loader instance
_prompt_loader: Optional[PromptLoader] = None


def get_prompt_loader() -> PromptLoader:
    """
    Get the global PromptLoader instance (singleton pattern).

    Returns:
        Global PromptLoader instance
    """
    global _prompt_loader
    if _prompt_loader is None:
        _prompt_loader = PromptLoader()
    return _prompt_loader


def render_agent_instructions(
    agent_name: str,
    recommended_prompt_prefix: str = "",
    **context: Any,
) -> str:
    """
    Convenience function to render agent instructions.

    Args:
        agent_name: Name of the agent (e.g., "triage", "cost_estimation")
        recommended_prompt_prefix: OpenAI Agents SDK recommended prefix
        **context: Additional context variables for the template

    Returns:
        Rendered instructions string

    Example:
        >>> from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
        >>> instructions = render_agent_instructions(
        ...     "triage",
        ...     recommended_prompt_prefix=RECOMMENDED_PROMPT_PREFIX
        ... )
    """
    loader = get_prompt_loader()
    return loader.render_agent_instructions(
        agent_name, recommended_prompt_prefix, **context
    )


# Validate templates on module import
def _validate_required_templates():
    """Validate that all required agent templates exist."""
    required_templates = [
        "triage_agent.j2",
        "project_information_agent.j2",
        "cost_estimation_agent.j2",
        "project_status_agent.j2",
        "appointment_booking_agent.j2",
        "faq_agent.j2",
    ]

    loader = get_prompt_loader()
    status = loader.validate_templates(required_templates)

    missing = [t for t, exists in status.items() if not exists]
    if missing:
        logger.error(
            f"Missing required templates: {missing}. "
            "Agent instructions may not work correctly."
        )


# Run validation on import
try:
    _validate_required_templates()
except Exception as e:
    logger.warning(f"Template validation failed: {e}")

