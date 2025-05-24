import os
import yaml
import base64
from typing import Dict, Any
import logging


class EmailHTMLGenerator:
    """A class to generate HTML emails with embedded Base64 images from a YAML configuration."""

    def __init__(self, config_file: str, output_file: str = 'email_template.html'):
        """
        Initializes the EmailHTMLGenerator with a YAML configuration file and an output file path.

        Args:
            config_file (str): Path to the YAML configuration file.
            output_file (str): Path to the output HTML file. Default is 'email_template.html'.
        """
        self.config_file = config_file
        self.output_file = output_file
        self.logger = logging.getLogger(__class__.__name__)
        self.config = self.load_config()
        os.makedirs("target", exist_ok=True)
        
        # Logging
        self.logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self.logger.info(f"Initialized with config file: {config_file} and output file: {output_file}")  

    def load_config(self) -> Dict[str, Any]:
        """
        Loads the configuration from a YAML file.

        Returns:
            Dict[str, Any]: A dictionary containing the configuration data.
        """
        try:
            with open(self.config_file, 'r', encoding="UTF-8") as file:
                config = yaml.safe_load(file)
            self.logger.info("Configuration loaded successfully.")
            return config
        except FileNotFoundError:
            self.logger.error(f"Configuration file {self.config_file} not found.")
            raise
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing YAML file: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise

    @staticmethod
    def encode_image_base64(image_path: str) -> str:
        """
        Encodes an image in Base64 format for embedding in HTML.

        Args:
            image_path (str): Path to the image file.

        Returns:
            str: The Base64 encoded image as a UTF-8 string.
        """
        try:
            with open(image_path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_image
        except FileNotFoundError:
            logging.error(f"Image file {image_path} not found.")
            raise
        except Exception as e:
            logging.error(f"Unexpected error encoding image: {e}")
            raise

    def generate_html(self) -> None:
        """
        Generates an HTML file with embedded Base64 images based on the configuration data.
        """
        html_start = """<!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <title>{title}</title>
            <style>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }}
                .container {{ max-width: {layout_width}; margin: 0 auto; background: #ffffff; border: 1px solid #dddddd; }}
                .header, .content, .footer, .button-container, .button {{ font-size: 16px; line-height: 1.5; }}
                .header, .footer {{ text-align: center; }}
                .button-container {{ text-align: center; }}
                .button {{ background-color: #007BFF; color: #ffffff; text-decoration: none; padding: 10px 20px; border-radius: 5px; display: inline-block; font-size: 16px; }}
                .button a {{ color: #ffffff; text-decoration: none; }}
                img {{ display: block; margin: 0 auto; border: none; }}
            </style>
            <!--[if mso]>
            <style type="text/css">
                img {{ width: auto; max-width: 100%; height: auto; }}
            </style>
            <![endif]-->
        </head>
        <body style="background-color: #f4f4f4; margin: 0; padding: 0;">
            <table class="container" align="center" cellpadding="0" cellspacing="0" border="0">
        """

        html_end = """
            </table>
            </body>
            </html>
        """

        # Initialize the content with the title from the config
        html_content = html_start.format(title=self.config.get("title", "Email"), layout_width=self.config.get("layout", {"width": "600px"})["width"])

        # Build sections based on the config
        for section in self.config.get("sections", []):
            html_content += self.build_section(section)

        # Close the HTML content
        html_content += html_end

        # Write the HTML content to the output file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        self.logger.info(f"HTML file generated successfully: {self.output_file}")

    def validate_section(self, section_type: str) -> None:
        """
        Validates the structure of the sections in the configuration.
        This method can be extended to include specific validation rules.
        """
        valid_sections = {"header", "paragraph", "footer", "list", "image", "block"}
        if section_type not in valid_sections:
            self.logger.warning(f"Invalid section type: {section_type}. Expected one of {valid_sections}. Skipping this section.")

    def build_section(self, section: Dict[str, Any]) -> str:
        """
        Builds a specific section of the HTML content based on the section type and styles.

        Args:
            section (Dict[str, Any]): A dictionary containing section details such as type, content, and styles.

        Returns:
            str: The HTML content for the section.
        """
        section_type = section.get("type")
        styles = section.get("styles", {})
        width = styles.get("width", "100%")
        style_str = "; ".join([f"{k}: {v}" for k, v in styles.items() if k != "width"])
        content = ""

        # Validate the section type
        self.validate_section(section_type)

        # Build the content based on the section type
        if section_type in {"header", "paragraph", "footer"}:
            # Replace newlines with <br> tags
            content_details = section.get("content", "").replace("\n", "<br>")
            content += f'<tr><td class="{section_type}" style="{style_str}" width="{width}">{content_details}</td></tr>'

        elif section_type == "list":
            items = section.get("items", [])
            content += f'<tr><td class="content" style="{style_str}" width="{width}"><ul style="padding-left: 20px;">'
            for item in items:
                content += f'<li style="margin-bottom: 10px;">{item}</li>'
            content += '</ul></td></tr>'

        elif section_type == "image":
            content += self.build_image_section(section, style_str, width)

        elif section_type == "block":
            content += self.build_block_section(section, style_str, width)

        return content


    def build_image_section(self, section: Dict[str, Any], style_str: str, width: str) -> str:
        """
        Builds the HTML content for an image section with embedded Base64 image.

        Args:
            section (Dict[str, Any]): Section details including the image source, alt text, and width.
            style_str (str): CSS styles for the section.
            width (str): Width of the section.

        Returns:
            str: The HTML content for the image section.
        """
        src = section.get("src", "")
        alt = section.get("alt", "")
        img_width = section.get("width", "100%")
        img_height = section.get("height", "auto")
        image_content = ""

        if os.path.exists(src):
            encoded_image = self.encode_image_base64(src)
            image_content += f'<tr><td class="content" style="{style_str}" width="{width}">'
            image_content += f'<img src="data:image/jpeg;base64,{encoded_image}" alt="{alt}" width="{img_width}" height="{img_height}"  style="width: {img_width}; height: {img_height};">'
            image_content += '</td></tr>'
        else:
            image_content += f'<tr><td class="content" style="{style_str}" width="{width}"><p>Image not found: {alt}</p></td></tr>'

        return image_content

    def build_block_section(self, section: Dict[str, Any], style_str: str, width: str) -> str:
        """
        Builds the HTML content for a block section containing multiple rows and columns.

        Args:
            section (Dict[str, Any]): Section details including rows and columns data.
            style_str (str): CSS styles for the section.
            width (str): Width of the section.

        Returns:
            str: The HTML content for the block section.
        """
        block_content = f'<tr><td class="content" style="{style_str}" width="{width}"><table width="100%" cellpadding="0" cellspacing="0" border="0">'
        
        for row in section.get("rows", []):
            row_styles = row.get("styles", {})
            row_style_str = "; ".join([f"{k}: {v}" for k, v in row_styles.items()])
            block_content += f'<tr style="{row_style_str}">'

            for column in row.get("columns", []):
                column_type = column.get("type")
                column_styles = column.get("styles", {})
                column_style_str = "; ".join([f"{k}: {v}" for k, v in column_styles.items()])
                col_width = column_styles.get("width", "auto")

                if column_type == "icon":
                    block_content += self.build_icon_column(column, column_style_str, col_width)
                elif column_type == "text":
                    block_content += f'<td style="{column_style_str}" width="{col_width}">{column.get("content", "")}</td>'
                elif column_type == "link":
                    block_content += self.build_link_column(column, column_style_str, col_width)
                elif column_type == "image":
                    block_content += self.build_image_column(column, column_style_str, col_width)

            block_content += '</tr>'  # Close row
        block_content += '</table></td></tr>'  # Close block and table

        return block_content

    def build_icon_column(self, column: Dict[str, Any], column_style_str: str, col_width: str) -> str:
        """
        Builds an icon column with a Base64 encoded image.

        Args:
            column (Dict[str, Any]): Column details including image source, alt text, and width.
            column_style_str (str): CSS styles for the column.
            col_width (str): Width of the column.

        Returns:
            str: The HTML content for the icon column.
        """
        src = column.get("src", "")
        alt = column.get("alt", "")
        icon_width = column.get("width", "100%")
        icon_height = column.get("height", "auto")

        if os.path.exists(src):
            encoded_image = self.encode_image_base64(src)
            return f'<td class="icon" style="{column_style_str}" width="{col_width}"><img src="data:image/jpeg;base64,{encoded_image}" alt="{alt}" width="{icon_width}" height="{icon_height}" style="width: {icon_width}; height: {icon_height};"></td>'
        else:
            return f'<td class="icon" style="{column_style_str}" width="{col_width}"><p>Image not found: {alt}</p></td>'

    def build_image_column(self, column: Dict[str, Any], column_style_str: str, col_width: str) -> str:
        """Builds an image column with a CID reference."""
        src = column.get("src", "")
        alt = column.get("alt", "")
        img_width = column.get("width", "100%")
        img_height = column.get("height", "auto")

        if os.path.exists(src):
            cid = self.add_inline_image(src)
            return f'<td class="image" style="{column_style_str}" width="{col_width}"><img src="cid:{cid}" alt="{alt}" width="{img_width}" height="{img_height}" style="width: {img_width}; height: {img_height};"></td>'
        else:
            return f'<td class="image" style="{column_style_str}" width="{col_width}"><p>Image not found: {alt}</p></td>'

    def add_inline_image(self, image_path: str) -> str:
        """
        Adds an image to the inline images dictionary and returns its Content-ID (CID).

        Args:
            image_path (str): Path to the image file.

        Returns:
            str: The Content-ID (CID) for the image.
        """
        cid = os.path.basename(image_path).replace(".", "_")
        self.inline_images[cid] = image_path
        return cid

    def get_inline_images(self):
        """Returns the dictionary of inline images with their CIDs and file paths."""
        return self.inline_images

    def build_link_column(self, column: Dict[str, Any], column_style_str: str, col_width: str) -> str:
        """
        Builds a link column with a styled button.

        Args:
            column (Dict[str, Any]): Column details including link href and content.
            column_style_str (str): CSS styles for the column.
            col_width (str): Width of the column.

        Returns:
            str: The HTML content for the link column.
        """

        href = column.get("href", "#")
        background_color_link = column.get("styles", {}).get("background-color-link", "none")  # Default to blue if not provided
        text_color = column.get("styles", {}).get("color", "#ffffff")  # Default to white text if not provided
        font_size = column.get("styles", {}).get("font-size", "16px")  # Default to 16px if not provided
        border_radius = column.get("styles", {}).get("border-radius", "16px")  # Default to 16px if not provided
        button_height = column.get("styles", {}).get("button-height", "auto")  # Default to 16px if not provided
        button_height = column.get("styles", {}).get("background-button-color", "none") 
        return f'''
        <td class="button-container" style="{column_style_str}" width="{col_width}">
            <table align="center" cellpadding="0" cellspacing="0" border="0">
                <tr>
                    <td class="button" style="background-color: {background_color_link}; border-radius: {border_radius}; text-align: center; font-size: {font_size}; height: {button_height}">
                        <a href="{href}" style="color: {text_color}; display: inline-block; padding: 10px 20px; text-decoration: none;">{column.get("content", "")}</a>
                    </td>
                </tr>
            </table>
        </td>
        '''
