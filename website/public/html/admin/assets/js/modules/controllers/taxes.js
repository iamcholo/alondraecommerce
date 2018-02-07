define(['angular'],function(angular){
 	angular.module('app.controllers.taxes', [])
 	.controller('TaxesListCtrl', 
	[ '$scope','$state','$translate','Taxes',
	  function ($scope,$state,$translate, Taxes) 
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
		    Taxes.list().then(function successCallback(response)
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
			Taxes.Delete(id).then(function successCallback(response){
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

	}]).controller('TaxesEditCtrl', 
	[ '$scope','$state','$translate','$stateParams','Taxes',
	  function ($scope,$state,$translate,$stateParams,Taxes) 
	  {

	  	$scope.model = { 
	  		
	  		'city': '',
			'country': 'USA',
			'percent': 0.00,
	  	} 


	  	Taxes.Get( $stateParams.id ).then(function successCallback(response){
	  			$scope.model.city = response.data.city;
	  			$scope.model.country = response.data.country;
	  			$scope.model.percent = response.data.percent;
	  		

			}, function errorCallback(response) {});
	  	
	  	$scope.save = function()
	  {
	  	$scope.model.id = $stateParams.id;
	  	Taxes.Update($scope.model);
	  }

	}]).controller('TaxesNewCtrl', 
	[ '$scope','$state','$translate','Taxes',
	  function ($scope,$state,$translate, Taxes) 
	  {

	  	$scope.model = {
	  		
	  		'city': '',
			'country': 'USA',
			'percent':0.00,
	  	} 

	  
	  	$scope.save = function()
		{
		  
		  	Taxes.New($scope.model).then(function successCallback(response)
		    {
		    	$state.go('root.taxes_edit',{'id':response.data.id});

		    }, function errorCallback(response) {});;;
		}

	 
	  

	}]);
  
});


