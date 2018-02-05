define(['angular'],function(angular){

    angular.module('app.routes.comments', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('root.comments',
        {
          url: '/comments',
          views: {
          'content': {
               controller: 'CommentsListCtrl',
               templateUrl: '/admin/assets/js/modules/templates/comments/lists.html',
            } 
          }
          
        })
        .state('root.comments.current', {
          url: '/page/{page:int}',
          params: {
            page:{ value: 1}
          },
        })
        .state('root.comments_edit', {
          url: '/comment/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              controller: 'CommentsEditCtrl',
              templateUrl: '/admin/assets/js/modules/templates/comments/edit.html',
            } 
          }
          
        })  
        .state('root.comments_new', {
          url: '/comment/new',
        
          views: {
          'content': {
               controller: 'CommentsNewCtrl',
                templateUrl: '/admin/assets/js/modules/templates/comments/edit.html',
            } 
          }
        });
      }]);

  
});
