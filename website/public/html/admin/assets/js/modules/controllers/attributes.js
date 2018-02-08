define(['angular'],function(angular){
 	angular.module('app.controllers.attributes', [])
 	.controller('AttributesListCtrl', 
	[ '$scope','$state','$translate','Attributes',
	  function ($scope,$state,$translate, Attributes) 
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
		    Attributes.list().then(function successCallback(response)
		    {
	         	angular.forEach(response.data, function(value, key){
				 	this.push({
			        	id: value.id,



				        title: value.name,
				        archetype: value.archetype,
				         priceable: value.priceable,
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
			Attributes.Delete(id).then(function successCallback(response){
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

	}]).controller('AttributesEditCtrl', 
	[ '$scope','$state','$translate','$stateParams','Attributes',
	  function ($scope,$state,$translate,$stateParams,Attributes) 
	  {

	  	$scope.model = { 
	  		'id':$stateParams.id ,
	  		'name':'', 
	  		'priceable': true,
	  		'archetype':'choices',
	  		'archetype_types':[],
	  	} 

	  	$translate(['CHOICES', 'TEXT', 'SELECTABLE','DATE',]).then(function (translations) {
			  
			    $scope.model.archetype_types = [
			    	{'id':'choices','label':translations.CHOICES},
		  			{'id':'text','label':translations.TEXT},
		  			{'id':'selectable','label':translations.SELECTABLE},
		  			{'id':'date','label':translations.DATE},
			    ]
			   
			  }, function (translationIds) {
			 
		});
	  	

	  	Attributes.Get( $stateParams.id ).then(function successCallback(response){
	  			$scope.model.name = response.data.name;
	  			$scope.model.priceable = response.data.priceable;
	  			$scope.model.archetype = response.data.archetype;
			}, function errorCallback(response) {});
	  	
	  	$scope.save = function()
	  {
	  	$scope.model.id = $stateParams.id;
	  	Attributes.Update($scope.model);
	  }

	}]).controller('AttributesNewCtrl', 
	[ '$scope','$state','$translate','Attributes',
	  function ($scope,$state,$translate, Attributes) 
	  {
		$scope.model = { 
	  		'name':'', 
	  		'priceable': true,
	  		'archetype':'choices',
	  		'archetype_types':[],
	  	} 
		$translate(['CHOICES', 'TEXT', 'SELECTABLE','DATE',]).then(function (translations){
			$scope.model.archetype_types = [
				{'id':'choices','label':translations.CHOICES},
		  		{'id':'text','label':translations.TEXT},
		  		{'id':'selectable','label':translations.SELECTABLE},
		  		{'id':'date','label':translations.DATE},
			]
			   
		}, function (translationIds) {});

	  	$scope.save = function()
		{
		  
		  	Attributes.New($scope.model).then(function successCallback(response)
		    {
		    	$state.go('root.attributes_edit',{'id':response.data.id});

		    }, function errorCallback(response) {});;;
		}

	 
	  

	}]);
  
});


