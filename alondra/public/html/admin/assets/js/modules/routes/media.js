define(['angular'],function(angular){

    angular.module('app.routes.media', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('root.media',
        {
          url: '/media',
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/media/lists.html',
              controller: 'MediaListCtrl'
             
            } 
          }
        })
        .state('root.media.current', {
          url: '/page/{page:int}',
          params: {
            page:{ value: 1}
          },
        }).state('root.media_new',
        {
          url: '/media/new/',
        
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/media/edit.html',
              controller: 'MediaNewCtrl'
             
            } 
          }
        })
        .state('root.media_edit',
        {
          url: '/media/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/media/edit.html',
              controller: 'MediaEditCtrl'
             
            } 
          }
        })
      
      }]);

  
});
