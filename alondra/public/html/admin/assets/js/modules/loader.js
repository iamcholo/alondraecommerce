require.config({
    paths: {
      "jquery": "vendor/dashboard/jquery/jquery.min",
      "bootstrap":"vendor/dashboard/bootstrap/bootstrap.min",
      "jquery_migrate": "vendor/dashboard/jquery/jquery-migrate.min",
      "country_picker": "vendor/country-picker.min",
      "simplemde": "modules/directives/simplemde",
      "dropzone_directive": "modules/directives/dropzone",
      "datepicker_directive": "modules/directives/datepicker",
      "login_directive": "modules/directives/login",
      "files_directive": "modules/directives/files",
      "SimpleMDE": "vendor/simplemde.min",
      "clipboard": "vendor/clipboard.min",
      "custom": "modules/custom",
      "custom": "modules/custom",
      "angular": "vendor/angular.min",
      "angular_cookies": "vendor/angular-cookies",
      "paging":"vendor/paging",
      "app": "modules/app",
      "router": "vendor/angular-ui-router",
      "translate": "vendor/angular-translate.min",
      "posts_controllers": "modules/controllers/posts",
      "pages_controllers": "modules/controllers/pages",
      "navigation_controllers": "modules/controllers/navigation",
      "category_controllers": "modules/controllers/category",
      "tags_controllers": "modules/controllers/tags",
      "taxes_controllers": "modules/controllers/taxes",
      "media_controller": "modules/controllers/media",
      "users_controller": "modules/controllers/users",
      "themes_controllers": "modules/controllers/themes",
      "comments_controller": "modules/controllers/comments",
      "login_controller": "modules/controllers/login",
      "root_routers": "modules/routes/root",
      "posts_routers": "modules/routes/posts", 
      "pages_routers": "modules/routes/pages",  
      "category_routers": "modules/routes/category",
      "navigation_routers": "modules/routes/navigation",
      "user_routers": "modules/routes/users",     
      "media_routers": "modules/routes/media", 
      "themes_routers": "modules/routes/themes",
      "tags_routers": "modules/routes/tags",
      "taxes_routers": "modules/routes/taxes",
      "comments_routers": "modules/routes/comments",
      "login_routers": "modules/routes/login",
      "login_services": "modules/services/login",
      "user_services": "modules/services/user",
      "posts_services": "modules/services/posts",
      "pages_services": "modules/services/pages",
      "media_services": "modules/services/media",
      "navigation_services": "modules/services/navigation",
      "navigation_items_services": "modules/services/navigation_items",
      "comments_services": "modules/services/comments",
      "category_services": "modules/services/category",
      "tags_services": "modules/services/tags",
      "taxes_services": "modules/services/taxes",
      "discounts_services": "modules/services/discounts",
      "I18N_EN":"modules/I18N/EN",
      "I18N_ES":"modules/I18N/ES",
      "directives":"modules/directives",
      "services":"modules/services",
      "dashboard":"modules/dashboard",
      //custom games
      "orders_controllers": "modules/controllers/orders",
      "orders_routers": "modules/routes/orders",
      "orders_services": "modules/services/orders",
      "orders_items_services": "modules/services/orders_items",

      "media_album_controllers": "modules/controllers/media_album",
      "media_album_routers": "modules/routes/media_album",
      "media_album_services": "modules/services/media_album",


      "attributes_controllers": "modules/controllers/attributes",
      "attributes_routers": "modules/routes/attributes",
      "attributes_services": "modules/services/attributes",
      "attributes_product_services": "modules/services/attributes_product",

    },
    baseUrl: '/admin/assets/js/',
    shim: {
      'app': {
        deps: [
          'angular',
          'angular_cookies',
          'country_picker',
          'paging',
          'simplemde',
          'dropzone_directive',
          'datepicker_directive',
          'login_directive',
          'custom',
          'router',
          'translate',
          'I18N_EN',
          'I18N_ES',
          'directives',
          'services',
          'root_routers',
          'media_controller',
          'media_routers',
          'media_services',

          'login_controller',
          'login_routers',          
          'login_services',
          'themes_routers',
          'themes_controllers',
          'comments_controller',          
          'comments_routers',         
          'dashboard',
          'users_controller',
          'user_services',
          'user_routers',
          'posts_controllers',
          'posts_routers',
          'posts_services',
          'pages_controllers',
          'pages_routers',
          'pages_services',
          'category_controllers',
          'category_routers',
          'category_services',
          'tags_controllers',
          'tags_routers',
          'tags_services',
          'taxes_controllers',
          'taxes_routers',
          'taxes_services',
          'discounts_services',
          'comments_services',         
          'files_directive',
          'clipboard',
          'navigation_controllers',
          'navigation_routers',
          'navigation_services',
          'navigation_items_services',
   
          'orders_controllers',
          'orders_routers',
          'orders_services',
          'orders_items_services',

          'attributes_controllers',
          'attributes_routers',
          'attributes_services',
          'attributes_product_services',

          'media_album_controllers',
          'media_album_routers',
          'media_album_services',
        ]
      },
      
      "directives": {
        deps: ["angular"]
      },
       "angular_cookies": {
        deps: ["angular"]
      },
      "country_picker": {
        deps: ["angular"]
      },

      
     
     
      'router': {
        deps: ['angular']
      },
      'paging': {
        deps: ['angular']
      },
      'translate': {
        deps: ['angular']
      },
      'simplemde': {
        deps: ['angular','SimpleMDE']
      },

      'dropzone_directive': {
        deps: ['angular','dashboard']
      },


      'datepicker_directive': {
        deps: ['angular','jquery']
      },



      'themes_routers': {
        deps: ['angular']
      },
      'themes_controllers': {
        deps: ['angular']
      },
      
   
      'angular':{
        exports : "angular",
      },
     'I18N_EN': {
        deps: ['angular']
      },
      'I18N_ES': {
        deps: ['angular']
      },
      'directives': {
        deps: ['angular']
      },
      'services': {
        deps: ['angular']
      },
      'posts_controllers': {
        deps: ['angular','jquery']
      },

      'media_controller': {
        deps: ['angular']
      },

      'users_controller': {
        deps: ['angular']
      },
      'comments_controller': {
        deps: ['angular']
      },
      'comments_routers': {
        deps: ['angular']
      },
      
      'login_controller': {
        deps: ['angular']
      },
   
      'user_routers': {
        deps: ['angular']
      },
      'login_routers': {
        deps: ['angular']
      },
      'media_routers': {
        deps: ['angular']
      },
      'posts_routers': {
        deps: ['angular']
      },
      'root_routers': {
        deps: ['angular']
      },
      'login_routers': {
        deps: ['angular']
      },
      'login_services': {
        deps: ['angular']
      },
      'user_services': {
        deps: ['angular']
      },
      'posts_services': {
        deps: ['angular']
      },
      'login_directive': {
        deps: ['angular']
      },

      'category_controllers': {
        deps: ['angular']
      },

      'category_routers': {
        deps: ['angular']
      },
      
      'category_services': {
        deps: ['angular']
      },

      'tags_controllers': {
        deps: ['angular']
      },

      'tags_routers': {
        deps: ['angular']
      },
      
      'tags_services': {
        deps: ['angular']
      },


      'taxes_controllers': {
        deps: ['angular']
      },

      'taxes_routers': {
        deps: ['angular']
      },
      
      'taxes_services': {
        deps: ['angular']
      },
      'discounts_services': {
        deps: ['angular']
      },


      'comments_services': {
        deps: ['angular']
      },
      
      'media_services': {
        deps: ['angular']
      },
      'navigation_controllers': {
        deps: ['angular']
      },
      'navigation_routers': {
        deps: ['angular']
      },
      'navigation_services': {
        deps: ['angular']
      },
      'navigation_items_services': {
        deps: ['angular']
      },

      'files_directive': {
        deps: ['angular']
      },
      'angular_file_upload': {
        deps: ['angular']
      },
      //custom

      'orders_controllers': {
        deps: ['angular']
      },
      'orders_routers': {
        deps: ['angular']
      },
      'orders_services': {
        deps: ['angular']
      },



      'media_album_controllers': {
        deps: ['angular']
      },
      'media_album_routers': {
        deps: ['angular']
      },
      'media_album_services': {
        deps: ['angular']
      },

      'attributes_controllers': {
        deps: ['angular']
      },
      'attributes_routers': {
        deps: ['angular']
      },
      'attributes_services': {
        deps: ['angular']
      },

      'attributes_product_services': {
        deps: ['angular']
      },


      





    },
    deps: ['app'],
    waitSeconds: 1880
});

var modules = [];
modules.push('app');

// Start the main app logic.
requirejs(modules, function (App) {
  App.bootstrap();
});