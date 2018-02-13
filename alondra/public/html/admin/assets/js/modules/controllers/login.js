define(['angular'],function(angular){
 	angular.module('app.controllers.login', [])
 	.controller('LoginCtrl', 
	[ '$scope','$state','$translate','Login','$cookies',
	  function ($scope,$state,$translate,Login,$cookies) 
	  {
	  	
	  	if($cookies.get('access_token'))
	  		{
	  			$state.go('root.posts');
	  		}
	  	$scope.model = {'username':'','password':''};
	  	$scope.login = function()
	  	{
	  		////login.logout();


	  		Login.login(
	  			$scope.model.username,
	  			$scope.model.password
	  		).then(function successCallback(response) 
	        {
	        	
	        	if(response.data.token!=='undefined')
	        	{

	        		var expireDate = new Date(response.data.expires_in*1000);
 					
	        		$cookies.put(
	        			'access_token',
	        			response.data.token,
	        			{path:'/'}
	        			);
	        	
	        		
	        		
	        		$state.go('root.posts');
	        	}
	            
	        }, function errorCallback(response) {});;
	  	}
	  	
	  	//
	  }]).controller('LogoutCtrl',[
	'$scope','$state','$translate','Login','$cookies',
	  function ($scope,$state,$translate,Login,$cookies) 
	  {
	  	$cookies.remove('access_token');
	  	$state.go('login.screen');

	}])
  
});


