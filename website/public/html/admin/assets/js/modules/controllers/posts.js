define(['angular','clipboard'],function(angular,clipboard){
 	angular.module('app.controllers.posts', [])
 	
 	.controller('PostsListCtrl', 
	[ '$scope','$state','$translate','Posts',
	  function ($scope,$state,$translate, Posts) 
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
		    Posts.list().then(function successCallback(response)
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
			Posts.Delete(id).then(function successCallback(response){
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

	}]).controller('PostsEditCtrl', 
	[ '$scope','$state','$translate','$stateParams','Posts','Tags','Category','Media','Taxes','pvpCountries','Discounts',
	  function ($scope,$state,$translate,$stateParams,Posts,Tags,Category,Media,Taxes,pvpCountries,Discounts) 
	  {

	  	new clipboard('.btn');
	  	$scope.model = {
	  		'title':'',
	  		'price':0.00,
	  		'qty': 0,
	  		'publish': true,
	  		'post_type': 'post',
	  		'is_featured': true,
	  		'is_on_feed': true,
	  		'publish_date': null,
	  		'thumbnail':'',
	  		'thumbnail_text':'',
	  		'featured_image':'',
            'featured_image_text':'',
            'taxes_lists':[],
	  		'categories_lists': [], 
	  		'tags_lists': [], 
	  		'content':'',
	  		'excerpt':'',
	  		'slug':'',
	  		'meta_title':'',
	  		'meta_description':''
	  	} 

	  	$scope.model2 = {
	  		'product_id': $stateParams.id ,
	  		'percent':0.00,
	  		'start_date':'',
	  		'end_date': '',
		} 
	  	$scope.query = '';
		$scope.name = '';
		$scope.showCountry = function(name)
	  	{
	  		return pvpCountries.getCountries().filter(function(item){
				return item.alpha2 == name;
			})[0].name;
	  	}
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

	  	Posts.Get( $stateParams.id ).then(function successCallback(response){
	  			$scope.model.title = response.data.title;
	  			$scope.model.price = response.data.price;
	  			$scope.model.qty = response.data.qty;
	  			$scope.model.categories_lists = response.data.categories_lists;	 
	  			$scope.model.tags_lists = response.data.tags_lists;	
	  			$scope.model.taxes_lists = response.data.taxes_lists;	
	  			$scope.model.publish = response.data.publish;
	  			$scope.model.publish_date = response.data.publish_date;	 
	  			$scope.model.is_featured = response.data.is_featured;
	  			$scope.model.is_on_feed = response.data.is_on_feed;
	  			$scope.model.content = response.data.content;
	  			$scope.model.excerpt = response.data.excerpt;
	  			$scope.model.meta_title = response.data.meta_title;
	  			$scope.model.featured_image = response.data.featured_image;
	  			$scope.model.featured_image_text = response.data.featured_image_text;
	  			$scope.model.thumbnail = response.data.thumbnail;
	  			$scope.model.thumbnail_text = response.data.thumbnail_text;
	  			$scope.model.meta_description = response.data.meta_description;
	  			$scope.model.slug = response.data.slug;
	  			$scope.makeTodos();
	  			$scope.makeTodosMedia();
	  			$scope.makeTodosTaxes();
			}, function errorCallback(response) {});
	  	

	  	$scope.confirmAction = function(){
	  		return Posts.Get( $stateParams.id );
	  	}

		$scope.makeTodos = function()
		{
			$scope.todos = [];
			$scope.tags = [];
			$scope.discounts = [];
		    Category.list().then(function successCallback(response)
		    {
		    	angular.forEach(response.data, function(value, key){

	         			checked =  $scope.model.categories_lists.filter(function(item){
				              	return item.id === value.id;
				          	});
					     			
					 	this.push({
				        	id: value.id,
					        title: value.name,
					        status: value.publish,
					        checked: checked.length > 0,
					        created: value.created,
					        modified: value.modified,
				      	});
			      	},$scope.todos);
        	}, function errorCallback(response) {});
        	Tags.list().then(function successCallback(response)
		    {
		    	angular.forEach(response.data, function(value, key){

	         			checked =  $scope.model.tags_lists.filter(function(item){
				              	return item.id === value.id;
				          	});
					     			
					 	this.push({
				        	id: value.id,
					        title: value.name,
					        status: value.publish,
					        checked: checked.length > 0,
					        created: value.created,
					        modified: value.modified,
				      	});
			      	},$scope.tags);
        	}, function errorCallback(response) {});



	  		Discounts.list($stateParams.id).then(function successCallback(response){
	  			angular.forEach(response.data, function(value, key){
					this.push({
						'id':value.id,
						'editable':false,
						'amount':value.amount,
						'start_date': value.start_date,
						'end_date': value.end_date,
					});
				},$scope.discounts);
			}, function errorCallback(response) {});

		};

		$scope.makeTodosTaxes = function()
		{
			$scope.taxes = [];
		    Taxes.list().then(function successCallback(response)
		    {
	         	angular.forEach(response.data, function(value, key){
	         			checked =  $scope.model.taxes_lists.filter(function(item){
				              	return item.id === value.id;
				          	});

				 	this.push({
			        	id: value.id,
				        title: value.percent,
				        city: value.city,
				        country: value.country,
				        checked: checked.length > 0,
				        
			      	});
				},$scope.taxes);
        	}, function errorCallback(response) {});
		};
	 
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

          	$scope.model.categories_lists = $scope.todos.filter(function(item){        
              return item.checked === true;
          	});

          	$scope.model.tag_lists = $scope.tags.filter(function(item){        
              return item.checked === true;
          	});

          	$scope.model.taxes_lists = $scope.taxes.filter(function(item){        
              return item.checked === true;
          	});

		  	$scope.model.id = $stateParams.id;

		  	if(featured_image.length > 0)
		  	{
		  		$scope.model.featured_image = featured_image[0].img;
		  		$scope.model.featured_image_text =  thumbnail[0].title;
		  		console.log(featured_image[0].img)
		  	}
		  	if(thumbnail.length > 0)
		  	{
		  		$scope.model.thumbnail = thumbnail[0].img;
		  		$scope.model.thumbnail_text = thumbnail[0].title;
		  		console.log(thumbnail[0].img)
		  	}
		 	Posts.Update($scope.model);
		}

		$scope.AddDiscounts = function()
		{
			if($scope.model2.percent > 0 && $scope.model2.start_date.length > 0 && $scope.model2.end_date.length > 0)
			{
				Discounts.New($scope.model2).then(function successCallback(response){
					$scope.discounts.push({
						'id':response.data.id,
						'editable':false,
						'percent':response.data.percent,
						'start_date': response.data.start_date,
						'end_date': response.data.end_date,
					});
				}, function errorCallback(response) {});
			}	
		}
		$scope.edit_Discount = function(id)
		{
			var item = $scope.discounts.filter(function(item){
	  				
					return item.id == id ;
				});
			if(item.length > 0)
			{
				item[0].editable = true;
			}
		}
		
		$scope.SaveDiscount = function(id)
		{
			var item = $scope.discounts.filter(function(item){
	  				
					return item.id == id ;
				});
			if(item.length > 0)
			{
				item[0].editable = false;
				Discounts.Update(item[0]);
			}
		}


		$scope.DELETE_Discount = function(id)
		{
			$scope.discounts = $scope.discounts.filter(function(item){
	  				
					return item.id != id ;
				});
			Discounts.Delete(id);
		}
		

	}]).controller('PostsNewCtrl', 
	[ '$scope','$state','$translate','$stateParams','Posts','Tags','Category','Media','Taxes','pvpCountries',
	  function ($scope,$state,$translate,$stateParams,Posts,Tags,Category,Media, Taxes,pvpCountries) 
	  {
	  	new clipboard('.btn');
	  	$scope.model = {
	  		'title':'',
	  		'price':0.00,
	  		'qty': 0,
	  		'publish': true,
	  		'post_type': 'post',
	  		'is_featured': true,
	  		'is_on_feed': true,
	  		'publish_date': null,
	  		'thumbnail':'',
	  		'thumbnail_text':'',
	  		'featured_image':'',
            'featured_image_text':'',
	  		'categories_lists': [], 
	  		'tags_lists': [], 
	  		'content':'',
	  		'excerpt':'',
	  		'slug':'',
	  		'meta_title':'',
	  		'meta_description':''
	  	} 
		$scope.query = '';

			Posts.New($scope.model).then(function successCallback(response)
		    {
		    	$state.go('root.post_edit',{'id':response.data.id});

		    }, function errorCallback(response) {});;


		$scope.showCountry = function(name)
	  	{
	  		return pvpCountries.getCountries().filter(function(item){
				return item.alpha2 == name;
			})[0].name;
	  	}
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
	  		$scope.model.categories_lists = $scope.todos.filter(function(item){
              	return item.checked === true;
          	});
          	$scope.model.tag_lists = $scope.tags.filter(function(item){        
              return item.checked === true;
          	});
          	$scope.model.taxes_lists = $scope.taxes.filter(function(item){        
              return item.checked === true;
          	});
	  		Posts.New($scope.model).then(function successCallback(response)
		    {
		    	$state.go('root.post_edit',{'id':response.data.id});

		    }, function errorCallback(response) {});;
	  	}

	  	$scope.AddDiscounts = function()
		{
			if($scope.model2.amount > 0 && $scope.model2.start_date.length > 0 && $scope.model2.end_date.length > 0)
			{
				//pending
					$scope.discounts.push({
						
						'editable':false,
						'amount':response.data.amount,
						'start_date': response.data.start_date,
						'end_date': response.data.end_date,
					});
				
			}	
		}
		$scope.edit_Discount = function(id)
		{
			var item = $scope.discounts.filter(function(item){
	  				
					return item.id == id ;
				});
			if(item.length > 0)
			{
				item[0].editable = true;
				

			}
		}

		$scope.DELETE_Discount = function(id)
		{
			$scope.discounts = $scope.discounts.filter(function(item){
	  				
					return item.id != id ;
				});
			Discounts.Delete(id);
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



		$scope.makeTodos = function()
		{
			$scope.todos = [];
			$scope.tags = [];
			$scope.taxes = [];
		    Taxes.list().then(function successCallback(response)
		    {
	         	angular.forEach(response.data, function(value, key){
				 	this.push({
			        	id: value.id,
				        title: value.percent,
				        city: value.city,
				        country: value.country,
				        checked: false,
			      	});
				},$scope.taxes);
        	}, function errorCallback(response) {});
		    Category.list().then(function successCallback(response)
		    {
	         	angular.forEach(response.data, function(value, key){
				 	this.push({
			        	id: value.id,
				        title: value.name,
				        status: value.publish,
				        checked: false,
				        created: value.created,
				        modified: value.modified,
			      	});

				},$scope.todos);
				
        	}, function errorCallback(response) {});
        	
			Tags.list().then(function successCallback(response)
		    {
		    	angular.forEach(response.data, function(value, key){

	         			
					     			
					 	this.push({
				        	id: value.id,
					        title: value.name,
					        status: value.publish,
					        checked: false,
					        created: value.created,
					        modified: value.modified,
				      	});
			      	},$scope.tags);
        	}, function errorCallback(response) {});
		};
	  	$scope.makeTodos();

	  	$scope.makeTodosMedia();
	  	
	}]);
  
});


