define(
    [
      "angular",
      "router",
      "app_boostrap"
    ],

    function (angular)
    {
      var app = angular.module('app', [
        'ui.router',
        'bw.paging',
        'ngCookies',
        'puigcerber.countryPicker',
        'cms-simplemde',
        'dropzone',
        'datepicker',
        'pascalprecht.translate', 
        'app.directives',
        'app.directives.login',
        'app.directives.fileupload',
        'app.controllers.posts',
        'app.controllers.pages',
        'app.controllers.category',
        'app.controllers.tags',
        'app.controllers.taxes',
        'app.controllers.comments',
        'app.controllers.media',
        'app.controllers.media_album',
        'app.controllers.users',
        'app.controllers.themes',        
        'app.controllers.login',
        'app.controllers.navigation',
        'app.controllers.orders',
        'app.services.user',
        'app.services.login',
        'app.services.posts',
        'app.services.pages',
        'app.services.tags',
        'app.services.taxes',
        'app.services.discounts',
        'app.services.category',
        'app.services.comments',
        'app.services.media',
        'app.services.media_album',
        'app.services.navigation',
        'app.services.navigation_items',
        'app.services.orders',
        'app.routes.posts',
        'app.routes.pages',
        'app.routes.media',
        'app.routes.media_album',
        'app.routes.users',
        'app.routes.category',
        'app.routes.tags',
        'app.routes.taxes',
        'app.routes.comments',
        'app.routes.themes',
        'app.routes.root',
        'app.routes.login',
        'app.routes.navigation',
        'app.routes.orders',
        'app.I18N.EN',
        'app.I18N.ES',
      ]);
      
      var resize_window = function()
      {
        window.app.accordionFullHeightResize();
        window.app.features.gallery.controlHeight();
        window.app.spy();
      }
      function intializedash()
      {
     
        resize_window();
        angular.element(window).on('resize', resize_window);
      
      }


      app.run([
        '$rootScope', '$state','$http', '$stateParams', '$interval','Login',
        function ($rootScope, $http,  $state, $stateParams,$interval,Login) 
        {
         
          $rootScope.$state = $state;

          $rootScope.$stateParams = $stateParams;
          intializedash();
          $interval(resize_window, 100);

         $rootScope.$on('$includeContentLoaded', function(){
              window.app.init();
              window.app.layout();
              window.app.resizableLayout();  
              window.app.navigation();        
              window.app.navigationMobile();
              window.app.contentTabs();    
              window.app.formsFile();
              window.app.checkAll();
              window.app.features.gallery.init();
              window.app.features.preview.init();
              window.app.statusbar.init();    
              window.app.search();   
              window.app.misc();
              //window.app_plugins.customScrollBar();
              window.app_plugins.checkbox_radio();
              window.app_plugins.formSpinner();
              window.app_plugins.switch_button();
              window.app_plugins.bootstrap_select();
              window.app_plugins.select2();
              window.app_plugins.bootstrap_popover();
              window.app_plugins.bootstrap_datepicker();
              window.app_plugins.bootstrap_tooltip();
              window.app_plugins.maskedInput();
              window.app_plugins.datatables();
              window.app_plugins.knob();
              window.app_plugins.sparkline();
              window.app_plugins.isotope();
              window.app_plugins.noty();
              window.app_plugins.wizard();
              //window.app_plugins.nestable();
              window.app_plugins.bootstrap_daterange();
              window.app_plugins.multiselect();
              window.app_plugins.bootstrap_colorpicker();
              window.app_demo.googlemap();
              window.app_demo.jvectormap();
              window.app_demo.solutions.bank.change_password();
              window.app_demo.solutions.bank.change_pin();
              window.app_demo.charts.morris();
              window.app_demo.charts.rickshaw();
              window.app_demo.charts.chartjs();
              window.app_plugins.Dropzone();
               //intializedash();


          });
          $rootScope.$on('$viewContentLoaded', function() {
            //intializedash();

          });
          $rootScope.$on('$stateChangeStart', function (event, toState, toParams, fromState, fromParams){
            //intializedash();
             
              contains = [
                'login.screen',
                'login',
                'login.screen',
                'login.registration',             
                'login.forgot',
                'login.new_password',
              ];
            
             
          });
        }
      ]);
    
      app.config([
      '$stateProvider', '$urlRouterProvider',"$locationProvider",'$translateProvider','$httpProvider','$cookiesProvider',
      function($stateProvider, $urlRouterProvider, $locationProvider,$translateProvider,$httpProvider,$cookiesProvider)
      {
        $urlRouterProvider.otherwise('/login');
        $cookiesProvider.defaults.path = "/";
        $translateProvider.useSanitizeValueStrategy('sanitizeParameters');
        $translateProvider.preferredLanguage('es');
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      }]);
      
      app.bootstrap = function () {
        angular.bootstrap(document, ['app']);
      }
     
      return app;
   
});