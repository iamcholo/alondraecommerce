define(['angular'],function(angular){

    angular.module('app.routes.attributes', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('root.attributes',
        {
          url: '/attributes',
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/attributes/lists.html',
              controller: 'AttributesListCtrl',
            } 
          }
         
        })
        .state('root.attributes.current', {
          url: '/page/{page:int}',
          params: {
            page:{ value: 1}
          },
        })
        .state('root.attributes_edit', {
          url: '/attributes/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              controller: 'AttributesEditCtrl',
              templateUrl: '/admin/assets/js/modules/templates/attributes/edit.html',
            } 
          }
         
        })  
        .state('root.attributes_new', {
          url: '/attributes/new',
          views: {
          'content': {
              controller: 'AttributesNewCtrl',
              templateUrl: '/admin/assets/js/modules/templates/attributes/edit.html',
            } 
          }
        });
      }]);

  
});
