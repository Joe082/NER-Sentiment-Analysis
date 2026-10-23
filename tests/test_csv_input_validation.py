from types import SimpleNamespace

import pytest

from run_batch import load_docs


def test_empty_csv_raises_value_error(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("", encoding="utf-8")

    args = SimpleNamespace(
        csv=str(csv_file),
        column=None,
        jsonl=None,
    )

    with pytest.raises(ValueError, match="header"):
        load_docs(args)


def test_header_only_csv_returns_empty_list(tmp_path):
    csv_file = tmp_path / "header_only.csv"
    csv_file.write_text("input_doc\n", encoding="utf-8")

    args = SimpleNamespace(
        csv=str(csv_file),
        column=None,
        jsonl=None,
    )

    assert load_docs(args) == []


def test_missing_column_raises_value_error(tmp_path):
    csv_file = tmp_path / "wrong_column.csv"
    csv_file.write_text(
        "other_column\nSome text\n",
        encoding="utf-8",
    )

    args = SimpleNamespace(
        csv=str(csv_file),
        column="input_doc",
        jsonl=None,
    )

    with pytest.raises(ValueError, match="input_doc"):
        load_docs(args)


def test_valid_csv_returns_documents(tmp_path):
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text(
        "input_doc\nBrightEdge is useful.\nSemrush is popular.\n",
        encoding="utf-8",
    )

    args = SimpleNamespace(
        csv=str(csv_file),
        column=None,
        jsonl=None,
    )

    assert load_docs(args) == [
        "BrightEdge is useful.",
        "Semrush is popular.",
    ]

def test_explicit_column_overrides_default_column(tmp_path):
    csv_file = tmp_path / "custom_column.csv"
    csv_file.write_text(
        "input_doc,custom_text\n"
        "Default text,Selected text\n",
        encoding="utf-8",
    )

    args = SimpleNamespace(
        csv=str(csv_file),
        column="custom_text",
        jsonl=None,
    )

    assert load_docs(args) == ["Selected text"]