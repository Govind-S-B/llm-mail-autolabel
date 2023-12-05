import os
import requests
import json

# API endpoint URL
url = "http://localhost:11434"

prompt = """

You are an expert email categorizing AI model that can understand and think about the user intentions behind an email and label things accordingly

Given the following user 

```
I am a Software Engineering Student and I am right now on the lookout for work oppoprtunitites and advancing my carrer.
I want my mails to be focused on that goal and streamlined, I really dont want to see spammy promotional mails
```

According to the label specifications below

"Job" - any work related email should go here
"Personal" - any personal communication from friends or family
"Trashy" - All Promotional Emails and Spam
"Bills" - All invoices or finance related things

For the email content
```
Hello, dnivog.

You are welcome to register and compete in Codeforces Round 913 (Div. 3). It starts on Tuesday, December, 5, 2023 14:35 (UTC). The contest duration is 2 hours 15 minutes. The allowed programming languages are C/C++, Pascal, Java, C#, Python, Ruby, Perl, PHP, Haskell, Scala, OCaml, Go, D, JavaScript, Rust and Kotlin.

Div. 3 rounds are designed especially for participants with a rating below 1600. We invite you to participate in the competition!

The goal of such rounds is to help beginner participants to gain skills and to get new knowledge in a real contest. You can read the details in this post dedicated to them. In short:

Not only real problems, but also exercises can be used.
Our main goal is to give nice training problems, so we do not care much about the innovativeness of the problems.
Often the formal text of the statements.
Rated for participant with the rating below 1600.
ICPC rules + 12-hour open hacking phase.
Untrusted participants are not included in the official ranklist.
The round will be held on the rules of Educational Rounds, so read the rules (here) beforehand. The round will be for newcomers and participants with a rating below 1600. Want to compete? Do not forget to register for the contest and check your handle on the registrants page. The registration will be open for the whole contest duration.

If you have any questions, please feel free to ask me on the pages of Codeforces. If you no longer wish to receive these emails, click https://codeforces.com/unsubscribe/contests/49a4594bc46bb9a8d383b2bf91dea7b0f3d201a5/ to unsubscribe.

Wish you high rating,
MikeMirzayanov and Codeforces team
```

Classify the email content into a json format
{
"label": <one of the labels specified earlier>
}

Return only the json

"""

# Send the request
response = requests.post(
            url=f"{url}/api/generate/",
            headers={"Content-Type": "application/json"},
            json={'model': 'openhermes2.5-mistral', 'prompt': prompt, 'format': 'json', 'options': {'temperature': 0, 'top_k': 10}, 'stream': False} ,
        )

print(json.loads(response.text)["response"])
