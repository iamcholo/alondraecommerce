define(['angular'],function(angular){

    angular.module('app.routes.custom.games', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('root.games',
        {
          url: '/custom/games',
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/custom/games/lists.html',
              controller: 'GamesListCtrl',
            } 
          }
         
        })
        .state('root.games.current', {
          url: '/page/{page:int}',
          params: {
            page:{ value: 1}
          },
        })
        .state('root.game_edit', {
          url: '/custom/games/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              controller: 'GamesEditCtrl',
              templateUrl: '/admin/assets/js/modules/templates/custom/games/edit.html',
            } 
          }
         
        })  
        .state('root.game_new', {
          url: '/custom/games/new',
          views: {
          'content': {
              controller: 'GamesNewCtrl',
              templateUrl: '/admin/assets/js/modules/templates/custom/games/edit.html',
            } 
          }
        });
      }]);

  
});
