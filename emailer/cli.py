import argparse
from .generator import EmailHTMLGenerator

def parse_args():
    parser = argparse.ArgumentParser(description='Generate HTML email from a config file.')
    parser.add_argument('-c', '--config', type=str, required=True, help='Path to the config file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to the output HTML file')
    # parser.add_argument('-h', '--help', action='help', help='Show this help message and exit')
    return parser.parse_args()

def main() -> None:    
    args = parse_args()
    config_file = args.config
    html_output_file = args.output

    # Create an instance of the class and generate the HTML
    email_generator = EmailHTMLGenerator(config_file, html_output_file)
    email_generator.generate_html()


if __name__=='__main__':
    main()