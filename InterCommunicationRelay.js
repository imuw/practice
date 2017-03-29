module.exports={
	relayManager : {
		relayClients:[],
		primary:function(obj){
			relayClients.unshift(obj);
		},
		attach: function(client){
			relayClients.push(client);
		},

		setPrimary:function(prim){
			primary(prim);
		},

		interchange: function(){
			relayClients.forEach(function(client){
				client.InterChange(relayClients.filter(function(c){return c != client});
			});
		}
	},

	client:{
		id:null
		name:null,
		sdp:null,
		webSocketServer:null,
		InterChange:function(lstClients){

		},
	}
};
