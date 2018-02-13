define(['angular'],function(angular){
 	angular.module('app.controllers.category', [])
 	.controller('CategoryListCtrl', 
	[ '$scope','$state','$translate','Category',
	  function ($scope,$state,$translate, Category) 
	  {

	  	$scope.filteredTodos = [];
	  	$scope.itemsPerPage = 8;
	  	$scope.currentPage = 1;
		$scope.model = {'query':''};
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

		$scope.makeTodos = function()
		{
			$scope.todos = [];
			$scope.filteredTodos = [];
		    Category.list().then(function successCallback(response)
		    {
	         	angular.forEach(response.data, function(value, key){
				 	this.push({
			        	id: value.id,
				        title: value.name,
				        status: value.publish,
			      	});
			      	if(response.data.length-1 >= key)
			      	{
			      		$scope.figureOutTodosToDisplay(1);
			      	}
			      	
				},$scope.todos);
				if(response.data.length > 0)
				{
					$scope.figureOutTodosToDisplay(1);
				}
        	}, function errorCallback(response) {});


		};

		$scope.DELETE = function(id)
		{
			Category.Delete(id).then(function successCallback(response){
				$scope.makeTodos(); 
			}, function errorCallback(response) {});
		}

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

		$scope.makeTodos(); 
		$scope.figureOutTodosToDisplay(1);

		$scope.pageChanged =  function(page) 
		{
		  $scope.figureOutTodosToDisplay(page);
		};

	}]).controller('CategoryEditCtrl', 
	[ '$scope','$state','$translate','$stateParams','Category',
	  function ($scope,$state,$translate,$stateParams,Category) 
	  {

	  	$scope.model = { 
	  		'name':'', 
	  		'publish': true,
	  		'slug':'',
	  		'meta_title':'',
	  		'meta_description':''
	  	} 

	  	$scope.ChangeTitle = function()
	  	{
	  		 $scope.model.meta_title = $scope.model.name
	  		 $scope.model.slug = window.string_to_slug($scope.model.name)
	  	}

	  	Category.Get( $stateParams.id ).then(function successCallback(response){
	  			$scope.model.name = response.data.name;
	  			$scope.model.publish = response.data.publish;
	  			$scope.model.content = response.data.content;
	  			$scope.model.meta_title = response.data.meta_title;
	  			$scope.model.meta_description = response.data.meta_description;
	  			$scope.model.slug = response.data.slug;

			}, function errorCallback(response) {});
	  	
	  	$scope.save = function()
	  {
	  	$scope.model.id = $stateParams.id;
	  	Category.Update($scope.model);
	  }

	}]).controller('CategoryNewCtrl', 
	[ '$scope','$state','$translate','Category',
	  function ($scope,$state,$translate, Category) 
	  {

	  	$scope.model = {
	  		'name':'',
	  		'publish': true,
	  		'slug':'',
	  		'meta_title':'',
	  		'meta_description':''
	  	} 
	  	$scope.ChangeTitle = function()
	  	{
	  		 $scope.model.meta_title = $scope.model.name
	  		 $scope.model.slug = window.string_to_slug($scope.model.name)
	  	}


	  	$scope.save = function()
		{
		  
		  	Category.New($scope.model).then(function successCallback(response)
		    {
		    	$state.go('root.category_edit',{'id':response.data.id});

		    }, function errorCallback(response) {});;;
		}

	 
	  

	}]);
  
});


