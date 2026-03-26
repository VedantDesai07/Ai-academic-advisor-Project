"""
AI Academic Advisor — Test Suite
Run with: python -m pytest test_advisor.py -v
"""
import os
import pytest
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime
from pydantic import BaseModel


# ── tools.py tests ──────────────────────────────────────────────────────────

from tools import save_to_txt, save_tool, search_tool, wiki_tool


class TestSaveToTxt:
    def test_saves_data_to_file(self, tmp_path):
        """save_to_txt writes content to a file."""
        filepath = str(tmp_path / "output.txt")
        result = save_to_txt("test content", filename=filepath)
        assert os.path.exists(filepath)

    def test_returns_success_message(self, tmp_path):
        """save_to_txt returns a success string."""
        filepath = str(tmp_path / "output.txt")
        result = save_to_txt("some data", filename=filepath)
        assert "successfully saved" in result.lower()

    def test_file_contains_timestamp(self, tmp_path):
        """Saved file includes a timestamp."""
        filepath = str(tmp_path / "output.txt")
        save_to_txt("test data", filename=filepath)
        with open(filepath, "r") as f:
            content = f.read()
        assert "Timestamp:" in content

    def test_file_contains_saved_data(self, tmp_path):
        """Saved file includes the original data string."""
        filepath = str(tmp_path / "output.txt")
        save_to_txt("my important research", filename=filepath)
        with open(filepath, "r") as f:
            content = f.read()
        assert "my important research" in content

    def test_appends_on_multiple_calls(self, tmp_path):
        """Calling save_to_txt twice appends rather than overwriting."""
        filepath = str(tmp_path / "output.txt")
        save_to_txt("first entry", filename=filepath)
        save_to_txt("second entry", filename=filepath)
        with open(filepath, "r") as f:
            content = f.read()
        assert "first entry" in content
        assert "second entry" in content

    def test_default_filename_is_research_output(self):
        """Default filename is research_output.txt."""
        with patch("builtins.open", mock_open()) as mock_file:
            save_to_txt("data")
            mock_file.assert_called_once_with("research_output.txt", "a", encoding="utf-8")

    def test_empty_string_input(self, tmp_path):
        """save_to_txt handles empty string without crashing."""
        filepath = str(tmp_path / "output.txt")
        result = save_to_txt("", filename=filepath)
        assert result is not None

    def test_long_input(self, tmp_path):
        """save_to_txt handles large content correctly."""
        filepath = str(tmp_path / "output.txt")
        big_data = "word " * 1000
        result = save_to_txt(big_data, filename=filepath)
        assert "successfully saved" in result.lower()


class TestTools:
    def test_save_tool_has_correct_name(self):
        """save_tool is named correctly for the agent."""
        assert save_tool.name == "save_text_to_file"

    def test_save_tool_has_description(self):
        """save_tool has a non-empty description."""
        assert len(save_tool.description) > 0

    def test_search_tool_has_correct_name(self):
        """search_tool is named 'search'."""
        assert search_tool.name == "search"

    def test_search_tool_has_description(self):
        """search_tool has a non-empty description."""
        assert len(search_tool.description) > 0

    def test_wiki_tool_exists(self):
        """wiki_tool is instantiated and not None."""
        assert wiki_tool is not None

    def test_all_three_tools_are_distinct(self):
        """All three tools are different objects."""
        assert save_tool is not search_tool
        assert save_tool is not wiki_tool
        assert search_tool is not wiki_tool


# ── Answer schema tests (mirrors main.py definition) ────────────────────────
# Defined here directly to avoid importing main.py's top-level LLM setup,
# which requires a live API key and network access during testing.

class Answer(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


class TestAnswerSchema:
    def test_valid_answer_parses_correctly(self):
        """Answer model accepts valid data."""
        answer = Answer(
            topic="Course Selection",
            summary="Take CS 135 in first year.",
            sources=["uwaterloo.ca"],
            tools_used=["search"],
        )
        assert answer.topic == "Course Selection"

    def test_answer_requires_topic(self):
        """Answer model raises error if topic is missing."""
        with pytest.raises(Exception):
            Answer(
                summary="some summary",
                sources=[],
                tools_used=[],
            )

    def test_answer_requires_summary(self):
        """Answer model raises error if summary is missing."""
        with pytest.raises(Exception):
            Answer(
                topic="Topic",
                sources=[],
                tools_used=[],
            )

    def test_sources_is_a_list(self):
        """sources field is stored as a list."""
        answer = Answer(
            topic="Topic",
            summary="Summary",
            sources=["source1", "source2"],
            tools_used=["wiki"],
        )
        assert isinstance(answer.sources, list)

    def test_tools_used_is_a_list(self):
        """tools_used field is stored as a list."""
        answer = Answer(
            topic="Topic",
            summary="Summary",
            sources=[],
            tools_used=["search", "wiki"],
        )
        assert isinstance(answer.tools_used, list)

    def test_empty_sources_allowed(self):
        """sources can be an empty list."""
        answer = Answer(
            topic="Topic",
            summary="Summary",
            sources=[],
            tools_used=[],
        )
        assert answer.sources == []

    def test_multiple_tools_used(self):
        """tools_used can hold multiple tool names."""
        answer = Answer(
            topic="Topic",
            summary="Summary",
            sources=[],
            tools_used=["search", "wiki", "save_text_to_file"],
        )
        assert len(answer.tools_used) == 3
