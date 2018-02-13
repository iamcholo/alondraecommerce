define(['angular'],function(angular){
 	angular.module('app.controllers.comments', [])
 	.controller('CommentsListCtrl',
	[ '$scope','$state','$translate','Comment',
	  function ($scope,$state,$translate,Comment) 
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
					return re.test(item.email) ;
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
		    Comment.list().then(function successCallback(response)
		    {
	         	angular.forEach(response.data, function(value, key){
				 	this.push({
			        	id: value.id,
				        name: value.name,
				        email: value.email,
				        website: value.website,
				        img: '/admin/assets/images/logo.jpg',
				        status: value.status,
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

		$scope.makeTodos();


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

	}]).controller('CommentsEditCtrl', 
	[ '$scope','$state','$translate',
	  function ($scope,$state,$translate) 
	  {
	  	$scope.content = "SADASDSAD";
	  

	}]).controller('CommentsNewCtrl', 
	[ '$scope','$state','$translate',
	  function ($scope,$state,$translate) 
	  {

	  	$scope.content = "SADASDSAD";
	  

	}]);
  
});


