"""Unit tests for word counting logic."""

from word_counter.counter import count_words


def test_basic_counting():
    text = "apple banana apple cherry banana apple"
    result = count_words(text)
    assert result == [("cherry", 1), ("banana", 2), ("apple", 3)]


def test_lowercasing():
    text = "Hello HELLO hello"
    result = count_words(text)
    assert result == [("hello", 3)]


def test_punctuation_removal():
    text = "hello, world! hello... world?"
    result = count_words(text)
    assert result == [("hello", 2), ("world", 2)]


def test_empty_string():
    assert count_words("") == []


def test_only_punctuation():
    assert count_words("!!! ??? ...") == []


def test_contractions_preserved():
    text = "don't can't won't don't"
    result = count_words(text)
    assert result == [("can't", 1), ("won't", 1), ("don't", 2)]


def test_ascending_sort_order():
    text = "a b b c c c"
    result = count_words(text)
    counts = [count for _, count in result]
    assert counts == sorted(counts)


def test_numbers_included():
    text = "file1 file2 file1"
    result = count_words(text)
    assert result == [("file2", 1), ("file1", 2)]
