import pytest
import os
import yaml
from unittest import mock
from main.utils.email_html_generator import EmailHTMLGenerator

# Fixtures
@pytest.fixture
def mock_config():
    """Fixture for a mock configuration dictionary."""
    return {
        "title": "Test Email",
        "sections": [
            {
                "type": "header",
                "content": "Welcome to the Test Email",
                "styles": {"background-color": "#333333", "color": "#ffffff", "padding": "10px", "width": "100%"}
            },
            {
                "type": "paragraph",
                "content": "This is a test email generated for unit testing.",
                "styles": {"padding": "10px", "width": "100%"}
            }
        ]
    }

@pytest.fixture
def mock_yaml_file(tmp_path, mock_config):
    """Fixture for a mock YAML configuration file."""
    yaml_file = tmp_path / "config.yaml"
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(mock_config, f)
    return str(yaml_file)

def test_load_config(mock_yaml_file):
    """Test loading configuration from a YAML file."""
    email_generator = EmailHTMLGenerator(mock_yaml_file)
    config = email_generator.load_config()
    assert config['title'] == "Test Email"
    assert config['sections'][0]['type'] == "header"
    assert config['sections'][1]['content'] == "This is a test email generated for unit testing."

# @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=mock_config)
@mock.patch("main.utils.email_html_generator.EmailHTMLGenerator.load_config", return_value=mock_config)
@mock.patch("os.path.exists", return_value=True)
def test_generate_html(mock_exists, mock_open, mock_yaml_file):
    """Test generating HTML from the configuration."""
    mock_config.get()
    email_generator = EmailHTMLGenerator(mock_yaml_file, "output.html")
    email_generator.generate_html()
    output_file = email_generator.output_file
    assert os.path.exists(output_file)
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "<html>" in content
        assert "Welcome to the Test Email" in content  # Check if the header content is present

# @mock.patch("builtins.open", new_callable=mock.mock_open, read_data="<html>{title}</html>")
# @mock.patch("os.path.exists", return_value=True)
# @mock.patch("src.main.utils.email_html_generator.EmailHTMLGenerator.load_config", return_value=mock_config)
# def test_generate_html_with_random_titles(mock_open, mock_exists, mock_config):
#     """Test generating HTML with random titles."""
#     email_generator = EmailHTMLGenerator(mock_yaml_file, output_file="tmp_path/output.html")
#     email_generator.config['title'] = "Random Title"
#     email_generator.generate_html()
#     with open(email_generator.output_file, 'r', encoding='utf-8') as f:
#         content = f.read()
#         assert "Random Title" in content  # Check if the random title is present

# @mock.patch("builtins.open", new_callable=mock.mock_open, read_data="<html><img src='image.png' alt='{alt_text}'></html>")
# @mock.patch("os.path.exists", return_value=True)
# def test_image_alt_text(mock_exists, mock_open, mock_yaml_file, tmp_path):
#     """Test generating HTML with random alt text for images."""
#     email_generator = EmailHTMLGenerator(mock_yaml_file, output_file=str(tmp_path / "output.html"))
#     email_generator.config['sections'][1]['content'] = "<img src='image.png' alt='Random Alt Text'>"
#     email_generator.generate_html()
#     with open(email_generator.output_file, 'r', encoding='utf-8') as f:
#         content = f.read()
#         assert "Random Alt Text" in content  # Check if the random alt text is present

# @mock.patch("builtins.open", new_callable=mock.mock_open, read_data="<html><img src='{image_path}'></html>")
# @mock.patch("os.path.exists", return_value=True)
# def test_invalid_image_path(mock_exists, mock_open, mock_yaml_file, tmp_path):
#     """Test generating HTML with invalid image paths."""
#     email_generator = EmailHTMLGenerator(mock_yaml_file, output_file=str(tmp_path / "output.html"))
#     email_generator.config['sections'][1]['content'] = "<img src='invalid_image_path'>"
#     email_generator.generate_html()
#     with open(email_generator.output_file, 'r', encoding='utf-8') as f:
#         content = f.read()
#         assert "invalid_image_path" in content  # Check if the random image path is present

if __name__=="__main__":
    pytest.main()
