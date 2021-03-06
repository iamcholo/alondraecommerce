define(['angular'],function(angular){
 	angular.module('app.controllers.orders', [])
 	.controller('OrdersListCtrl', 
	[ '$scope','$state','$translate','Orders',
	  function ($scope,$state,$translate, Orders) 
	  {

	  	$scope.filteredTodos = [];
	  	$scope.itemsPerPage = 100;
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
		    	
	         	angular.forEach(response.data.items, function(value, key){

				 	this.push({
			        	id: value.id,
				        title: value.order_id,
				        status: value.status,
			      	});
			      	if(response.data.items.length-1 >= key)
			      	{
			      		$scope.figureOutTodosToDisplay(1);
			      	}
			      	
				},$scope.todos);
				
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
            'statuses':[],
            'autor':null,
            'payment_method':{},
            'billing_address':{},
            'shipping_address':{},
            'todos':[],
            'carriers':[

            ],
            'total':0,
            'currency':"USD",
            'created':null, 
            'modified':null,
            'editable':false,

	  	} 

	  	$translate(['PERSONAL_DELIVERY',]).then(function (translations)
	  	{

			$scope.model.carriers = [
				{'id':'USPS','label':'USPS'},
				{'id':'FEDEX','label':'FEDEX'},
				{'id':'DHL','label':'DHL'},
				{'id':'MRW','label':'MRW'},
				{'id':'PERSONAL_DELIVERY','label':translations.PERSONAL_DELIVERY},
			];
				
			   
		}, function (translationIds) {});

	  	$translate(['approved','pending','refunded','processed',]).then(function (translations)
	  	{

			$scope.model.statuses = [
				{'id':'approved','label':translations.approved},
				{'id':'pending','label':translations.pending},
				{'id':'refunded','label':translations.refunded},
				{'id':'processed','label':translations.processed},
			];
				
			   
		}, function (translationIds) {});

		$scope.editable = function(item)
		{
			
			item.editable = true;
				

		}

		$scope.save_status = function(item)
		{
			
			item.editable = false;
			console.log(item.status)
			Orders.Update({
				'id':$stateParams.id,
				'status':item.status,
			})	
		}





		$scope.SaveShipping = function(item)
		{
			item.editable = false;
			OrdersItems.Update({
				'id':item.id,
				'carrier':item.carrier,
				'tracking_number':item.tracking_number
			})	

		}

	  	Orders.Get( $stateParams.id ).then(function successCallback(response){
	  			$scope.model.status = response.data.status;
	  			$scope.model.order_id = response.data.order_id;
	  			$scope.model.payment_method = response.data.payment_methodx;
	  			//$scope.model.currency = response.data.currency;
	  			$scope.model.autor = response.data.autorx;
	  			$scope.model.billing_address = response.data.billing_addresssx;
	  			$scope.model.shipping_address = response.data.shipping_addressx;
	  			//$scope.model.total = response.data.total;
	  			$scope.model.created = response.data.created;
	  			$scope.model.modified = response.data.modified;
	  			OrdersItems.list($stateParams.id).then(function successCallback(response){
		  			angular.forEach(response.data, function(value, key){
		  				$scope.model.total += value.price;
		  				 	
					 	this.push({
				        	id: value.id,
				        	thumbnail: value.productx.thumbnail,
					        title: value.productx.title,
					        price: value.price,
					        qty: value.qty,
					        editable: false,
					        currency: $scope.model.payment_method.currency,
					        carrier: value.carrier,
					        tracking_number: value.tracking_number,
				      	});
					},$scope.model.todos);
	  			}, function errorCallback(response) {});
			}, function errorCallback(response) {});
	}]);
  
});


