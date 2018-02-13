define(['angular'],function(angular){

    angular.module('app.routes.category', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('root.categories',
        {
          url: '/categories',
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/categories/lists.html',
              controller: 'CategoryListCtrl',
            } 
          }
         
        })
        .state('root.categories.current', {
          url: '/page/{page:int}',
          params: {
            page:{ value: 1}
          },
        })
        .state('root.category_edit', {
          url: '/category/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              controller: 'CategoryEditCtrl',
              templateUrl: '/admin/assets/js/modules/templates/categories/edit.html',
            } 
          }
         
        })  
        .state('root.category_new', {
          url: '/category/new',
          views: {
          'content': {
              controller: 'CategoryNewCtrl',
              templateUrl: '/admin/assets/js/modules/templates/categories/edit.html',
            } 
          }
        });
      }]);

  
});
