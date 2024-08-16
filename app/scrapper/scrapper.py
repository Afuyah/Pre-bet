import requests
from bs4 import BeautifulSoup
from flask import render_template, redirect, url_for, flash
from . import scraper
from ..extensions import celery, db
from ..models import MatchPrediction

@scraper.route('/scrape', methods=['GET', 'POST'])
def scrape():
    scrape_and_analyze.delay()
    flash('Scraping and analysis started!', 'info')
    return redirect(url_for('main.dashboard'))

@celery.task
def scrape_and_analyze():
    urls = [
        # Add your 100 URLs here
    ]
    predictions = []

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Example of scraping logic, adjust according to the site's structure
        match_data = soup.find_all('div', class_='match-prediction')
        for match in match_data:
            prediction = {
                'team_a': match.find('span', class_='team-a').text,
                'team_b': match.find('span', class_='team-b').text,
                'prediction': match.find('span', class_='prediction').text
            }
            predictions.append(prediction)

    # Analysis logic using AI/ML models
    # Here you could use scikit-learn, TensorFlow, or other libraries to analyze the data

    # Example: simple majority vote for the most popular prediction
    from collections import Counter
    popular_predictions = Counter([p['prediction'] for p in predictions]).most_common(100)

    for pred in popular_predictions:
        match_pred = MatchPrediction(
            team_a=pred['team_a'],
            team_b=pred['team_b'],
            prediction=pred['prediction']
        )
        db.session.add(match_pred)

    db.session.commit()

    # Store predictions in the database