define(['angular'],function(angular){

    angular.module('app.routes.posts', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('root.posts',
        {
          url: '/posts',
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/posts/lists.html',
              controller: 'PostsListCtrl',
            } 
          }
         
        })
        .state('root.posts.current', {
          url: '/page/{page:int}',
          params: {
            page:{ value: 1}
          },
        })
        .state('root.post_edit', {
          url: '/post/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              controller: 'PostsEditCtrl',
              templateUrl: '/admin/assets/js/modules/templates/posts/edit.html',
            } 
          }
         
        })  
        .state('root.post_new', {
          url: '/post/new',
          views: {
          'content': {
              controller: 'PostsNewCtrl',
              templateUrl: '/admin/assets/js/modules/templates/posts/edit.html',
            } 
          }
        });
      }]);

  
});
