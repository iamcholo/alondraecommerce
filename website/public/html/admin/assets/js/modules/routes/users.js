define(['angular'],function(angular){

    angular.module('app.routes.users', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('root.users',
        {
          url: '/users',
         
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/user/lists.html',
              controller: 'UserListCtrl'
            } 
          }
        })
        .state('root.users.current', {
          url: '/{page:int}',
          params: {
            page:{ value: 1}
          },
        })
        .state('root.user_edit', {
          url: '/user/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/user/edit.html',
              controller: 'UserEditCtrl',
            } 
          }
         
          
        })  
        .state('root.user_new', {
          url: '/user/new',
          views: {
          'content': {
              controller: 'UserNewCtrl',
              templateUrl: '/admin/assets/js/modules/templates/user/new.html',
            } 
          }
         
        });



      }]);

  
});
