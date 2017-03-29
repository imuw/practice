#!/bin/env node
var ws = require("ws").Server;
var wss = new ws({port:9000});

var clients=[];
var sender;
var reciever;

wss.on('connection',function connection(ws){
	clients.push(ws);
	ws.on('message',function incoming(message){
		console.log('recieved: %s',message);
		console.log(message.data);
		
	});
	ws.send("hello from server");
	clients[0].send("hello from list");
});




//wss.on('message',function(soc){wss.client[0].send("hello from server")})
	

/*
var conns = []
var server = ws.createServer(function(conn){

conn.on('text',function(message){
	conns.push(conn)
	respond();
//console.log(server.connections);
})
//conn.on('close',function(){respond()})
}).listen(9000);


function respond(){
	server.connections.forEach(function(connection){
		connection.emit("this is the server sending stuff");})
}

*/
