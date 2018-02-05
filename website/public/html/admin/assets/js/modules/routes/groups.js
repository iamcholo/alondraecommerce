define(['angular'],function(angular){

    angular.module('app.routes.groups', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
       /* .state('groups',
        {
          url: '/groups',
          templateUrl: 'admin/assets/js/modules/templates/groups/lists.html',
          controller: 'UserListCtrl'
        })
        .state('groups.current', {
          url: '/{page:int}',
          params: {
            page:{ value: 1}
          },
        })*/
        .state('root.group_edit', {
          url: '/groups/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              controller: 'GroupEditCtrl',
              templateUrl: '/admin/assets/js/modules/templates/groups/edit.html',
            } 
          }

        })  
        .state('root.group_new', {
          url: '/groups/new',
          views: {
          'content': {
              controller: 'GroupNewCtrl',
              templateUrl: '/admin/assets/js/modules/templates/groups/edit.html',
            } 
          }

        
        });
      }]);

  
});
