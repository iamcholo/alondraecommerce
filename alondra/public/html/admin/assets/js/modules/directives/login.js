angular.module('app.directives.login', [])

.directive('imOnline', ['$http','$cookies', '$interval', '$state','$rootScope', function($http,$cookies,$interval,$state,$rootScope) {
  return {
  
    replace: false,
    scope: false,
      
    controller:function($scope)
    {
      var listener = function(event, toState) {
         
            contains = [
              'login.screen',
              'login',
              'login.screen',
              'login.registration',             
              'login.forgot',
              'login.new_password',
              'login.reset_password',
              'login.reset_password_change',
              'login.register',



            ];
           
            if (contains.indexOf(toState.name)  <= 0)
            {
              var stop = function() 
              {
               
                  if(!$cookies.get('access_token'))
                  {
                      $state.go('login.screen');
                  }
              };
              
              //stop();
              $interval(stop, 1000);
                
            }   
           
        };
      $rootScope.$on('$stateChangeSuccess', listener);
    
     
    },
   
}
}])
;
