# Automated Loom Transcript Scraper

This repository contains an automated scraper built with Python and FastAPI that takes a Loom video link as input and extracts the transcript from the video. It then generates a professional proposal email for the customer based on the extracted transcript. The application is hosted on AWS.

## Features

- Extracts transcript from Loom videos automatically.
- Generates professional proposal emails based on the transcript content.
- Utilizes FastAPI for creating a RESTful API endpoint.
- Hosted on AWS.

## Usage

1. **Clone the repository:**

    ```bash
    git clone [https://github.com/manas-codes/ScraperGPT/tree/master]
    ```

2. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the FastAPI application:**

    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

4. **Access the API endpoint** at `http://your-aws-instance-ip:8000/download_caption/` with a POST request containing JSON data in the following format:

    ```json
    {
        "video_url": "loom_video_url",
        "prompt": "additional_prompt_for_proposal"
    }
    ```

    Example:

    ```json
    {
        "video_url": "https://www.loom.com/video/your-video-id",
        "prompt": "Please create a proposal based on the video content."
    }
    ```

5. **Receive the transcript and proposal email** generated as a response.

## Tech Stack

- Python
- FastAPI
- Selenium
- OpenAI API
- AWS (Amazon Web Services)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
