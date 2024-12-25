from utils.email_html_generator import EmailHTMLGenerator

def main() -> None:    
    # Main execution
    config_file = 'src/main/config/contents.yaml'
    html_output_file = 'target/contents_email.html'

    # Create an instance of the class and generate the HTML
    email_generator = EmailHTMLGenerator(config_file, html_output_file)
    email_generator.generate_html()


if __name__=='__main__':
    main()

