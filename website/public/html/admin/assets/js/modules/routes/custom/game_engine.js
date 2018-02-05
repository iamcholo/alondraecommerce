define(['angular'],function(angular){

    angular.module('app.routes.custom.game_engine', ['ui.router']).config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",
      function($stateProvider, $urlRouterProvider, $locationProvider) 
      {
        $stateProvider
        .state('root.game_engines',
        {
          url: '/custom/game_engines',
          views: {
          'content': {
              templateUrl: '/admin/assets/js/modules/templates/custom/game_engine/lists.html',
              controller: 'GameEngineListCtrl',
            } 
          }
         
        })
        .state('root.game_engines.current', {
          url: '/page/{page:int}',
          params: {
            page:{ value: 1}
          },
        })
        .state('root.game_engine_edit', {
          url: '/custom/game_engine/edit/{id:int}',
          params: {
            id:{ value: 0}
          },
          views: {
          'content': {
              controller: 'GameEngineEditCtrl',
              templateUrl: '/admin/assets/js/modules/templates/custom/game_engine/edit.html',
            } 
          }
         
        })  
        .state('root.game_engine_new', {
          url: '/custom/game_engine/new',
          views: {
          'content': {
              controller: 'GameEngineNewCtrl',
              templateUrl: '/admin/assets/js/modules/templates/custom/game_engine/edit.html',
            } 
          }
        });
      }]);

  
});
