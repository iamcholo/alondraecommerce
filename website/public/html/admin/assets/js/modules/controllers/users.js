define(['angular'],function(angular){
 	angular.module('app.controllers.users', [])
 	.controller('UserListCtrl', 
	['$scope','$state','$translate','User',// TIP: Access Route Parameters for your page via $stateParams.parameterName
	  function ($scope,$state,$translate,User) 
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
		    User.List().then(function successCallback(response){
	         	angular.forEach(response.data, function(value, key){
				 	this.push({
			        	id: value.id,
			        	is_superuser: value.is_superuser,
			        	role: (value.is_superuser == true)?'Admin':'User',
				        username: value.username,
				        project_type: value.project_type,
				        description: value.content
			      	});
			      	if(response.data.length-1 >= key)
			      	{
			      		$scope.figureOutTodosToDisplay(1);
			      	}
			      	
				},$scope.todos);
        	}, function errorCallback(response) {});


		};

			
		$scope.DELETE = function(id)
		{
			User.Delete({'id':id}).then(function successCallback(response){
				$scope.makeTodos(); 
			}, function errorCallback(response) {});
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

	}]).controller('UserEditCtrl', 
	[ '$scope','$state','$translate','$stateParams','User',
	  function ($scope,$state,$translate,$stateParams,User) 
	  {


	  	$scope.model = {
	  		'id':$stateParams.id,
	  		'first_name':'',
	  		'last_name':'',
	  		'email':'',	 
	  		'nick':'',	 
	  		'username':'',
	  		'old_password':'',
			'new_password':'',
			'repeat_new_password':'',
	  	}
	  	User.Get({'id':$scope.model.id}).then(function successCallback(response){
         	$scope.model.first_name = response.data.first_name;
         	$scope.model.first_name = response.data.first_name;
         	$scope.model.last_name = response.data.last_name;
         	$scope.model.username = response.data.username;
         	$scope.model.email = response.data.email;
         	$scope.model.nick = response.data.nick;
        }, function errorCallback(response) {});

        $scope.updateProfile = function()
        {
        	User.update_profile({
        		'id': $scope.model.id ,
				'first_name': $scope.model.first_name ,
				'last_name': $scope.model.last_name, 
				'email': $scope.model.email,
				'username': $scope.model.username,
				'nick': $scope.model.nick
        	});
        }
        
        $scope.updatePassword = function()
        {
        	User.update_password({
        		'id': $scope.model.id ,
				'old_password': $scope.model.old_password,
				'new_password': $scope.model.new_password, 
				'repeat_new_password': $scope.model.repeat_new_password
        	}).then(function successCallback(response){
        		$scope.model.old_password = null;
				$scope.model.new_password = null;
				$scope.model.repeat_new_password = null;
			});
        }
	}]).controller('UserNewCtrl', 
	[ '$scope','$state','$translate','$stateParams','Login',
	  function ($scope,$state,$translate,$stateParams,Login) 
	  {


	  	$scope.model = {
	  		'first_name':'',
	  		'last_name':'',
	  		'email':'',	 
	  		'nick':'',	 
	  		'username':'',	  
			'password':''
	  	}
	  

        $scope.new_user = function()
        {
        	Login.NewUser({        		
				'first_name': $scope.model.first_name ,
				'last_name': $scope.model.last_name, 
				'email': $scope.model.email,
				'username': $scope.model.username,
				'nick': $scope.model.nick,
				'password': $scope.model.password
        	}).then(function successCallback(response) 
        	{
            	$state.go('root.users');
        	});

        	
        }
        
      
	}]);
  
});
