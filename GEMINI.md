# GEMINI.md

## Project Overview

This is a "Smart Procurement" system designed for factories. It helps monitor real-time market prices of raw materials, forecast price trends using AI, and provides recommendations on the optimal time to purchase. The system also includes features for inventory management, vendor comparison, and a purchase order system.

The application is composed of a Flask backend that serves a REST API and a Streamlit frontend for the user interface. Data is stored in CSV and JSON files.

## Building and Running

To build and run this project, follow these steps:

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Backend:**
    ```bash
    python app.py
    ```
    The backend will be available at `http://localhost:5000`.

3.  **Run the Frontend:**
    ```bash
    streamlit run dashboard.py
    ```
    The frontend will be available at `http://localhost:8501`.

## Development Conventions

*   **Configuration:** Project configuration is managed in `config.py`. Sensitive information or environment-specific settings can be placed in a `.env` file.
*   **Backend:** The Flask backend in `app.py` uses APScheduler to run background tasks for updating prices and forecasts.
*   **Frontend:** The Streamlit dashboard in `dashboard.py` interacts with the backend through the REST API.
*   **Forecasting:** The `models/forecast_model.py` file contains the Facebook Prophet model for price forecasting.
*   **Data:** All data files are stored in the `data/` directory.
*   **Utilities:** The `utils/` directory contains various helper modules for tasks like data generation, notifications, and PDF exporting.
