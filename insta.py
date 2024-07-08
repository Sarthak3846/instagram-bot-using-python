from instabot import Bot 
import config 
import schedule 
import time
import logging
import random

bot = Bot()
logging.basicConfig(level=logging.INFO, filename='instabot.log', filemode='a', format= '%(name)s - %(levelname)s - %(message)s')

def login():
    bot.login(username = config.USERNAME, password=config.PASSWORD)
def logout():
    bot.logout()

def upload_photo(photo_path, caption):
    bot.upload_photo(photo_path, caption= caption)

def follow_user(username):
    bot.follow(username)

def like_post(post_url):
    bot.like(post_url)

def comment_on_post(post_url, comment):
    bot.comment(post_url, comment)

def schedule_posting(photo_path, caption, post_time):
    schedule.every().day.at(post_time).do(upload_photo, photo_path, caption)
    while True:
        schedule.run_pending()
        time.sleep(1)

def unfollow_non_followers():
    """Unfollow users who do not follow you back."""
    non_followers = set(bot.following) - set(bot.followers)
    for user in non_followers:
        bot.unfollow(user)
        random_delay()

def like_post_by_hashtag(hashtag, count = 10):
    posts = bot.get_hashtag_medias(hashtag)
    for post in posts[:count]:
        bot.like(post)
        random_delay()

def like_posts_by_hashtag(hashtag, count=10):
    """Like posts based on a specific hashtag."""
    posts = bot.get_hashtag_medias(hashtag)
    for post in posts[:count]:
        bot.like(post)
        random_delay()

def random_delay(min_seconds=30, max_seconds=120):
    """Introduce a random delay to mimic human behavior."""
    time.sleep(random.randint(min_seconds, max_seconds))

def comment_on_posts_by_hashtag(hashtag, comment, count=10):
    """Comment on posts based on a specific hashtag."""
    posts = bot.get_hashtag_medias(hashtag)
    for post in posts[:count]:
        bot.comment(post, comment)
        random_delay()

def auto_follow_by_hashtag(hashtag, count=10):
    """Auto-follow users based on a specific hashtag."""
    users = bot.get_hashtag_users(hashtag)
    for user in users[:count]:
        bot.follow(user)
        random_delay()

def safe_execute_with_delay(func, delay=60):
    """Execute a function safely with a delay to avoid being flagged as a bot."""
    try:
        func()
        time.sleep(delay)
    except Exception as e:
        logging.error(f'Error executing {func.__name__}: {e}')

def daily_routine():
    """Perform a daily routine of Instagram automation tasks."""
    login()
    safe_execute_with_delay(lambda: upload_photo('path/to/photo.jpg', 'Daily post caption'))
    safe_execute_with_delay(lambda: auto_follow_by_hashtag('yourhashtag', 10))
    safe_execute_with_delay(lambda: like_posts_by_hashtag('anotherhashtag', 10))
    safe_execute_with_delay(lambda: comment_on_posts_by_hashtag('yetanotherhashtag', 'Nice post!', 5))
    safe_execute_with_delay(unfollow_non_followers)
    logout()

# Example usage
if __name__ == "__main__":
    daily_routine()