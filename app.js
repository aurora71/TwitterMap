var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var es = require('elasticsearch');
http.listen(8081, function(){
  console.log('listening on *:8888');
});
var database = new es.Client({
    host: 'search-twittmap-6kcrspxukie6wotjhqthjgon4u.us-east-1.es.amazonaws.com:80'
});
app.get('/', function(req, res){
  res.sendfile('app.html');
});

io.on('connection', function(socket){
	socket.emit('First message', {message: 'Connected!', id: socket.id});
	socket.on('transferData', function(data) {
		var key = data.key;	
		console.log(key);
		database.search({
			  q: key
			}).then(function (body) {
			  var hits = body.hits.hits;
			  console.log(hits);
			  socket.emit('informationTransmission', {data: hits});

			}, function (error) {
			  console.trace(error.message);
			});
	 });

	 socket.on('serachRegion', function(data){
	 	console.log("received command");
	 	console.log(data.la);
	 	console.log(data.len);
	 	var lat = data.la;
	 	var lon = data.len;
		database.search({
			"index" : "twittmap",
			"tpye" : "tweets",
			"body" : {
			    "query": {
			    "filtered": {
			      "query": {
			        "match_all": {}
			      },
			      "filter": {
			      	"geo_distance" : {
			      		"distance" : "200km",
			      		"tweets.geo" : {
			      			"lat" : data.la,
			      			"lon" : data.len
			      		}
			                    
			      	}
			      }
			    }
			  }
			}

			}).then(function (resp) {
			    var hits = resp.hits.hits;
			    console.log(hits.length);
			    socket.emit('getResponse', {data: hits});
			   

			}).catch(function (error) {
			    console.log("Error on geo_distance (coordiates)");
			    console.log(error);
			});
		}); 

	
});

