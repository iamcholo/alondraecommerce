define(['angular'],function(angular){

    angular.module('app.routes.orders', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('root.orders',
        {
          url: '/orders',
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/orders/lists.html',
              controller: 'OrdersListCtrl',
            } 
          }
         
        })
        .state('root.orders.current', {
          url: '/page/{page:int}',
          params: {
            page:{ value: 1}
          },
        })
        .state('root.orders_edit', {
          url: '/orders/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              controller: 'OrdersEditCtrl',
              templateUrl: '/admin/assets/js/modules/templates/orders/edit.html',
            } 
          }
         
        })  
        .state('root.orders_new', {
          url: '/orders/new',
          views: {
          'content': {
              controller: 'OrdersNewCtrl',
              templateUrl: '/admin/assets/js/modules/templates/orders/edit.html',
            } 
          }
        });
      }]);

  
});
