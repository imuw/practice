var https=require("https");
var fs = require("fs");

var express = require("express");
var app = express();


var creds = {key: fs.readFileSync("./ssl/key.pem"),cert:fs.readFileSync("./ssl/cert.pem")};
var port=8001;
app.get('/',function(req,res){
	console.log(req);
	res.send("hello");
});

var serv = https.createServer(creds,app).listen(port);


