define(['angular'],function(angular){

    angular.module('app.routes.media_album', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
       .state('root.media_album_edit',
        {
          url: '/media/album/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/media_album/edit.html',
              controller: 'MediaAlbumEditCtrl'
             
            } 
          }
        })
        .state('root.media_album_new',
        {
          url: '/media/album/new/',
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/media_album/edit.html',
              controller: 'MediaAlbumNewCtrl'
             
            } 
          }
        })
      
      }]);

  
});
