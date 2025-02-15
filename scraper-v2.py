#Install packages 
#python3 -m venv scraper
#source scraper/bin/activate 
#pip3 install praw 
#pip3 install pandas
#pip3 install openpyxl

import os
import praw
import openai
from datetime import datetime, timezone

# ✅ Load API keys from environment variables
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Ensure all API keys are loaded correctly
if not all([CLIENT_ID, CLIENT_SECRET, USER_AGENT, OPENAI_API_KEY]):
    raise ValueError("❌ Missing API keys! Make sure all API keys are set as environment variables.")

# ✅ Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# ✅ Initialize Reddit API
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# ✅ Define the subreddit
subreddit = reddit.subreddit("oscp")

# ✅ Fetch OSCP "Passed" Posts from 2023 & 2024
search_query = "passed"
start_date = datetime(2023, 1, 1, tzinfo=timezone.utc).timestamp()  # Start of 2023
end_date = datetime(2024, 12, 31, 23, 59, 59, tzinfo=timezone.utc).timestamp()  # End of 2024

# ✅ Extract detailed, high-quality success stories
def is_useful_post(post):
    """Filters posts that are detailed and useful for OSCP preparation."""
    content = f"{post.title} {post.selftext}".lower()
    useful_keywords = [
        "study", "methodology", "privilege escalation", "active directory",
        "tools", "practice", "proving grounds", "htb", "time management",
        "exam strategy", "report writing", "buffer overflow", "initial foothold"
    ]
    
    # Ensure the post has substantial content and relevant keywords
    return any(keyword in content for keyword in useful_keywords) and len(post.selftext) > 700

# ✅ Collect posts from 2023 and 2024
posts = []
for post in subreddit.search(search_query, sort="new", time_filter="all"):  # Fetch all-time posts
    post_timestamp = post.created_utc  # Get post creation time
    if start_date <= post_timestamp <= end_date:  # Filter only 2023 & 2024 posts
        if is_useful_post(post):
            posts.append(post)

print(f"Collected {len(posts)} useful OSCP 'passed' posts from 2023 & 2024.")

# ✅ Save posts and replies to a text file
output_file = "oscp_useful_passed_posts.txt"
post_texts = []

with open(output_file, "w", encoding="utf-8") as f:
    for post in posts:
        post_info = f"Title: {post.title}\nBody: {post.selftext}\nURL: {post.url}\n"
        post_texts.append(post_info)
        f.write(post_info)

        # Fetch and save comments for additional insights
        post.comments.replace_more(limit=0)  # Load all top-level comments
        for comment in post.comments.list():
            comment_info = f"Reply: {comment.body}\n\n"
            post_texts.append(comment_info)
            f.write(comment_info)

print(f"Saved high-quality OSCP 'passed' posts from 2023 & 2024 to {output_file}")

# --- AI-Based Analysis Using OpenAI ---
def analyze_oscp_success(posts_text):
    prompt = f"""
    You are analyzing high-quality OSCP success stories. Your goal is to extract **detailed, actionable insights** 
    for future students, based on **real-world study techniques, tools, and strategies** that worked.

    **Focus on:**
    - **Hands-on practice environments** (HTB, Proving Grounds, home labs, retired OSCP boxes).
    - **Effective enumeration techniques** (ports, services, users, shares).
    - **Privilege escalation strategies** (Windows & Linux misconfigurations, kernel exploits).
    - **Active Directory attack techniques** (kerberoasting, ASREPRoasting, BloodHound analysis).
    - **Common mistakes people made and how they overcame them.**
    - **Time management tips during the exam.**
    - **How candidates handled stress and setbacks.**
    - **Exam strategy for tackling the AD set and standalone boxes.**
    - **Effective report writing techniques that saved candidates time.**

    **🚀 Structure your response like this:**
    
    1️⃣ **Key Study Strategy (e.g., Active Directory Focus)**
    - 🔹 **Recommended Resources:** (e.g., Derron C’s YouTube series, TryHackMe, HackTheBox Pro Labs)
    - 🔹 **Tool Used:** (e.g., `BloodHound`, `CrackMapExec`, `Mimikatz`)
    - 🔹 **Strategy:** (e.g., "Students practiced building attack paths using BloodHound and CrackMapExec.")
    - 🔹 **Example:** ("One candidate gained an initial foothold using ASREPRoasting and moved laterally with Pass-The-Hash.")

    **🚀 Avoid vague responses—focus only on specific techniques that appeared in multiple discussions.**

    **📌 Here are OSCP success stories and discussions:**
    {posts_text}

    **Extract exactly 4 specific study techniques or best practices that appear most frequently.**
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use "gpt-3.5-turbo" if hitting rate limits
        messages=[{"role": "system", "content": "You are a cybersecurity mentor."},
                  {"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response["choices"][0]["message"]["content"]

# ✅ Process in chunks if needed (to avoid API limits)
full_text = "\n".join(post_texts)[:5000]  # Limit to first 5000 characters

# ✅ Get AI analysis
oscp_analysis = analyze_oscp_success(full_text)

# ✅ Save AI results
ai_output_file = "oscp_success_analysis.txt"
with open(ai_output_file, "w", encoding="utf-8") as f:
    f.write(oscp_analysis)

print("\n✅ AI Analysis Completed! Check 'oscp_success_analysis.txt' for results.")
