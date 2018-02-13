define(['angular'],function(angular){

angular.module('app.services.user', [] )
.service('User', [ 
    '$q', '$http',  '$rootScope', '$cookies',
    function ($q, $http, $rootScope,$cookies) 
  {
    // AngularJS will instantiate a singleton by calling "new" on this function
    var service = {
        
        'API_URL': '/api',
        // Set use_session to true to use Django sessions to store security token.
        // Set use_session to false to store the security token locally and transmit it as a custom header.
        /* END OF CUSTOMIZATION */
        'request': function(args) 
        {
           
            // Continue
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
                headers: {
                    'Authorization': 'Token ' + $cookies.get('access_token'),
                    'Content-Type': 'application/json'
                },
                params: params,
                data: data
            });
        },
        'me': function(){
            return this.request({
                'method': "GET",
                'url': "/me/"              
            });
        },
        'Get': function(data){
            return this.request({
                'method': "POST",
                'url': "/user/",
                'data': data,             
            });
        },
        'Delete': function(data){
            return this.request({
                'method': "PUT",
                'url': "/user/delete/",
                'data': data,             
            });
        },
        'List': function(){
            return this.request({
                'method': "GET",
                'url': "/users/"              
            });
        },
        'update_me_profile': function(data){
            return this.request({
                'method': "PUT",
                'url': "/me/",   
                'data': data           
            });
        },  
        'update_me_profile': function(data){
            return this.request({
                'method': "PUT",
                'url': "/me/",   
                'data': data           
            });
        },  
        'update_me_password': function(data){
            return this.request({
                'method': "PUT",
                'url': "/me/password/",   
                'data': data           
            });
        },       
        'update_profile': function(data){
            return this.request({
                'method': "PUT",
                'url': "/user/",   
                'data': data           
            });
        },  
        'update_password': function(data){
            return this.request({
                'method': "PUT",
                'url': "/me/password/",   
                'data': data           
            });
        },       
        'initialize': function(url){
            this.API_URL = url;         
        }

    }
    return service;
  }]);




});


