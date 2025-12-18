# Sample Data for Social Media Analytics Platform

## Overview
This repository includes sample data to help you get started with the Social Media Analytics Platform. The sample data demonstrates the expected format and allows you to immediately see charts and analytics in action.

## Sample Files
- `sample_posts.csv` - Contains 10 sample social media posts with realistic metrics

## Data Schema
The CSV files follow this schema:

| Column | Description |
|--------|-------------|
| post_id | Unique identifier for each post |
| timestamp | Date and time of post (YYYY-MM-DD HH:MM:SS) |
| caption | Post caption/text content |
| likes | Number of likes received |
| comments | Number of comments received |
| shares | Number of shares/reposts |
| saves | Number of times post was saved |
| impressions | Total number of times post was displayed |
| reach | Unique number of people who saw the post |
| follower_count | Total follower count at time of post |
| audience_gender | Primary audience gender (Male/Female/Mixed) |
| audience_age | Primary audience age group |
| location | Geographic location of post |
| hashtags | Comma-separated list of hashtags used |
| media_type | Type of media (Image/Video/Carousel/Link) |

## Loading Sample Data
To load the sample data into the platform:

1. Start the dashboard: `streamlit run professional_dashboard.py`
2. Navigate to the Upload section
3. Upload the `sample_posts.csv` file
4. The data will be processed and charts will populate automatically

## Using Your Own Data
To use your own social media data:

1. Format your data to match the schema above
2. Save as a CSV file
3. Upload through the dashboard interface
4. The platform will automatically process and visualize your data

Note: The platform supports various CSV formats from Instagram, Facebook, and other social platforms through its adaptive data processor.