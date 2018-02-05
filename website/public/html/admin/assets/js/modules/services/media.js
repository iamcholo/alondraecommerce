define(['angular'],function(angular){

angular.module('app.services.media', [] )
.service('Media', [ 
    '$q', '$http',  '$cookies',
    function ($q, $http,$cookies) 
  {
    // AngularJS will instantiate a singleton by calling "new" on this function
    var service = {
        
        'API_URL': '/api',
        'uploadprogress': 0,
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
                method: method.toUpperCase(),
                 headers: {
                    'Authorization': 'Token '+$cookies.get('access_token'),
                    'Content-Type': undefined
                },
                transformRequest: angular.identity,
                data: data
            });
        },
        'request5': function(args) 
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
                    'Authorization': 'Token '+$cookies.get('access_token'),
                    'Content-Type':  'application/json'
                },
                params: params,
                data: data
            });
        },
        'request3': function(args) 
        {
            params = args.params || {}
            args = args || {};
            var deferred = $q.defer(),
                url = this.API_URL + args.url,
                method = args.method || "GET",
                params = params,
                data = args.data || {};
            
            return $http({
                url: url,
                withCredentials: this.use_session,
                method: method.toUpperCase(),
                headers: {
                    'Authorization': 'Token '+$cookies.get('access_token'),
                    'Content-Type':  'application/json'
                },
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
                headers: {'Content-Type': undefined},
                params: params,
                uploadEventHandlers: {
                    progress: function(e)
                    {
                        if (e.lengthComputable) 
                        {
                            service.uploadprogress = (e.loaded / e.total) * 100;
                        }
                    }
                },
                data: data
            });
        },
        'list': function(){
            return this.request({
                'method': "GET",
                'url': "/images/"                    
            });
        },
        'New': function(data){
            return this.request2({
                'method': "PUT",
                'url': "/image/create/",
                'data': data
            });
        },
        'Save': function(data){
            return this.request5({
                'method': "POST",
                'url': "/image/",
                'data': data       
            });
        },
        'Update': function(data){
            return this.request5({
                'method': "PUT",
                'url': "/image/",
                'data': data       
            });
        },
        'Get': function(id){
            return this.request5({
                'method': "POST",
                'url': "/image/details/",
                'data': {'id':id,}                 
            });
        },
        'Delete': function(id){
            return this.request3({
                'method': "DELETE",
                'url': "/image/", 
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


