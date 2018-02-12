define(['angular'],function(angular){
 	angular.module('app.controllers.orders', [])
 	.controller('OrdersListCtrl', 
	[ '$scope','$state','$translate','Orders',
	  function ($scope,$state,$translate, Orders) 
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
		    Orders.list().then(function successCallback(response)
		    {
	         	angular.forEach(response.data, function(value, key){
				 	this.push({
			        	id: value.id,
				        title: value.order_id,
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
			Orders.Delete(id).then(function successCallback(response){
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

	}]).controller('OrdersEditCtrl', 
	[ '$scope','$state','$translate','$stateParams','Orders',
	  function ($scope,$state,$translate,$stateParams,Orders) 
	  {

	  	$scope.model = { 
	  		'name':'', 
	  		'publish': true,
	  		'slug':'',
	  		'meta_title':'',
	  		'meta_description':''
	  	} 

	


	  	Orders.Get( $stateParams.id ).then(function successCallback(response){
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
	  	Orders.Update($scope.model);
	  }

	}]).controller('OrdersNewCtrl', 
	[ '$scope','$state','$translate','Orders',
	  function ($scope,$state,$translate, Orders) 
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
		  
		  	Orders.New($scope.model).then(function successCallback(response)
		    {
		    	$state.go('root.Orders_edit',{'id':response.data.id});

		    }, function errorCallback(response) {});;;
		}

	 
	  

	}]).controller('OrdersViewCtrl', 
	[ 
		'$scope','$state','$translate','$stateParams','Orders','OrdersItems',
	  	function ($scope,$state,$translate,$stateParams,Orders,OrdersItems){

	  	$scope.model = { 
	  		'id':$stateParams.id,
	  		'order_id':null,
            'status':null,
            'autor':null,
            'payment_method':{},
            'billing_address':{},
            'shipping_address':{},
            'todos':[],
            'total':0.00,
            'currency':"USD",
            'created':null, 
            'modified':null,

	  	} 

	


	  	Orders.Get( $stateParams.id ).then(function successCallback(response){
	  			$scope.model.status = response.data.status;
	  			$scope.model.order_id = response.data.order_id;
	  			$scope.model.payment_method = response.data.payment_methodx;
	  			//$scope.model.currency = response.data.currency;
	  			$scope.model.autor = response.data.autorx;
	  			$scope.model.billing_address = response.data.billing_addresssx;
	  			$scope.model.shipping_address = response.data.shipping_addressx;
	  			$scope.model.total = response.data.total;
	  			$scope.model.created = response.data.created;
	  			$scope.model.modified = response.data.modified;
	  			OrdersItems.list($stateParams.id).then(function successCallback(response){
		  			angular.forEach(response.data, function(value, key){
					 	this.push({
				        	id: value.id,
				        	thumbnail: value.productx.thumbnail
					        title: value.productx.title,
					        price: value.price,
					        currency: $scope.model.payment_method.currency,
					        carrier: value.carrier,
					        tracking_number: value.tracking_number,
				      	});
					},$scope.model.todos);
	  			}, function errorCallback(response) {});
			}, function errorCallback(response) {});
	}]);
  
});


