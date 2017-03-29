module.exports=function(grunt){
	grunt.initConfig({
		concat:{
			dist:{
				src:[],
				dest:'',
			}
		}
	});

	grunt.loadNpmTasks("grunt-contrib-concat");
}
