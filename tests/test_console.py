"""Test cases for the console module."""
import click.testing
import pytest
import requests

from src.hypermodern_python_practice import console

@pytest.fixture
def runner():
  return click.testing.CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker):
  """Mocks wikipedia.random_page"""
  return mocker.patch("src.hypermodern_python_practice.wikipedia.random_page")

def test_main_succeeds(runner, mock_requests_get):
  result = runner.invoke(console.main)
  assert result.exit_code == 0

@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner):
  result = runner.invoke(console.main)
  assert result.exit_code == 0

"""Checks the string "Lorem Ipsum" is in the title"""
def test_main_prints_title(runner, mock_requests_get):
  result = runner.invoke(console.main)
  assert "Lorem Ipsum" in result.output

def test_main_invokes_requests_get(runner, mock_requests_get):
  """invokes requests.get"""
  runner.invoke(console.main)
  assert mock_requests_get.called

"""Uses English Wikipedia by default"""
def test_main_uses_en_wikipedia_org(runner, mock_requests_get):
  runner.invoke(console.main)
  args, _ = mock_requests_get.call_args
  assert "en.wikipedia.org" in args[0]

"""Uses specified language version of Wikipedia"""
def test_main_uses_specified_language(runner, mock_wikipedia_random_page):
  runner.invoke(console.main, ["--language=pl"])
  mock_wikipedia_random_page.assert_called_with(language="pl")

"""It exits with non-zero status code if the request fails"""
def test_main_fails_on_request_error(runner, mock_requests_get):
  mock_requests_get.side_effect = Exception("Boom")
  result = runner.invoke(console.main)
  assert result.exit_code == 1

"""request exception raised if connection fails"""
def test_main_prints_message_on_request_error(runner, mock_requests_get):
  mock_requests_get.side_effect = requests.RequestException
  result = runner.invoke(console.main)
  assert "Error" in result.output

