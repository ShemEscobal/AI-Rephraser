# AI Academic Paraphraser

by Shem Escobal

A web application that uses the Together AI API with Llama 3.3 to paraphrase academic text while maintaining academic integrity.

## Features

- Paraphrase academic text with different academic levels (High School, Undergraduate, Graduate, PhD)
- Natural and concise paraphrasing that avoids overly formal language
- Modern and responsive UI built with Bootstrap 5
- Real-time word count
- Copy to clipboard functionality
- Loading indicators for better user experience

## Prerequisites

- Python 3.7 or higher
- Together AI API key (free tier available)

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/ai-academic-paraphraser.git
cd ai-academic-paraphraser
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Together AI API key:
```
TOGETHER_API_KEY=your_together_api_key_here
```

## Usage

1. Start the Flask application:
```
python app.py
```

2. Open your web browser and navigate to `http://127.0.0.1:5000`

3. Paste your academic text in the editor, select the appropriate academic level, and click "Paraphrase"

4. Review the paraphrased text and copy it to your clipboard if needed

## How It Works

The application uses the Together AI API with the Llama 3.3 70B Instruct Turbo model (free tier) to generate paraphrased versions of academic text. The API is prompted to maintain the same meaning but with different wording, appropriate for the selected academic level, while keeping the language natural and avoiding overly formal phrasing.

## Important Notes

- Always review the paraphrased text for accuracy and meaning
- This tool is designed to help with paraphrasing, not to encourage plagiarism
- Always cite your sources properly in academic writing

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Together AI for providing the API
- Meta for the Llama 3.3 model
- Bootstrap for the UI components
- Flask for the web framework 
