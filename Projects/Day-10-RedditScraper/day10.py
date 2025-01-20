import requests

def scrape_subreddit(subreddit, limit=5):
    url = f"https://old.reddit.com/r/{subreddit}/top/.json?limit={limit}"
    headers = {"User-Agent": "Python:RedditScraper:v1.0 (by /u/yourusername)"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return

    data = response.json()
    posts = data["data"]["children"]

    for i, post in enumerate(posts, 1):
        post_data = post["data"]
        title = post_data["title"]
        author = post_data["author"]
        score = post_data["score"]
        url = post_data["url"]

        print(f"{i}. {title}")
        print(f"   Author: {author} | Score: {score}")
        print(f"   URL: {url}\n")

if __name__ == "__main__":
    subreddit = input("Enter subreddit: ")
    scrape_subreddit(subreddit, limit=5)
