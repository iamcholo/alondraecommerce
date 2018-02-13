define(['angular','jquery'],function(angular,jquery){
 	angular.module('app.controllers.media_album', [])
 	.controller('MediaAlbumEditCtrl', 
	[ '$scope','$state','$translate','$stateParams','Tags','Category','MediaAlbum',
	  function ($scope,$state,$translate,$stateParams,Tags,Category,MediaAlbum) 
	  {

	  
	  	$scope.model = {
	  		'title':''
	  	} 


	  	MediaAlbum.Get( $stateParams.id ).then(function successCallback(response){
	  			$scope.model.title = response.data.title;
	  		

			}, function errorCallback(response) {});
	  	

	

	  	$scope.Save = function()
	  	{
		  	$scope.model.id = $stateParams.id;

		 	MediaAlbum.Update($scope.model);
		}

	}]).controller('MediaAlbumNewCtrl', 
	[ '$scope','$state','$translate','$stateParams','Tags','Category','MediaAlbum',
	  function ($scope,$state,$translate,$stateParams,Tags,Category,MediaAlbum) 
	  {
	  
	  	$scope.model = {
	  		'title':''
	  	} 

	  	$scope.Save = function()
	  	{
	  		
	  		MediaAlbum.New($scope.model).then(function successCallback(response)
		    {
		    	$state.go('root.media_album_edit',{'id':response.data.id});

		    }, function errorCallback(response) {});;
	  	}
	

	  
	}]);
  
});


