define(['angular','clipboard'],function(angular,clipboard){
 	angular.module('app.controllers.pages', [])
 	.controller('PagesListCtrl', 
	[ '$scope','$state','$translate','Pages',
	  function ($scope,$state,$translate, Pages) 
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
		    Pages.list().then(function successCallback(response)
		    {
	         	angular.forEach(response.data, function(value, key){
				 	this.push({
			        	id: value.id,
				        title: value.title,
				        img: '/admin/assets/img/logo.jpg',
				        status: value.publish,
				        created: value.created,
				        modified: value.modified,
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
			Pages.Delete(id).then(function successCallback(response){
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
		$scope.pageChanged =  function(page) 
		{
		  $scope.figureOutTodosToDisplay(page);
		};

	}]).controller('PagesEditCtrl', 
	[ '$scope','$state','$translate','$stateParams','Pages','Media',
	  function ($scope,$state,$translate,$stateParams,Pages,Media) 
	  {

	  	new clipboard('.btn');
	  	$scope.model = {
	  		'title':'',
	  		'publish': true,
	  		'post_type': 'page',
	  		'is_featured': true,
	  		'is_on_feed': true,
	  		'thumbnail':'',
	  		'thumbnail_text':'',
	  		'featured_image':'',
            'featured_image_text':'',
	  		'content':'',
	  		'slug':'',
	  		'meta_title':'',
	  		'meta_description':''
	  	} 
	  	$scope.query = '';
		$scope.name = '';

	  	$scope.search = function()
	  	{	if($scope.query.length > 0)
	  		{
	  			$scope.images = $scope.images.filter(function(item){
	  				re = new RegExp($scope.query);
					return re.test(item.title) ;
				});
				
	  		}else
	  		{
	  			$scope.makeTodosMedia(); 
	  		}
	  		
	  	}

	  		$scope.ChangeTitle = function()
	  	{
	  		 $scope.model.meta_title = $scope.model.title
	  		 $scope.model.slug = window.string_to_slug($scope.model.title)
	  	}


	  	Pages.Get( $stateParams.id ).then(function successCallback(response){
	  			$scope.model.title = response.data.title;			
	  			$scope.model.publish = response.data.publish;
	  			$scope.model.is_featured = response.data.is_featured;
	  			$scope.model.is_on_feed = response.data.is_on_feed;
	  			$scope.model.content = response.data.content;
	  			$scope.model.meta_title = response.data.meta_title;
	  			$scope.model.featured_image = response.data.featured_image;
	  			$scope.model.featured_image_text = response.data.featured_image_text;
	  			$scope.model.thumbnail = response.data.thumbnail;
	  			$scope.model.thumbnail_text = response.data.thumbnail_text;
	  			$scope.model.meta_description = response.data.meta_description;
	  			$scope.model.slug = response.data.slug;
	  			$scope.makeTodos();
	  			$scope.makeTodosMedia();

			}, function errorCallback(response) {});
	  	

	  	$scope.confirmAction = function(){
	  		return Pages.Get( $stateParams.id );
	  	}



	 
	  	$scope.makeTodosMedia = function()
		{
			$scope.images = [];
		    Media.list().then(function successCallback(response)
		    {
	         	angular.forEach(response.data, function(value, key){
	         	
				 	this.push({
			        	id: value.id,
				        title: value.title,
				        status: value.publish,
				        img: value.image,
				        featured_checked: value.image === $scope.model.featured_image,
				        thumb_checked: value.image === $scope.model.thumbnail,
				        created: value.created,
				        modified: value.modified,
			      	});
				},$scope.images);
        	}, function errorCallback(response) {});
		};



		$scope.featured_image = function (value) {
			featured_image = $scope.images.filter(function(item){        
              return item.id !== value.id;
          	});
          	angular.forEach(featured_image, function(value, key){

          		value.featured_checked = false;
          	})
        	
   		}
   		$scope.thumb_checked = function (value) {
			thumb = $scope.images.filter(function(item){        
              return item.id !== value.id;
          	});
          	angular.forEach(thumb, function(value, key){
          		value.thumb_checked = false;
          	});        	
   		}
	  	$scope.Save = function()
	  	{
	  		featured_image = $scope.images.filter(function(item){        
              return item.featured_checked === true;
          	});
          	thumbnail = $scope.images.filter(function(item){        
              return item.thumb_checked === true;
          	});
         
		  	$scope.model.id = $stateParams.id;

		  	if(featured_image.length > 0)
		  	{
		  		$scope.model.featured_image = featured_image[0].img;
		  		$scope.model.featured_image_text =  thumbnail[0].title;
		  		
		  	}
		  	if(thumbnail.length > 0)
		  	{
		  		$scope.model.thumbnail = thumbnail[0].img;
		  		$scope.model.thumbnail_text = thumbnail[0].title;
		  		
		  	}
		 	Pages.Update($scope.model);
		}

		$scope.makeTodosMedia();

	}]).controller('PagesNewCtrl', 
	[ '$scope','$state','$translate','Pages','Category','Media',
	  function ($scope,$state,$translate, Pages,Category,Media) 
	  {
	  	new clipboard('.btn');
	  	$scope.model = {
	  		'title':'',
	  		'post_type': 'page',
	  		'publish': true,
	  		'is_featured': true,
	  		'is_on_feed': true,
	  		'thumbnail':'',
	  		'thumbnail_text':'',
	  		'featured_image':'',
            'featured_image_text':'',
	  		'content':'',
	  		'slug':'',
	  		'meta_title':'',
	  		'meta_description':''
	  	} 
		$scope.query = '';
	  	$scope.search = function()
	  	{	if($scope.query.length > 0)
	  		{
	  			$scope.images = $scope.images.filter(function(item){
	  				re = new RegExp($scope.query);
					return re.test(item.title) ;
				});
				
	  		}else
	  		{
	  			$scope.makeTodosMedia(); 
	  		}
	  		
	  	}

	  	$scope.ChangeTitle = function()
	  	{
	  		 $scope.model.meta_title = $scope.model.title
	  		 $scope.model.slug = window.string_to_slug($scope.model.title)
	  	}
	  	$scope.Save = function()
	  	{	
	  		featured_image = $scope.images.filter(function(item){        
              return item.featured_checked === true;
          	});
          	thumbnail = $scope.images.filter(function(item){        
              return item.thumb_checked === true;
          	});
         
         	if(featured_image.length > 0)
		  	{
		  		$scope.model.featured_image = featured_image[0].img;
		  		$scope.model.featured_image_text =  thumbnail[0].title;
		  		
		  	}
		  	if(thumbnail.length > 0)
		  	{
		  		$scope.model.thumbnail = thumbnail[0].img;
		  		$scope.model.thumbnail_text = thumbnail[0].title;
		  		
		  	}
	  		
	  		Pages.New($scope.model).then(function successCallback(response)
		    {
		    	$state.go('root.page_edit',{'id':response.data.id});

		    }, function errorCallback(response) {});;
	  	}
		$scope.makeTodosMedia = function()
		{
			$scope.images = [];
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
				},$scope.images);
        	}, function errorCallback(response) {});
		};
		$scope.makeTodosMedia();
	
	}]);
  
});


