define(['angular'],function(angular){

    angular.module('app.routes.navigation', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('root.navigations',
        {
          url: '/navigations',
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/navigation/lists.html',
              controller: 'NavigationListCtrl',
            } 
          }
         
        })
        .state('root.navigations.current', {
          url: '/page/{page:int}',
          params: {
            page:{ value: 1}
          },
        })
        .state('root.navigation_edit', {
          url: '/navigation/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              controller: 'NavigationEditCtrl',
              templateUrl: '/admin/assets/js/modules/templates/navigation/edit.html',
            } 
          }
         
        })  
        .state('root.navigation_new', {
          url: '/navigation/new',
          views: {
          'content': {
              controller: 'NavigationNewCtrl',
              templateUrl: '/admin/assets/js/modules/templates/navigation/new.html',
            } 
          }
        });
      }]);





  
});
