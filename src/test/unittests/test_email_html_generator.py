import pytest
import os
import yaml
from hypothesis import given, strategies as st
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
                "content": "This is a test paragraph.",
                "styles": {"background-color": "#f9f9f9", "color": "#000000", "padding": "15px", "width": "100%"}
            },
            {
                "type": "image",
                "src": "tests/assets/test_image.jpg",
                "alt": "Test Image",
                "width": "300px"
            }
        ]
    }

@pytest.fixture
def mock_yaml_file(tmp_path, mock_config):
    """Fixture for creating a mock YAML configuration file."""
    config_file = tmp_path / "mock_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(mock_config, f)
    return str(config_file)

@pytest.fixture
def mock_image(tmp_path):
    """Fixture for creating a mock image file."""
    img_path = tmp_path / "test_image.jpg"
    with open(img_path, 'wb') as f:
        f.write(os.urandom(1024))  # Create a dummy file with random bytes
    return str(img_path)

@pytest.fixture
def email_generator(mock_yaml_file):
    """Fixture to create an instance of EmailHTMLGenerator."""
    return EmailHTMLGenerator(mock_yaml_file, output_file="target/mock_email_template.html")


# Unit Tests
def test_load_config(email_generator, mock_config):
    """Test that the configuration is loaded correctly."""
    assert email_generator.config == mock_config


def test_encode_image_base64(email_generator, mock_image):
    """Test that image encoding works correctly."""
    encoded_image = email_generator.encode_image_base64(mock_image)
    assert isinstance(encoded_image, str)
    assert encoded_image.startswith('/9j/')  # Check for Base64 JPEG header


def test_generate_html(email_generator, tmp_path):
    """Test that the HTML file is generated correctly."""
    email_generator.generate_html()
    output_file = email_generator.output_file
    assert os.path.exists(output_file)
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "<html>" in content
        assert "Welcome to the Test Email" in content  # Check if the header content is present


# Property-Based Tests
@given(st.text())
def test_generate_html_with_random_titles(mock_yaml_file, tmp_path, title):
    """Test generating HTML with random titles using Hypothesis."""
    # Create a generator with a modified title
    email_generator = EmailHTMLGenerator(mock_yaml_file, output_file=str(tmp_path / "output.html"))
    email_generator.config['title'] = title
    email_generator.generate_html()
    with open(email_generator.output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert title in content  # Check if the random title is present


@given(st.text(min_size=1))
def test_image_alt_text(mock_yaml_file, tmp_path, mock_image, alt_text):
    """Test that random alt text appears correctly in the generated HTML."""
    email_generator = EmailHTMLGenerator(mock_yaml_file, output_file=str(tmp_path / "output.html"))
    # Modify the config to include the random alt text
    email_generator.config['sections'] = [
        {
            "type": "image",
            "src": mock_image,
            "alt": alt_text,
            "width": "100px"
        }
    ]
    email_generator.generate_html()
    with open(email_generator.output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert alt_text in content  # Check if the alt text is present in the generated HTML


@given(st.text(min_size=1))
def test_invalid_image_path(email_generator, tmp_path, invalid_path):
    """Test that the HTML correctly handles invalid image paths."""
    email_generator.config['sections'] = [
        {
            "type": "image",
            "src": invalid_path,
            "alt": "Invalid Image",
            "width": "100px"
        }
    ]
    email_generator.generate_html()
    with open(email_generator.output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "Image not found: Invalid Image" in content
