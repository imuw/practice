var https =require("https");
var fs = require("fs");
var ws = require("ws").Server;

var options={key:fs.readFileSync("./ssl/https.key"),cert:fs.readFileSync("./ssl/https.crt")};
var port = 8001;

var express= require("express");
var app = express();

var serv = https.createServer(options,app).listen(port);
var WebServ = new ws({server:serv});


WebServ.on("connection",function(wServ){
	console.log(wServ);
	wServ.on("message",function(msg){
		console.log(msg);
	});
	ws.send("hello");
});


