define(['angular'],function(angular){

    angular.module('app.routes.taxes', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('root.taxes',
        {
          url: '/taxes',
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/taxes/lists.html',
              controller: 'TaxesListCtrl',
            } 
          }
         
        })
        .state('root.taxes.current', {
          url: '/page/{page:int}',
          params: {
            page:{ value: 1}
          },
        })
        .state('root.taxes_edit', {
          url: '/taxes/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              controller: 'TaxesEditCtrl',
              templateUrl: '/admin/assets/js/modules/templates/taxes/edit.html',
            } 
          }
         
        })  
        .state('root.taxes_new', {
          url: '/taxes/new',
          views: {
          'content': {
              controller: 'TaxesNewCtrl',
              templateUrl: '/admin/assets/js/modules/templates/taxes/edit.html',
            } 
          }
        });
      }]);

  
});
