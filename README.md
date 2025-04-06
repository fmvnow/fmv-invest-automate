# README.md

# Python Scraping Project

This project is scraping application built in Python. It utilizes Docker for containerization and PDF reader to process a negociation note

## Project Structure

```
src
├── scrapers
│   └── main.py
docker
├── Dockerfile
└── docker-compose.yml
requirements.txt
.env
.dockerignore
.gitignore
README.md
```

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   ```

2. **Install dependencies:**
   You can install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application using Docker:**
   Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```

## Usage

- The main entry point for the application is located in `src/scrapers/main.py`. You can modify this file to change the scraping logic as needed.
- Utility functions can be found in `src/utils/helpers.py`, which can be used to assist with various scraping tasks.
- Unit tests for the scraper functions are located in `src/tests/test_scraper.py`. You can run these tests to ensure everything is functioning correctly.

## Environment Variables

Make sure to configure the `.env` file with any necessary environment variables, such as API keys or other configuration settings.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
