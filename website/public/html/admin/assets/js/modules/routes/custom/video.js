define(['angular'],function(angular){

    angular.module('app.routes.custom.video', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('root.videos',
        {
          url: '/custom/videos',
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/custom/video/lists.html',
              controller: 'VideoListCtrl',
            } 
          }
         
        })
        .state('root.video.current', {
          url: '/page/{page:int}',
          params: {
            page:{ value: 1}
          },
        })
        .state('root.video_edit', {
          url: '/custom/video/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              controller: 'VideoEditCtrl',
              templateUrl: '/admin/assets/js/modules/templates/custom/video/edit.html',
            } 
          }
         
        })  
        .state('root.video_new', {
          url: '/custom/video/new',
          views: {
          'content': {
              controller: 'VideoNewCtrl',
              templateUrl: '/admin/assets/js/modules/templates/custom/video/edit.html',
            } 
          }
        });
      }]);

  
});
