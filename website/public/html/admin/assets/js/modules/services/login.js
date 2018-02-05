define(['angular'],function(angular){

angular.module('app.services.login', [] )
.service('Login', [ 
    '$q', '$http',  '$rootScope',"$cookies", 
    function ($q, $http, $rootScope,$cookies) 
  {
    // AngularJS will instantiate a singleton by calling "new" on this function
    var service = {
        
        'API_URL': '/api',
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
                //headers: {'X-CSRFToken': $cookies['csrftoken']},
                params: params,
                data: data
            });
        },
          'request2': function(args) 
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
        'login': function(username, password){
            var data = {
                'username':username,
                'password':password,
            }
            return this.request({
                'method': "POST",
                'url': "/get_auth_token/",
                'data': data
            });
        },
        'logout': function(){
           
            return this.request({
                'method': "POST",
                'url': "/logout/",
            });
        },

        'NewUser': function(data){
            return this.request2({
                'method': "POST",
                'url': "/new/user/",
                'data': data
            });
        },

        'Reset': function(email){
            return this.request({
                'method': "POST",
                'url': "/me/password/reset/",
                'data': { 'email': email}
            });
        },
        'imOnline': function(){
            return this.request({
                'method': "GET",
                'url': "/check/online/",
            });
        },
        'ResetUpdateNewPassword': function(data){
            return this.request({
                'method': "POST",
                'url': "/me/password/reset/new/",
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


