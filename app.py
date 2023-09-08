from flask import Flask, render_template
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib.dates as mdates

app = Flask(__name__)

# Database setup
DB_FILE = 'sensor_data.db'

@app.route('/')
def index():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, temperature, humidity FROM sensor_data ORDER BY timestamp DESC LIMIT 60")
    data = cursor.fetchall()
    conn.close()

    timestamps = [row[0] for row in data]
    temperatures = [row[1] for row in data]
    humidity = [row[2] for row in data]

    # Convert timestamps to matplotlib date format
    time_series = [mdates.datestr2num(str(ts)) for ts in timestamps]

    # Create a plot with two y-axes
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot temperature on the left y-axis
    ax1.plot(time_series, temperatures, label='Temperature (°C)', color='tab:red')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Temperature (°C)', color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    # Create a second y-axis for humidity on the right
    ax2 = ax1.twinx()
    ax2.plot(time_series, humidity, label='Humidity (%)', color='tab:blue')
    ax2.set_ylabel('Humidity (%)', color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    # Format x-axis with timestamps
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
    plt.gcf().autofmt_xdate()  # Rotate x-axis labels for readability

    # Display legends for both datasets
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.grid()

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Embed the plot in the HTML template
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
