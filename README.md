# Flight Delay Prediction

A Django web application that predicts flight delays using a trained machine-learning model. Users enter flight details (airline, source, destination, and schedule) and the app returns a delay prediction in real time.

## Features
- Django web interface for entering flight details and viewing predictions
- Trained ML model (`delay_model.pkl`) with label encoders for airline, source, and destination
- Real-time delay prediction served through the web app

## Tech Stack
- Python, Django
- scikit-learn, pandas (model training)
- HTML / Django templates (frontend)

## Project Structure
- `manage.py` — Django entry point
- `myapp/` — application logic and views
- `templates/` — HTML templates
- `delay_model.pkl`, `*_enc.pkl` — trained model and encoders

## Running Locally

Then open http://127.0.0.1:8000 in your browser.
