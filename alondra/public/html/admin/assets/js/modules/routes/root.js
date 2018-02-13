define(['angular'],function(angular){

    angular.module('app.routes.root', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        
        .state('root', {
          
          views: {
            '': {
              abstract: true,
              templateUrl: '/admin/assets/js/modules/templates/layouts/dashboard.html',
            },
          }
        })
        //$locationProvider.html5Mode(true);

        
        
      }]);

  
});
