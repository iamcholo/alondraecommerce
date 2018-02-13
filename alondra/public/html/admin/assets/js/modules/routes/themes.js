define(['angular'],function(angular){

    angular.module('app.routes.themes', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('root.themes',
        {
          url: '/themes',
        
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/themes/lists.html',
              controller: 'ThemeListCtrl'
            } 
          }
        })
        .state('root.themes.current', {
          url: '/page/{page:int}',
          params: {
            page:{ value: 1}
          },
        })
        
      }]);

  
});
