var websocket = require("websocket").server;

var https = require("https");
var fs = require("fs");


var creds = {key:fs.readFileSync("./ssl/https.key"),cert:fs.readFileSync("./ssl/https.crt")}

var port=8001;

var srv = https.createServer(creds,function(req,res){
	console.log("request: "+req);
	res.writeHead(404);
	res.end();
}).listen(port,function(){console.log("listening")});

var WebServ = new websocket({httpServer:srv});

WebServ.on("request",function(req){
	var conn = req.accept("echo-protocol",req.origin);
	conn.on('message',function(msg){
		conn.send("hello");
	});
});
