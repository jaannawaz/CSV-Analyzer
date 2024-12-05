from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Serve static files from the uploads folder
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename != "":
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return redirect(url_for("analyze", filename=file.filename))
    return render_template("index.html")

@app.route("/analyze/<filename>")
def analyze(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Read the uploaded CSV file
    try:
        data = pd.read_csv(filepath)
    except Exception as e:
        return f"Error reading CSV file: {e}"

    print("Uploaded CSV Preview:")
    print(data.head())

    # Data cleaning: Strip whitespace and normalize case for string columns only
    for col in data.columns:
        if data[col].dtype == 'object':  # Process only string-like columns
            data[col] = data[col].str.strip().str.upper()  # Remove spaces and convert to uppercase

    data = data.dropna(how="any")  # Remove rows with missing values
    print("\nCleaned Data Preview:")
    print(data.head())

    if data.empty:
        return "The uploaded CSV file contains no valid data after cleaning."

    # Identify value occurrences across all columns
    columns = data.columns
    print(f"\nColumns Detected: {list(columns)}")

    # Count occurrences of each value across all columns
    value_counts = {}
    for col in columns:
        for value in data[col].dropna():
            value = str(value).strip().upper()  # Normalize case and remove whitespace
            value_counts[value] = value_counts.get(value, []) + [col]

    # Prepare a DataFrame showing the value, count, and sample columns
    results = []
    for value, col_list in value_counts.items():
        results.append({
            "Value": value,
            "Count": len(col_list),
            "Sample Columns": ", ".join(col_list)
        })

    result_df = pd.DataFrame(results)
    result_df = result_df.sort_values(by="Count", ascending=False)

    # Save results to CSV
    result_file = os.path.join(app.config['UPLOAD_FOLDER'], "value_distribution.csv")
    result_df.to_csv(result_file, index=False)
    print(f"Results saved to: {result_file}")

    # Generate Plotly figure
    fig = px.bar(
        result_df,
        x="Value",
        y="Count",
        title="Value Count Distribution",
        labels={"Value": "Genomic Value", "Count": "Count"},
        text="Count",
    )
    fig.update_traces(textposition='outside', marker_color='blue')

    # Convert Plotly figure to HTML
    figure_html = fig.to_html(full_html=False)

    return render_template(
        "analyze.html",
        result_file="value_distribution.csv",
        tables=result_df.to_html(classes="table table-striped", index=False),
        figure_html=figure_html,
    )

if __name__ == "__main__":
    app.run(debug=True)
