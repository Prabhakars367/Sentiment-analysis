### YouTube Comment Sentiment Analysis

#### Overview:
This script allows you to analyze the sentiments of comments on a YouTube video. It fetches comments using the YouTube Data API, filters them for relevance, analyzes their sentiments using the VADER sentiment analysis tool, and visualizes the results in a bar chart. The relevant comments are also saved to a text file for further review.

#### Key Functionalities:
1. **Extract Video ID**: The script extracts the video ID from a provided YouTube URL.
2. **Fetch Video Details**: It retrieves the channel ID and title of the video using the YouTube Data API.
3. **Fetch Comments**: The script fetches up to 100 comments from the specified YouTube video.
4. **Filter Relevant Comments**: It filters out spammy or irrelevant comments, such as those containing hyperlinks or excessive emojis.
5. **Sentiment Analysis**: Using VADER (Valence Aware Dictionary and sentiment Reasoner), the script performs sentiment analysis on the filtered comments.
6. **Save Comments to File**: Relevant comments are saved to a text file for further review.
7. **Visualization**: The script creates a bar chart to visualize the distribution of positive, negative, and neutral comments.

#### Script Breakdown:
1. **Initialization**:
   - Imports necessary libraries.
   - Initializes the YouTube Data API with the provided API key.

2. **Helper Functions**:
   - `get_video_id(URL)`: Extracts the video ID from a YouTube URL.
   - `get_video_details(video_id)`: Retrieves video details using the YouTube Data API.
   - `get_comments(video_id, max_results=100)`: Fetches comments from a YouTube video.
   - `filter_relevant_comments(comments, threshold_ratio=0.65)`: Filters comments to remove spammy or irrelevant content.
   - `analyze_sentiments(comments)`: Analyzes the sentiments of the comments using VADER.

3. **Main Functionality**:
   - Takes the YouTube video URL as input from the user.
   - Extracts the video ID and retrieves video details.
   - Fetches comments from the video.
   - Filters relevant comments and analyzes their sentiments.
   - Saves relevant comments to a text file.
   - Displays sentiment analysis results, including the average polarity and comments with the most positive and negative sentiments.
   - Creates a bar chart to visualize the sentiment distribution of the comments.

#### How to Use:
1. **Input**: Provide the YouTube video URL when prompted.
2. **Output**:
   - The script prints the video ID, channel ID, video title, and first 5 relevant comments.
   - It saves all relevant comments to a file named `ytcomments.txt`.
   - It prints the average polarity of the comments and indicates whether the overall sentiment is positive, negative, or neutral.
   - It prints the comments with the most positive and negative sentiments.
   - It displays a bar chart showing the count of positive, negative, and neutral comments.

#### Example Usage:
1. Run the script.
2. Enter the YouTube video URL when prompted.
3. Review the printed output for video details and sentiment analysis results.
4. Check the `ytcomments.txt` file for the saved relevant comments.
5. Observe the bar chart displaying the sentiment distribution of the comments.

This script provides a comprehensive tool for analyzing the sentiments of comments on a YouTube video, offering valuable insights into viewer feedback.
