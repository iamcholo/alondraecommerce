define(['angular'],function(angular){
 	angular.module('app.controllers.themes', [])
 	.controller('ThemeListCtrl', 
	[ '$scope','$state','$translate',// TIP: Access Route Parameters for your page via $stateParams.parameterName
	  function ($scope,$state,$translate) 
	  {

	  	$scope.filteredTodos = [];
	  	$scope.itemsPerPage = 8;
	  	$scope.currentPage = 1;
		$scope.makeTodos = function()
		{
		    $scope.todos = [];
		  
		    for(i=0; i<=15;i++)
		    {

		      $scope.todos.push({
		        id: i,
		        img : '/admin/assets/images/users/user_3.jpg',
		        title : 'Test Project'+ i,
		        created : '2012-10-11',     
		        updated : '2012-10-11',      
		        status : 'pending'
		      });
		    }
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

		$scope.makeTodos(); 
		$scope.figureOutTodosToDisplay(1);

		$scope.pageChanged =  function(page) 
		{
		  $scope.figureOutTodosToDisplay(page);
		};

	}]).controller('ThemesEditCtrl', 
	[ '$scope','$state','$translate','$window',
	  function ($scope,$state,$translate,$window) 
	  {
	  	$window.app_plugins.nestable();
	  	$scope.content = "SADASDSAD";
	  

	}]).controller('ThemesNewCtrl', 
	[ '$scope','$state','$translate',
	  function ($scope,$state,$translate) 
	  {
	  	$window.app_plugins.nestable();
	  	$scope.content = "SADASDSAD";
	  

	}]);
  
});


