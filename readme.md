# 🐦 Twitter Timeline Scraper

A Python-based command-line tool to fetch **all public tweets** from a given Twitter user and save them to a CSV file. Useful for downstream analytics like engagement analysis, clustering, or research.

---

## 📌 Features

- Fetches **all available public tweets** using Twitter API v2
- Handles **pagination**, **rate limits**, and **transient errors**
- Extracts:
  - Tweet ID
  - Created timestamp
  - Full text
  - Engagement metrics (likes, retweets, replies, quotes)
  - Media indicator (media/link presence)
- Outputs a clean, flat CSV
- Simple CLI interface and `.env` support for API keys

---

## 💠 Setup Instructions

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd twitter_scraper
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API keys to `.env`

Create a file named `.env` in the root directory:

```env
BEARER_TOKEN=your_twitter_api_bearer_token
```

You can generate this from the [Twitter Developer Portal](https://developer.x.com/en/portal/dashboard).

---

## ▶️ Usage

```bash
python twitter.py --username <twitter_handle> --output <filename.csv> --max <number_of_tweets>
```

### Example

```bash
python twitter.py --username elonmusk --output elon_tweets.csv --max 2000
```

This will create a CSV file `elon_tweets.csv` with up to 2000 of Elon Musk's public tweets.

---

## 📄 Output Format

The CSV will include the following columns:

| Column Name | Description                     |
| ----------- | ------------------------------- |
| Tweet ID    | Unique ID of the tweet          |
| Created At  | UTC timestamp of tweet creation |
| Likes       | Number of likes                 |
| Retweets    | Number of retweets              |
| Replies     | Number of replies               |
| Quotes      | Number of quote tweets          |
| Media       | Indicator: media / link / none  |
| Tweet       | Full text of the tweet          |

---

## 💡 Assumptions Made

- Only **public tweets** are accessible and fetched
- Rate limits (429 errors) are handled with **exponential backoff**
- Media detection is based on presence of `attachments` or `entities.urls`

---

## 📆 Dependencies

- [tweepy](https://www.tweepy.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [pandas](https://pandas.pydata.org/)

---


## 👨‍💻 Author

Dharani K\
[GitHub](https://github.com/daredevil-99) | [Email](mailto:kdharanikarur@gmail.com)
---


