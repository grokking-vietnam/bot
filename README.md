# Grokking Bot
This is for development of Grokking Bot
# Set up
1. Install Python virtual environment
```
sudo pip install virtualenv
```
2. Create your own virtual env
```
mkdir .venv
virtualenv .venv
source .venv/bin/activate
```
3. Install python dependencies
```
pip install -r requirements.txt
```
4. Run the application

#### for welcome.py
```
API_TOKEN=<api_token> python welcome.py --channel=<channel>
```

#### for jobs_post.py
```
API_TOKEN=<api_token> CLIENT_ID=<client_id> CLIENT_SECRET=<client_secret> python jobs_post.py --channel=<channel>
```