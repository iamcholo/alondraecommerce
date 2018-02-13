define(['angular'],function(angular){

angular.module('app.services.orders_items', [] )
.service('OrdersItems', [ 
    '$q', '$http',  '$rootScope', '$cookies',
    function ($q, $http, $rootScope,$cookies) 
  {
    // AngularJS will instantiate a singleton by calling "new" on this function
    var service = {
        
        'API_URL': '/api',
        'request': function(args) 
        {
            params = args.params || {}
            args = args || {};
            var deferred = $q.defer(),
                url = this.API_URL + args.url,
                method = args.method || "GET",
                params = params,
                data = args.data || {};
            
            return  $http({
                url: url,
                withCredentials: this.use_session,
                method: method.toUpperCase(),
                //headers: {'X-CSRFToken': $cookies['csrftoken']},
               headers: {
                    'Authorization': 'Token ' + $cookies.get('access_token'),
                    'Content-Type': 'application/json'
                },
                //transformRequest: angular.identity,
                params: params,
                data: data
            });
        },
        'list': function(id){
            return this.request({
                'method': "POST",
                'url': "/order/shipping/list/",
                'data': {'id':id,}             
            });
        },
        'New': function(data){
            return this.request({
                'method': "POST",
                'url': "/order/shipping/",
                'data': data              
            });
        },
        'Update': function(data){
            return this.request({
                'method': "PUT",
                'url': "/order/shipping/",
                'data': data       
            });
        },
        'Get': function(id){
            return this.request({
                'method': "POST",
                'url': "/order/shipping/details/",
                'data': {'id':id,}                 
            });
        },
        'Delete': function(id){
            return this.request({
                'method': "DELETE",
                'url': "/order/shipping/", 
                'data': {'id':id}             
            });
        },
           
        'initialize': function(url){
            this.API_URL = url;         
        }

    }
    return service;
  }]);




});


