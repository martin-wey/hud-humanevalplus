from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json


@dataclass
class PromptTemplate:
    """A prompt template with metadata."""

    name: str
    description: str
    template: str
    variables: List[str]

    def format(self, **kwargs) -> str:
        """Format the template with provided variables."""
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required variable: {e}")

    def validate_variables(self, **kwargs) -> bool:
        """Check if all required variables are provided."""
        return all(var in kwargs for var in self.variables)


class BasePromptTemplate(ABC):
    """Abstract base class for prompt templates."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def generate(self, **kwargs) -> str:
        """Generate the prompt with given variables."""
        pass

    @abstractmethod
    def get_required_variables(self) -> List[str]:
        """Get list of required variables."""
        pass


class HumanEvalPrompt(BasePromptTemplate):
    """HumanEval prompt template version 1.0 - Basic approach."""

    @property
    def name(self) -> str:
        return "humaneval_basic"

    @property
    def description(self) -> str:
        return "Basic HumanEval prompt - direct problem solving"

    def generate(self, **kwargs) -> str:
        prompt = kwargs.get("prompt", "")
        entry_point = kwargs.get("entry_point", "")
        test = kwargs.get("test", "")

        return f"""You are an expert Python programmer. Solve this coding problem:

Function to implement: `{entry_point}`

Please provide ONLY the Python function implementation. No explanations, no markdown formatting, just the code.

```python
{prompt}
"""

    def get_required_variables(self) -> List[str]:
        return ["prompt", "entry_point"]


class IterativePromptTemplate(BasePromptTemplate):
    """Iterative prompt template for refinement."""

    @property
    def name(self) -> str:
        return "humaneval_iterative"

    @property
    def description(self) -> str:
        return "Iterative prompt for refining solutions based on test feedback"

    def generate(self, **kwargs) -> str:
        prompt = kwargs.get("prompt", "")
        entry_point = kwargs.get("entry_point", "")
        test = kwargs.get("test", "")
        previous_attempt = kwargs.get("previous_attempt", "")
        test_feedback = kwargs.get("test_feedback", "")

        base_prompt = f"""You are an expert Python programmer. Solve this coding problem:

Problem:
{prompt}

Function to implement: `{entry_point}`

Test cases:
{test}"""

        if previous_attempt and test_feedback:
            return f"""{base_prompt}

## Previous Attempt
```python
{previous_attempt}
```

## Test Results
{test_feedback}

## Your Task
Fix the implementation to pass all tests. Provide ONLY the corrected Python function implementation."""

        return f"""{base_prompt}

Please provide ONLY the Python function implementation. No explanations, no markdown formatting, just the code."""

    def get_required_variables(self) -> List[str]:
        return ["prompt", "entry_point", "test"]


class PromptTemplateManager:
    """Manager for prompt templates with versioning and selection."""

    def __init__(self):
        self._templates: Dict[str, BasePromptTemplate] = {}
        self._register_builtin_templates()

    def _register_builtin_templates(self):
        """Register built-in prompt templates."""
        builtin_templates = [
            HumanEvalPrompt(),
            IterativePromptTemplate(),
        ]

        for template in builtin_templates:
            self.register_template(template)

    def register_template(self, template: BasePromptTemplate):
        """Register a new prompt template."""
        self._templates[template.name] = template

    def get_template(self, name: str) -> Optional[BasePromptTemplate]:
        """Get a template by name."""
        if name not in self._templates:
            return None

        return self._templates[name]

    def list_templates(self) -> List[Dict[str, Any]]:
        """List all available templates."""
        result = []
        for name, template in self._templates.items():
            result.append(
                {
                    "name": name,
                    "description": template.description,
                    "required_variables": template.get_required_variables(),
                }
            )
        return result

    def generate_prompt(self, template_name: str, **kwargs) -> str:
        """Generate a prompt using the specified template."""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")

        return template.generate(**kwargs)

    def validate_template_variables(self, template_name: str, **kwargs) -> bool:
        """Validate that all required variables are provided."""
        template = self.get_template(template_name)
        if not template:
            return False

        required_vars = template.get_required_variables()
        return all(var in kwargs for var in required_vars)


# Example usage and testing
if __name__ == "__main__":
    prompt_manager = PromptTemplateManager()

    # Test the prompt manager
    print("Available templates:")
    for template_info in prompt_manager.list_templates():
        print(f"  {template_info['name']}: {template_info['description']}")

    print("\n" + "=" * 50)

    # Test generating a prompt
    sample_data = {
        "prompt": 'def has_close_elements(numbers, threshold):\n    """Check if any two numbers are closer than threshold."""\n    pass',
        "entry_point": "has_close_elements",
        "test": "def test_has_close_elements():\n    assert has_close_elements([1, 2, 3], 0.5) == True",
        "canonical_solution": "def has_close_elements(numbers, threshold):\n    for i in range(len(numbers)):\n        for j in range(i + 1, len(numbers)):\n            if abs(numbers[i] - numbers[j]) < threshold:\n                return True\n    return False",
    }

    print("Generated prompt (basic):")
    print(prompt_manager.generate_prompt("humaneval_basic", **sample_data))

    print("\n" + "=" * 50)
