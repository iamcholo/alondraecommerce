define(['angular'],function(angular){

    angular.module('app.routes.pages', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('root.pages',
        {
          url: '/pages',
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/pages/lists.html',
              controller: 'PagesListCtrl',
            } 
          }
         
        })
        .state('root.pages.current', {
          url: '/page/{page:int}',
          params: {
            page:{ value: 1}
          },
        })
        .state('root.page_edit', {
          url: '/pages/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              controller: 'PagesEditCtrl',
              templateUrl: '/admin/assets/js/modules/templates/pages/edit.html',
            } 
          }
         
        })  
        .state('root.page_new', {
          url: '/pages/new',
          views: {
          'content': {
              controller: 'PagesNewCtrl',
              templateUrl: '/admin/assets/js/modules/templates/pages/edit.html',
            } 
          }
        });
      }]);

  
});
