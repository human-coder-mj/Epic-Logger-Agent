"""
Tests for the Epic Changelog Agent (Hugging Face version)
"""

from unittest.mock import Mock, patch
import pytest
from app.epic_log_generator import EpicChangelogAgent


class TestEpicChangelogAgent:
    
    def test_init_with_api_key(self):
        """Test initialization with API key."""
        agent = EpicChangelogAgent(api_key="test-key")
        assert agent.api_key == "test-key"
    
    def test_init_without_api_key_raises_error(self):
        """Test that missing API key raises ValueError."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="Hugging Face API key is required"):
                EpicChangelogAgent()
    
    def test_themes_exist(self):
        """Test that all expected themes are available."""
        agent = EpicChangelogAgent(api_key="test-key")
        expected_themes = ["medieval", "space", "superhero", "mythology"]
        
        for theme in expected_themes:
            assert theme in agent.themes
            assert "vocabulary" in agent.themes[theme]
            assert "metaphors" in agent.themes[theme]
            assert "tone" in agent.themes[theme]
    
    @patch('epic_changelog.InferenceClient')
    def test_generate_epic_changelog_success_chat(self, mock_inference_client):
        """Test successful changelog generation with chat completion."""
        # Mock the Hugging Face response structure
        mock_choice = Mock()
        mock_choice.message.content = "⚔️ Vanquished the login demon!"
        
        mock_response = Mock()
        mock_response.choices = [mock_choice]
        
        mock_inference_client.return_value.chat_completion.return_value = mock_response
        
        agent = EpicChangelogAgent(api_key="test-key")
        result = agent.generate_epic_changelog("Fixed login bug")
        
        assert result == "⚔️ Vanquished the login demon!"
        mock_inference_client.return_value.chat_completion.assert_called_once()
    
    @patch('epic_changelog.InferenceClient')
    def test_generate_epic_changelog_success_text_generation(self, mock_inference_client):
        """Test successful changelog generation with text generation fallback."""
        # Mock chat_completion to fail, text_generation to succeed
        mock_inference_client.return_value.chat_completion.side_effect = Exception("Chat not supported")
        mock_inference_client.return_value.text_generation.return_value = "⚔️ Vanquished the login demon!"
        
        agent = EpicChangelogAgent(api_key="test-key")
        result = agent.generate_epic_changelog("Fixed login bug")
        
        assert result == "⚔️ Vanquished the login demon!"
        mock_inference_client.return_value.text_generation.assert_called_once()
    
    @patch('epic_changelog.InferenceClient')
    def test_generate_epic_changelog_handles_error(self, mock_inference_client):
        """Test error handling in changelog generation."""
        mock_inference_client.return_value.chat_completion.side_effect = Exception("API Error")
        mock_inference_client.return_value.text_generation.side_effect = Exception("API Error")
        
        agent = EpicChangelogAgent(api_key="test-key")
        result = agent.generate_epic_changelog("Fixed login bug")
        
        assert "Failed to summon the epic transformation" in result
        assert "API Error" in result
    
    def test_process_changelog_file_not_found(self):
        """Test handling of non-existent file."""
        agent = EpicChangelogAgent(api_key="test-key")
        results = agent.process_changelog_file("nonexistent.txt")
        
        assert len(results) == 1
        assert "could not be found" in results[0]


if __name__ == "__main__":
    pytest.main([__file__])
