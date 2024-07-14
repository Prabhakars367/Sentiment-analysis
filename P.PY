from googleapiclient.discovery import build
import re
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

API_KEY = 'AIzaSyAy_Xd8I6JJl_ZLsFEsod9cMd8m_tZ56lw'

# Initialize YouTube API
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_id(url):
    """Extract the video ID from a YouTube URL."""
    if 'v=' in url:
        return url.split('v=')[-1][:11]
    else:
        return url.split('/')[-1][:11]

def get_video_details(video_id):
    """Fetch video details using YouTube API."""
    response = youtube.videos().list(part='snippet', id=video_id).execute()
    if 'items' in response and response['items']:
        snippet = response['items'][0]['snippet']
        return snippet['channelId'], snippet['title']
    return None, None

def get_comments(video_id, max_results=100):
    """Fetch comments from a YouTube video."""
    comments = []
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=max_results,
        textFormat='plainText'
    ).execute()

    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        if 'nextPageToken' in response:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=max_results,
                textFormat='plainText',
                pageToken=response['nextPageToken']
            ).execute()
        else:
            break

    return comments

def filter_relevant_comments(comments, threshold_ratio=0.65):
    """Filter comments to remove spammy or irrelevant content."""
    hyperlink_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    relevant_comments = []

    for comment in comments:
        comment_text = comment.lower().strip()
        emojis = emoji.emoji_count(comment_text)
        text_characters = len(re.sub(r'\s', '', comment_text))

        if any(char.isalnum() for char in comment_text) and not hyperlink_pattern.search(comment_text):
            if emojis == 0 or (text_characters / (text_characters + emojis)) > threshold_ratio:
                relevant_comments.append(comment_text)
                
    return relevant_comments

def analyze_sentiments(comments):
    """Analyze the sentiments of the comments."""
    analyzer = SentimentIntensityAnalyzer()
    polarity = []
    positive_comments = []
    negative_comments = []
    neutral_comments = []

    for comment in comments:
        score = analyzer.polarity_scores(comment)
        polarity.append(score['compound'])
        if score['compound'] > 0.05:
            positive_comments.append(comment)
        elif score['compound'] < -0.05:
            negative_comments.append(comment)
        else:
            neutral_comments.append(comment)

    return polarity, positive_comments, negative_comments, neutral_comments

def main():
    # Taking input from the user and extracting the video ID
    video_url = input('Enter YouTube Video URL: ')
    video_id = get_video_id(video_url)
    print("Video ID: " + video_id)

    # Getting the channel ID and title of the video
    channel_id, video_title = get_video_details(video_id)
    if not channel_id:
        print("No video found with the provided ID. Please check the ID and try again.")
        return

    print(f"Channel ID: {channel_id}")
    print(f"Video Title: {video_title}")

    # Fetching comments
    comments = get_comments(video_id)
    if not comments:
        print("No comments found for the video.")
        return

    # Filtering relevant comments
    relevant_comments = filter_relevant_comments(comments)
    print(f"First 5 relevant comments:\n{relevant_comments[:5]}")

    # Analyzing sentiments
    polarity, positive_comments, negative_comments, neutral_comments = analyze_sentiments(relevant_comments)

    # Saving relevant comments to a file
    with open("ytcomments.txt", 'w', encoding='utf-8') as f:
        for comment in relevant_comments:
            f.write(comment + "\n")
    print("Comments stored successfully!")

    # Sentiment analysis results
    avg_polarity = sum(polarity) / len(polarity)
    print("Average Polarity:", avg_polarity)
    if avg_polarity > 0.05:
        print("The Video has got a Positive response")
    elif avg_polarity < -0.05:
        print("The Video has got a Negative response")
    else:
        print("The Video has got a Neutral response")

    print("The comment with most positive sentiment:", relevant_comments[polarity.index(max(polarity))], 
          "with score", max(polarity), "and length", len(relevant_comments[polarity.index(max(polarity))]))
    print("The comment with most negative sentiment:", relevant_comments[polarity.index(min(polarity))], 
          "with score", min(polarity), "and length", len(relevant_comments[polarity.index(min(polarity))]))

    # Sentiment counts
    positive_count = len(positive_comments)
    negative_count = len(negative_comments)
    neutral_count = len(neutral_comments)

    # Labels and data for bar chart
    labels = ['Positive', 'Negative', 'Neutral']
    comment_counts = [positive_count, negative_count, neutral_count]

    # Creating bar chart
    plt.bar(labels, comment_counts, color=['blue', 'red', 'grey'])

    # Adding labels and title to the plot
    plt.xlabel('Sentiment')
    plt.ylabel('Comment Count')
    plt.title('Sentiment Analysis of Comments')

    # Displaying the chart
    plt.show()

if __name__ == "__main__":
    main()
