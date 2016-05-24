from urllib import urlopen
import json

CLIENT_ID = "2d7d4b83a596ae06623c"
CLIENT_SECRET = "9167a622887a9f5a468d49ee39142140750141f9"

API_URL = "https://api.github.com/repos/awesome-jobs/jobs/issues" \
			+ "?client_id=" + CLIENT_ID \
			+ "&client_secret=" + CLIENT_SECRET

if __name__ == "__main__":
	response = urlopen(API_URL)
	jsonRaw = response.read()
	jsonData = json.loads(jsonRaw)

	jobs = []

	for job in jsonData:
		item = {}
		item['title'] = job['title']
		item['html_url'] = job['html_url']
		item['labels'] = []
		for label in job['labels']:
			item['labels'].append(label['name'])

		jobs.append(item.copy())

	print len(jobs)