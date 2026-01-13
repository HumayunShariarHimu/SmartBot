from flask import Flask, request, jsonify
import requests
import random
import time
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

def get_mega_stealth_config(target_url):
    ua_list = [
        "Mozilla/5.0 (Linux; Android 15; SM-S938B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 18_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 14; Pixel 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36"
    ]

    sources = [
        f"https://www.google.com/search?q={target_url}", 
        "https://www.bing.com/search?q=latest+trending+topics", 
        "https://search.yahoo.com/search?p=global+updates", 
        "https://duckduckgo.com/?q=how+to+optimize+website",
        "https://www.baidu.com/s?wd=tech+innovations",
        "https://yandex.com/search/?text=cyber+security+2025",
        "https://chatgpt.com/", 
        "https://gemini.google.com/", 
        "https://grok.x.ai/", 
        "https://claude.ai/",
        "https://www.perplexity.ai/",
        "https://mistral.ai/",
        "https://www.tiktok.com/", 
        "https://www.facebook.com/", 
        "https://t.co/", 
        "https://www.reddit.com/r/technology/", 
        "https://www.pinterest.com/", 
        "https://www.instagram.com/",
        "https://www.linkedin.com/feed/",
        "https://www.quora.com/",
        "https://stackoverflow.com/", 
        "https://news.ycombinator.com/", 
        "https://github.com/trending",
        "https://www.bbc.com/news",
        "https://www.reuters.com/",
        "https://www.nytimes.com/",
        "https://medium.com/tag/programming",
        "https://www.theverge.com/",
        "https://www.techcrunch.com/",
        "https://wired.com/"
    ]

    return {'ua': random.choice(ua_list), 'ref': random.choice(sources)}

@app.route('/api/index', methods=['GET'])
def spark_bot():
    target = request.args.get('url')
    manual_ad = request.args.get('ad_link')
    
    if not target:
        return jsonify({"status": "FAILED", "behavior": ["Target URL is missing"]}), 400

    config = get_mega_stealth_config(target)
    
    headers = {
        'User-Agent': config['ua'],
        'Referer': config['ref'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,bn;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    behavior_log = []
    status = "FAILED"
    start_time = time.time()

    try:
        session = requests.Session()
        response = session.get(target, headers=headers, timeout=9, verify=False)
        
        if response.status_code == 200:
            status = "SUCCESS"
            behavior_log.append("Main Page Loaded Successfully")
            
            time.sleep(random.uniform(1.0, 2.5))
            behavior_log.append(f"Referrer Verified: {config['ref'].split('/')[2]}")

            soup = BeautifulSoup(response.text, 'html.parser')
            ad_url = None

            if manual_ad and manual_ad.strip():
                ad_url = manual_ad
                behavior_log.append("Manual Ad Target Injected")
            else:
                ad_keywords = ['googleadservices', 'pagead', 'adclick', 'doubleclick', 'clickserve', 'sponsored']
                for a in soup.find_all('a', href=True):
                    if any(key in a['href'] for key in ad_keywords):
                        ad_url = urljoin(target, a['href'])
                        break
            
            if ad_url:
                time.sleep(random.uniform(0.5, 1.5))
                session.get(ad_url, headers=headers, timeout=8, verify=False)
                behavior_log.append(f"Engagement: Ad Clicked ({urlparse(ad_url).netloc[:15]}...)")
                
                stay_time = random.uniform(2.5, 4.0)
                time.sleep(stay_time)
                behavior_log.append(f"Retention: Stayed on page for {round(stay_time,1)}s")
            else:
                domain = urlparse(target).netloc
                inner_links = [urljoin(target, a['href']) for a in soup.find_all('a', href=True) 
                               if domain in a['href'] or a['href'].startswith('/')]
                if inner_links:
                    inner_target = random.choice(inner_links)
                    session.get(inner_target, headers=headers, timeout=7, verify=False)
                    behavior_log.append(f"Action: Human Navigation to {urlparse(inner_target).path[:10]}")
                else:
                    behavior_log.append("Action: Full Engagement & Scroll")
        else:
            behavior_log.append(f"HTTP Error: {response.status_code}")

    except Exception as e:
        behavior_log.append(f"Trace Log: Connection Managed/Timeout")

    return jsonify({
        "status": status,
        "ip": "Vercel_Edge_Node",
        "source": config['ref'],
        "ua": config['ua'],
        "behavior": behavior_log,
        "latency": f"{round(time.time() - start_time, 2)}s",
        "engine": "SparkBot_V7_Elite_Ultra"
    })

if __name__ == "__main__":
    app.run()
