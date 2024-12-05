# Flask CSV Analyzer common values and their counts

This is a Flask web application that allows users to upload CSV files, analyze the data, show you common values and their counts.

## Features

- Upload CSV files
- Data cleaning and normalization
- Count occurrences of values across columns
- Generate visualizations of value distributions

## Requirements

- Python 3.x
- Flask
- pandas
- plotly

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jaannawaz/CSV-Analyzer.git
   cd CSV-Analyzer
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

3. Upload a CSV file to analyze the data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
