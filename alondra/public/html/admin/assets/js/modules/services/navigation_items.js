define(['angular'],function(angular){

angular.module('app.services.navigation_items', [] )
.service('NavigationItems', [ 
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
                params: params,
                data: data
            });
        },


        'List': function(id){
            return this.request({
                'method': "POST",
                'url': "/nav/items/" ,
                'data': {'id':id,}                 
            });
        },
                   
        'initialize': function(url){
            this.API_URL = url;         
        }

    }
    return service;
  }]);




});


