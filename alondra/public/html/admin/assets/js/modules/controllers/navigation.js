define(['angular','jquery'],function(angular,jquery){
 	angular.module('app.controllers.navigation', [])
 	.controller('NavigationListCtrl', 
	['$scope','$state','$translate','User','Navigation',// TIP: Access Route Parameters for your page via $stateParams.parameterName
	  function ($scope,$state,$translate,User,Navigation) 
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

				return re.test(item.username) ;
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
		    Navigation.List().then(function successCallback(response){
	         	angular.forEach(response.data, function(value, key){
				 	this.push({
			        	id: value.id,
			        	title: value.name,
					    img: '/admin/assets/img/nav.png'
			      	});			     
				},$scope.todos);
				$scope.figureOutTodosToDisplay(1);
        	});

        	
		};

			
		$scope.DELETE = function(id)
		{
			Navigation.Delete(id).then(function successCallback(response){
				$scope.makeTodos(); 
			});
		}
		$scope.figureOutTodosToDisplay = function(page) 
		{
		    $scope.currentPage  = page;
		    var begin = (($scope.currentPage - 1) * $scope.itemsPerPage);
		    var end = begin + $scope.itemsPerPage;
		    $scope.filteredTodos = $scope.todos.slice(begin, end);
	    	if($scope.HasallItems!=null)
	    	{
	      		$scope.HasallItems = false;
	    	}
	  	};

		$scope.makeTodos(); 

		$scope.pageChanged =  function(page) 
		{
		  $scope.figureOutTodosToDisplay(page);
		};

	}]).controller('NavigationEditCtrl', 
	[ '$scope','$state','$translate','$stateParams','Posts','Pages','Category','Navigation','NavigationItems',
	  function ($scope,$state,$translate,$stateParams,Posts,Pages, Category, Navigation, NavigationItems) 
	  {


	  	$scope.model = {
	  		'id':$stateParams.id,
	  		'name':'',
	  		'navigation':[],
	  		'publish': true
	  	}
	  	              
        jquery("#nestable2").nestable({group: 1});   
        jquery("#nestable3").nestable({group: 1});
        jquery("#nestable4").nestable({group: 1});
		

		function listify(strarr) {
			
			var l = $("<ol>").addClass("dd-empty");
		  	if (strarr.length>0)
		  	{
		  		l = $("<ol>").addClass("dd-list");
		  	}
		  
			jquery.each(strarr, function(i, v) {
			    var c = jquery("<li>").addClass("dd-item"),
				    h = jquery("<div>").addClass("dd-handle").text(v["title"]);
				c.attr('data-id',v["item_id"])
				c.attr('data-nav',v["view_name"])
				c.append(h);
			    l.append(c.append(h));
			    if (!!v["parent"] && v["parent"].length > 0)
			    {			    	
			    	c.append(listify(v["parent"]));
			    }

			});
			return l;
		}


		
        NavigationItems.List( $stateParams.id ).then(function successCallback(response){

        	var d =  listify(response.data);
        	
        	if (d !== null)
        	{
        		jquery("#nestable").append(d);
        	}
	  		
	  		jquery("#nestable").nestable({group: 1,maxDepth :7}); 
        });  


        Navigation.Get( $stateParams.id ).then(function successCallback(response){

        	$scope.model.id = $stateParams.id;
        	$scope.model.name = response.data.name;
        	$scope.model.publish = response.data.publish;
	  	
        });  
        $scope.Save = function(){
        	$scope.model.navigation = jquery("#nestable").nestable('serialize');
        	Navigation.Update($scope.model); 
	  	}
  
	 	$scope.makeTodos = function()
		{
			$scope.categories = [];
		    Category.list().then(function successCallback(response)
		    {
	         	angular.forEach(response.data, function(value, key){
				 	this.push({
			        	id: value.id,
				        title: value.name,
				        nav_type: 'category',	
				        status: value.publish,
			      	});
			      			      	
				},$scope.categories);
			
        	});

		};

      
		$scope.makeTodos2 = function()
		{
			$scope.posts = [];
			$scope.pages = [];
		    Posts.list().then(function successCallback(response)
		    {
	         	angular.forEach(response.data, function(value, key){
				 	this.push({
			        	id: value.id,
				        title: value.title,
				        nav_type: 'post_details',
				        status: value.publish,
				        created: value.created,
				        modified: value.modified,
			      	});
			      				      	
				},$scope.posts);
				
        	});
        	Pages.list().then(function successCallback(response)
		    {
	         	angular.forEach(response.data, function(value, key){
				 	this.push({
			        	id: value.id,
				        title: value.title,
				        nav_type: 'page_details',
				        status: value.publish,
				        created: value.created,
				        modified: value.modified,
			      	});
			      				      	
				},$scope.pages);
				
        	});

		};
		$scope.makeTodos();
		$scope.makeTodos2();
	}]).controller('NavigationNewCtrl', 
	[ '$scope','$translate','Posts','Category','Navigation','NavigationItems',
	  function ($scope,$translate,Posts,Category,Navigation,NavigationItems) 
	  {


	  	$scope.model = {
	  		'name':'',
	  		'publish': true
	  	}


        $scope.Save = function(){
        	Navigation.New($scope.model).then(function successCallback(response)
		    {
		    	$state.go('root.navigation_edit',{'id':response.data.id});

		    }, function errorCallback(response) {});;;
	  	}
      
	}]);
  
});
