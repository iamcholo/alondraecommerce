define(['angular'],function(angular){

    angular.module('app.routes.tags', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('root.tags',
        {
          url: '/tags',
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/tags/lists.html',
              controller: 'TagsListCtrl',
            } 
          }
         
        })
        .state('root.tags.current', {
          url: '/page/{page:int}',
          params: {
            page:{ value: 1}
          },
        })
        .state('root.tags_edit', {
          url: '/tags/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              controller: 'TagsEditCtrl',
              templateUrl: '/admin/assets/js/modules/templates/tags/edit.html',
            } 
          }
         
        })  
        .state('root.tags_new', {
          url: '/tags/new',
          views: {
          'content': {
              controller: 'TagsNewCtrl',
              templateUrl: '/admin/assets/js/modules/templates/tags/edit.html',
            } 
          }
        });
      }]);

  
});
