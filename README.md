# Jina Reader API Web Scraper

This project is a web scraper that uses the Jina AI Reader API to fetch and save content from web pages. It supports both single-page and multi-page scraping, with the ability to traverse links within allowed domains.

## Features

- Single-page and multi-page scraping
- Concurrent processing of URLs
- Rate limiting to respect API usage guidelines
- Extraction of page titles and links
- Saving content as Markdown files
- Configurable allowed domains for multi-page scraping

## Prerequisites

- Python 3.6+
- Jina AI Reader API key (obtain from https://jina.ai/reader/)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/jina-reader-api-scraper.git
   cd jina-reader-api-scraper
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory with the following content:
   ```
   BASE_URL=<Your Jina AI Reader API Base URL>
   API_KEY=<Your Jina AI Reader API Key>
   ```

## Requirements

The project requires the following Python packages (specified in `requirements.txt`):

```
certifi==2024.7.4
charset-normalizer==3.3.2
idna==3.7
joblib==1.4.2
numpy==2.0.1
python-dotenv==1.0.1
requests==2.32.3
scikit-learn==1.5.1
scipy==1.14.0
threadpoolctl==3.5.0
urllib3==2.2.2
```

You can install these requirements using the command:
```
pip install -r requirements.txt
```

## Usage

Run the scraper using the following command:

```
python jina.py <url> <output_dir> [--allowed_domains domain1 domain2 ...] [--multi_page]
```

Arguments:
- `url`: The initial URL to scrape
- `output_dir`: Directory to save scraped content
- `--allowed_domains` (optional): List of allowed domains to scrape (default: domain of the initial URL)
- `--multi_page` (optional): Enable multi-page scraping (default: False)

Example:
```
python jina.py https://example.com/start-page output_folder --allowed_domains example.com blog.example.com --multi_page
```

## Configuration

You can adjust the following variables in the script to fine-tune the scraper's behavior:

- `MAX_WORKERS`: Maximum number of concurrent workers (default: 5)
- `RATE_LIMIT`: Time in seconds between requests (default: 1)

## Output

The scraper saves each scraped page as a separate Markdown file in the specified output directory. The filename is based on the page title, sanitized to remove invalid characters.

## Limitations

- The scraper respects the rate limit set in the `RATE_LIMIT` variable to avoid overwhelming the API.
- Multi-page scraping is limited to the domains specified in `allowed_domains`.
- You need a valid API key from Jina AI Reader to use this scraper.

## Error Handling

The scraper prints error messages for failed requests or processing errors but continues with the next URL in the queue.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Specify your license here]