var redis = require("redis");
var bluebird = require("bluebird");
var options = {
	server:'',
	port:''
};
var redClient = redis.createClient(options);

redClient.set("key1","value1",redis.print);
