define(['angular'],function(angular){

    angular.module('app.routes.login', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('login', {
          
          views: {
            '': {
              abstract: true,
              templateUrl: '/admin/assets/js/modules/templates/layouts/login.html',
            },
          }
        })  
        .state('login.screen', {
          url: '/login',
         
          views: {
          'content': {
             controller: 'LoginCtrl',
             templateUrl:  '/admin/assets/js/modules/templates/user/login.html',
            } 
          }
         
        })
        .state('logout',
        {
          url: '/logout',
          controller: 'LogoutCtrl'
        });  
        ;

          
        
      }]);

  
});
