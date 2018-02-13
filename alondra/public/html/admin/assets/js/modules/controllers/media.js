define(['angular','jquery'],function(angular,jquery){
 	angular.module('app.controllers.media', [])
 	.controller('MediaListCtrl', 
	[ '$scope','$state','$translate','Media','MediaAlbum','$interval',
	  function ($scope,$state,$translate, Media,MediaAlbum,$interval) 
	  {

	  	$scope.filteredTodos = [];
	  	$scope.itemsPerPage = 8;
	  	$scope.currentPage = 1;
	  	$scope.filteredTodosAlbum = [];
	  	$scope.itemsPerPageAlbum = 8;
	  	$scope.currentPageAlbum = 1;
		$scope.model = {'query':'','query_album':''};
		$scope.name = '';
		$scope.progress = 0;
	  	$scope.search = function()
	  	{	if($scope.model.query.length > 0)
	  		{
	  			$scope.todos = $scope.todos.filter(function(item){
	  				re = new RegExp($scope.model.query);
					return re.test(item.title) ;
				});
				$scope.figureOutTodosToDisplay(1);
	  		}else
	  		{
	  			$scope.makeTodos(); 
	  		}
	  		
	  	}
	  	$scope.search_album = function()
	  	{	if($scope.model.query_album.length > 0)
	  		{
	  			$scope.todos = $scope.todos_album.filter(function(item){
	  				re = new RegExp($scope.model.query_album);
					return re.test(item.title) ;
				});
				$scope.figureOutTodosToDisplayAlbum(1);
	  		}else
	  		{
	  			$scope.makeTodosAlbum(); 
	  		}
	  		
	  	}

		$scope.makeTodos = function()
		{
			$scope.todos = [];
			$scope.filteredTodos = [];
		    Media.list().then(function successCallback(response)
		    {
	         	angular.forEach(response.data, function(value, key){
				 	this.push({
			        	id: value.id,
				        title: value.title,
				        status: value.publish,
				        img:  value.image,
				        created: value.created,
				        modified: value.modified,
			      	});
			      	if(response.data.length-1 >= key)
			      	{
			      		$scope.figureOutTodosToDisplay(1);
			      	}
			      	
				},$scope.todos);
				
				$scope.figureOutTodosToDisplay(1);
				
        	}, function errorCallback(response) {});


		};

		$scope.makeTodosAlbum = function()
		{
			$scope.todos_album = [];
		    MediaAlbum.list().then(function successCallback(response)
		    {
	         	angular.forEach(response.data, function(value, key){
				 	this.push({
			        	id: value.id,
				        title: value.title,
				        status: value.publish,
				        created: value.created,
				        modified: value.modified,
			      	});
			      	if(response.data.length-1 >= key)
			      	{
			      		$scope.figureOutTodosToDisplayAlbum(1);
			      	}
			      	
				},$scope.todos_album);
				
				$scope.figureOutTodosToDisplay(1);
				
        	}, function errorCallback(response) {});


		};

		$scope.figureOutTodosToDisplay = function(page) 
		{
		    $scope.currentPage  = page
		    var begin = (($scope.currentPage - 1) * $scope.itemsPerPage);
		    var end = begin + $scope.itemsPerPage;
		    $scope.filteredTodos = $scope.todos.slice(begin, end);
		    //reset items each pagination
		 
	    	if($scope.HasallItems!=null)
	    	{
	      		$scope.HasallItems = false;
	    	}
	  	};


	  	$scope.figureOutTodosToDisplayAlbum = function(page) 
		{
		    $scope.currentPageAlbum  = page
		    var begin = (($scope.currentPageAlbum - 1) * $scope.itemsPerPageAlbum);
		    var end = begin + $scope.itemsPerPageAlbum;
		    $scope.filteredTodosAlbum = $scope.todos_album.slice(begin, end);
		    //reset items each pagination
		 
	    	if($scope.HasallItemsAlbum!=null)
	    	{
	      		$scope.HasallItemsAlbum = false;
	    	}
	  	};

		$scope.makeTodos(); 
		$scope.makeTodosAlbum ();

		$scope.pageChanged =  function(page) 
		{
		  $scope.figureOutTodosToDisplay(page);
		};

		$scope.pageChangedAlbum =  function(page) 
		{
		  $scope.figureOutTodosToDisplayAlbum(page);
		};

		$scope.open_uploader = function ()
	   	{      
	   	  $scope.files = [];
	       jquery('#id_files').focus().trigger('click');
	       
	    }
	    
		//listen for the file selected event
		$scope.$on("fileSelected", function (event, args) {
		    $scope.$apply(function () {  
		        $scope.files.push(args.file);
		    });
		});

		
		$scope.DELETE = function(id)
		{
			Media.Delete(id).then(function successCallback(response){
				$scope.makeTodos(); 
				$scope.figureOutTodosToDisplay(1);
			}, function errorCallback(response) {});
		}

	}]).controller('MediaNewCtrl', 
	[ '$scope','$state','$translate','$stateParams','Tags','MediaAlbum','Media',
	  function ($scope,$state,$translate,$stateParams,Tags,MediaAlbum,Media) 
	  {

	  	
	  	$scope.model = {
	  		'title':'',
	  		'content':'',
	  		'image':'',
	  		'tags_lists': [],
	  		'album_lists': [], 
	  	} 
	  	$scope.image = null;
	  	$scope.tags = [];
		$scope.album = [];

		$scope.makeTodos = function()
		{
		
			
        	Tags.list().then(function successCallback(response)
		    {
		    	angular.forEach(response.data, function(value, key){

	         			checked =  $scope.model.tags_lists.filter(function(item){
				              	return item.id === value.id;
				          	});
					     			
					 	this.push({
				        	id: value.id,
					        title: value.name,
					        status: value.publish,
					        checked: checked.length > 0,
					        created: value.created,
					        modified: value.modified,
				      	});
			      	},$scope.tags);
        	}, function errorCallback(response) {});
        	MediaAlbum.list().then(function successCallback(response)
		    {
		    	angular.forEach(response.data, function(value, key){

	         			checked =  $scope.model.album_lists.filter(function(item){
				              	return item.id === value.id;
				          	});
					     			
					 	this.push({
				        	id: value.id,
					        title: value.title,
					        status: value.publish,
					        checked: checked.length > 0,
					        created: value.created,
					        modified: value.modified,
				      	});
			      	},$scope.album);
        	}, function errorCallback(response) {});
		};
		$scope.makeTodos();
	  	$scope.Save = function()
	  	{
          	$scope.model.tag_lists = $scope.tags.filter(function(item){        
              return item.checked === true;
          	});
          	$scope.model.album_lists = $scope.album.filter(function(item){        
              return item.checked === true;
          	});

		  

		 	Media.Save($scope.model).then(function successCallback(response)
		    {
		    	$state.go('root.media_edit',{'id':response.data.id});

		    }, function errorCallback(response) {});;;
		}

	}]).controller('MediaEditCtrl', 
	[ '$scope','$state','$translate','$stateParams','Tags','MediaAlbum','Media',
	  function ($scope,$state,$translate,$stateParams,Tags,MediaAlbum,Media) 
	  {

	  	
	  	$scope.model = {
	  		'title':'',
	  		'content':'',
	  		'image':'',
	  		'tags_lists': [],
	  		'album_lists': [], 
	  	} 
	  	$scope.image = null;
		$scope.tags = [];
		$scope.album = [];
	  	Media.Get( $stateParams.id ).then(function successCallback(response){
	  			$scope.model.title = response.data.title;
	  			$scope.model.image = response.data.image;
	  			$scope.model.content = response.data.content;
	  			$scope.model.tags_lists = response.data.tags_lists;	 	
	  			$scope.model.album_lists = response.data.albums_lists;	 			
	  			$scope.makeTodos();

			}, function errorCallback(response) {});
	  	

		$scope.makeTodos = function()
		{
		
			
        	Tags.list().then(function successCallback(response)
		    {
		    	angular.forEach(response.data, function(value, key){

	         			checked =  $scope.model.tags_lists.filter(function(item){
				              	return item.id === value.id;
				          	});
					     			
					 	this.push({
				        	id: value.id,
					        title: value.name,
					        status: value.publish,
					        checked: checked.length > 0,
					        created: value.created,
					        modified: value.modified,
				      	});
			      	},$scope.tags);
        	}, function errorCallback(response) {});
        	MediaAlbum.list().then(function successCallback(response)
		    {
		    	angular.forEach(response.data, function(value, key){

	         			checked =  $scope.model.album_lists.filter(function(item){
				              	return item.id === value.id;
				          	});
					     			
					 	this.push({
				        	id: value.id,
					        title: value.title,
					        status: value.publish,
					        checked: checked.length > 0,
					        created: value.created,
					        modified: value.modified,
				      	});
			      	},$scope.album);
        	}, function errorCallback(response) {});
		};

	  	$scope.Save = function()
	  	{

          	$scope.model.tag_lists = $scope.tags.filter(function(item){        
              return item.checked === true;
          	});
          	$scope.model.album_lists = $scope.album.filter(function(item){        
              return item.checked === true;
          	});

		  	$scope.model.id = $stateParams.id;

		 	Media.Update($scope.model);
		}

	}])
  
});


