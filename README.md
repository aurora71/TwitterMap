# TwitterMap
The process of deploying TwittMap in ElasticBeanStalk
1. Create, configure Elasticsearch domain

2. Use Amazon ES regional endpoints for accessing the configuration API and domain-specific endpoints for accessing the search API

3. Create search indices. We extracted geo, text, time and user from Tweets stream and store these data in a search instance.
		geo geo_point
		text string
		time date
		user string

4. Create an instance and configure environment for TwittStream.py to get data form tweets stream.

5. Create a web UI with google map API for user to search tweets through 13 key words. Use socket.io to send key word to backend. And once the elasticsearch responce the query, it would send the json format data to front-end.

6. Visualize tweets in google map. When user click a key word in the box, all the tweets with key word in its text would be located with marder in the map. Click the marker, it would give the detailed information in a windowbox. 

7. Click the map, you could get tweets within 100km from the point you click on the map.

8. Deployed application on AWS Elastic Beanstalk.